#!/usr/bin/env python3
# Adapted from Golem tutorial code by Jude Hungerford
import asyncio
import utils
import sys
import subprocess
import time
import numpy as np
from datetime import timedelta
from yapapi.log import enable_default_logger, log_summary, log_event_repr
from yapapi.runner import Engine, Task, vm
from yapapi.runner.ctx import WorkContext

GOLEM_WORKDIR = '/golem/work/'

def interpolate(fromVal, toVal, t):
    return fromVal + ((toVal - fromVal) * t)

def renderAnimation(ctx=None, tasks=None):
    subprocess.run(['convert', '-delay', '10', '-loop', '0', '*.png', 'output.gif'])

async def main(args):

    package = await vm.repo(
        image_hash="e34aaa2aac52cc98993b7d8fdbdcbafc9ba00aa2f38e7fa87796f7b7",
        min_mem_gib=0.5,
        min_storage_gib=2.0,
    )

    async def worker(ctx: WorkContext, tasks):
        async for task in tasks:
            (filename, offset, secondFrequency, smoothness) = task.data
            full_filename = filename + ".png"
            # Send these files so we don't have to update the Docker image
            ctx.send_file('graphWavePair.py', F'{GOLEM_WORKDIR}graphWavePair.py')
            ctx.run(F'chmod', 'u+x', F'{GOLEM_WORKDIR}graphWavePair.py')
            ctx.run(F'/bin/sh', '-c', F'{GOLEM_WORKDIR}graphWavePair.py {filename} {offset} {secondFrequency} {smoothness}')
            ctx.download_file(f'{GOLEM_WORKDIR+full_filename}', full_filename)

            yield ctx.commit()
            task.accept_task(result=full_filename)

    async with Engine(
        package=package,
        max_workers=args.number_of_providers,
        budget=10.0,
        # timeout should be keyspace / number of providers dependent
        timeout=timedelta(minutes=25),
        subnet_tag=args.subnet_tag,
        event_emitter=log_summary(log_event_repr),
    ) as engine:

        # Prepare our parameters for 125 graphs
        steps = np.arange(0.0, np.pi * 4, 0.1)
        numSteps = len(steps)
        inputs = []
        for (count, step) in enumerate(steps):
            filename = "graph-%04d" % (count,)
            if (step < np.pi * 2):
                distance = (count) / (numSteps / 2)
                secondFrequency = interpolate(10, 16, distance)
                smoothness = interpolate(10, 3, distance)
            else:
                distance = (count - numSteps / 2) / (numSteps / 2)
                secondFrequency = interpolate(16, 10, distance)
                smoothness = interpolate(3, 10, distance)
            inputs.append((filename, step, secondFrequency, smoothness))

        async for task in engine.map(worker, [Task(data=graphInput) for graphInput in inputs]):
            print(
                f"{utils.TEXT_COLOR_CYAN}"
                f"Task computed: {task}, result: {task.output}"
                f"{utils.TEXT_COLOR_DEFAULT}"
            )


if __name__ == "__main__":
    parser = utils.build_parser("golemGraph")
    parser.add_argument("--number-of-providers", dest="number_of_providers", type=int, default=4)
    args = parser.parse_args()
    enable_default_logger(log_file=args.log_file)
    sys.stderr.write(
        f"Using subnet: {utils.TEXT_COLOR_YELLOW}{args.subnet_tag}{utils.TEXT_COLOR_DEFAULT}\n"
    )

    loop = asyncio.get_event_loop()
    task = loop.create_task(main(args))

    try:
        # Generate a new set of images on the Golem network
        loop.run_until_complete(task)
        # Combine them locally
        renderAnimation()
    except (Exception, KeyboardInterrupt) as e:
        print(e)
        task.cancel()
        loop.run_until_complete(task)

