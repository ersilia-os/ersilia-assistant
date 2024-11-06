import asyncio


async def start_llamafile():
    process = await asyncio.create_subprocess_shell(
        "/opt/llamafile/command.sh",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )

    async def read_output(stream):
        while True:
            line = await stream.readline()
            if not line:
                break
            output = line.decode()
            print(output, end="")
            if "llama server listening" in output:
                return

    await asyncio.gather(read_output(process.stdout), read_output(process.stderr))

    await process.wait()


asyncio.run(start_llamafile())
