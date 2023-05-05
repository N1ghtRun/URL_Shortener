import asyncio

async def my_coroutine():
    print('Starting coroutine')
    await asyncio.sleep(1)
    print('Resuming coroutine')
    await asyncio.sleep(1)
    print('Ending coroutine')

async def main():
    print('Starting main')
    my_coroutine()
    print('Ending main')

asyncio.run(main())