import asyncio
import json
import matplotlib.pyplot as plt
from datetime import datetime
from aiocoap import *

data = []

async def get_sensor_data():
    try:
        protocol = await Context.create_client_context()
        request = Message(code=GET)
        request.set_request_uri('coap://127.0.0.1/sensor/data')
        response = await protocol.request(request).response
        payload = response.payload.decode('utf-8')
        print(f"Received from server: {payload}")  # Debug output
        return json.loads(payload)
    except Exception as e:
        print(f"Error fetching sensor data: {e}")
        return None

async def main():
    plt.ion()
    fig, ax = plt.subplots(figsize=(10, 6))
    while True:
        sensor_data = await get_sensor_data()
        if sensor_data:
            timestamp = datetime.now()
            data.append((timestamp, sensor_data['temperature'], sensor_data['humidity']))
            if len(data) > 100:
                data.pop(0)
            timestamps, temperatures, humidities = zip(*data)
            ax.clear()
            ax.plot(timestamps, temperatures, label='Temperature')
            ax.plot(timestamps, humidities, label='Humidity')
            ax.legend()
            plt.draw()
            plt.pause(0.1)
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())