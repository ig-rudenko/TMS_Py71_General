import asyncio


async def work(data):
    print(data)
    # I/O


async def main():
    print("start")

    await work(23)

    return 1


x = asyncio.run(main())
print(x)
