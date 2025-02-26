import asyncio
import matplotlib.pyplot as plt
from datetime import datetime
from asyncua import Client

data = []

async def main():
    client = Client("opc.tcp://localhost:4840/freeopcua/server/")
    try:
        print("Attempting to connect to OPC UA server...")
        await client.connect()
        print("Connected to OPC UA server")
        
        # Get namespace index
        idx = await client.get_namespace_index("http://examples.freeopcua.github.io")
        print(f"Namespace index for 'http://examples.freeopcua.github.io': {idx}")
        
        # Use numeric node IDs from server output
        temperature_node = client.get_node(f"ns={idx};i=2")
        humidity_node = client.get_node(f"ns={idx};i=3")
        
        # Test node existence
        try:
            await temperature_node.read_value()
            print("Temperature node found")
            await humidity_node.read_value()
            print("Humidity node found")
        except Exception as e:
            print(f"Node verification error: {e}")
            raise

        plt.ion()
        fig, ax = plt.subplots(figsize=(10, 6))
        while True:
            try:
                temperature = await temperature_node.read_value()
                humidity = await humidity_node.read_value()
                timestamp = datetime.now()
                data.append((timestamp, temperature, humidity))
                if len(data) > 100:
                    data.pop(0)
                timestamps, temperatures, humidities = zip(*data)
                ax.clear()
                ax.plot(timestamps, temperatures, label='Temperature')
                ax.plot(timestamps, humidities, label='Humidity')
                ax.legend()
                plt.draw()
                plt.pause(0.1)
            except Exception as e:
                print(f"Error reading values: {e}")
            await asyncio.sleep(1)
    except Exception as e:
        print(f"Connection error: {e}")
    finally:
        await client.disconnect()
        print("Disconnected from OPC UA server")

if __name__ == "__main__":
    asyncio.run(main())