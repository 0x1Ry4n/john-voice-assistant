import functools
import itertools
import asyncio


async def spin(msg):
    for char in itertools.cycle("⠇⠋⠙⠸⠴⠦"):
        status = msg + " " + char
        print(status, flush=True, end="\r")
        try:
            await asyncio.sleep(0.1)
        except asyncio.CancelledError:
            break
    print(" " * len(status), end="\r")


def spinner_msg(msg):
    def wrapper(func):
        @functools.wraps(func)
        async def wrapped(*args):
            spinner = asyncio.create_task(spin(msg))
            return await func(*args)

        return wrapped

    return wrapper
