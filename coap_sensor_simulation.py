import asyncio
import random
from aiocoap import *

async def simulate_sensor_data():
    try:
        protocol = await Context.create_client_context()
        print("CoAP client context created successfully")
        while True:
            temperature = random.uniform(20.0, 25.0)
            humidity = random.uniform(30.0, 50.0)
            payload = f'{{"temperature": {temperature}, "humidity": {humidity}}}'.encode('utf-8')
            request = Message(code=POST, payload=payload)
            request.set_request_uri('coap://127.0.0.1/sensor/data')
            print("Sending request...")
            response = await protocol.request(request).response
            print('Result: %s\n%r' % (response.code, response.payload))
            await asyncio.sleep(1)
    except Exception as e:
        print(f"CoAP error: {str(e)}")

print("CoAP sensor simulation started")
asyncio.run(simulate_sensor_data())