import asyncio
from aiocoap import Context, Message, CHANGED
from aiocoap.resource import Resource, Site

class SensorResource(Resource):
    def __init__(self):
        self.content = b""

    async def render_get(self, request):
        return Message(payload=self.content)

    async def render_post(self, request):
        self.content = request.payload
        return Message(code=CHANGED, payload=b"Data received")

async def main():
    root = Site()
    root.add_resource(['sensor', 'data'], SensorResource())
    # Bind to 127.0.0.1 instead of 0.0.0.0
    await Context.create_server_context(root, bind=('127.0.0.1', 5683))
    await asyncio.get_running_loop().create_future()

if __name__ == "__main__":
    asyncio.run(main())