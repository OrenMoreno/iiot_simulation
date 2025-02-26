import paho.mqtt.client as mqtt
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import queue
import threading

# Queue to pass data from MQTT thread to main thread
data_queue = queue.Queue()
data = []

# Callback for when the client connects
def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("Connected to MQTT broker")
        client.subscribe("sensor/data")
    else:
        print(f"Failed to connect, return code {rc}")

# Callback for when a message is received (runs in MQTT thread)
def on_message(client, userdata, message):
    try:
        payload = message.payload.decode("utf-8")
        print(f"Received: {payload}")
        data_queue.put((datetime.now(), payload))  # Pass data to main thread
    except Exception as e:
        print(f"Error decoding message: {e}")

# Function to update the plot (runs in main thread)
def update_plot():
    plt.ion()  # Interactive mode
    fig = plt.figure(figsize=(10, 6))
    while True:
        try:
            # Get data from queue (non-blocking)
            timestamp, payload = data_queue.get_nowait()
            data.append((timestamp, payload))
            if len(data) > 100:
                data.pop(0)

            # Process and plot data
            df = pd.DataFrame(data, columns=["timestamp", "sensor_data"])
            df["temperature"] = df["sensor_data"].apply(lambda x: eval(x)["temperature"])
            df["humidity"] = df["sensor_data"].apply(lambda x: eval(x)["humidity"])
            plt.clf()
            plt.plot(df["timestamp"], df["temperature"], label="Temperature")
            plt.plot(df["timestamp"], df["humidity"], label="Humidity")
            plt.legend()
            plt.draw()
            plt.pause(0.01)  # Update display
            data_queue.task_done()  # Mark task as done
        except queue.Empty:
            plt.pause(0.1)  # Wait briefly if no new data
        except Exception as e:
            print(f"Error plotting data: {e}")
            plt.pause(0.1)

# Initialize MQTT client
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message

# Connect to broker
try:
    print("Connecting to MQTT broker...")
    client.connect("localhost", 1883, keepalive=60)
except Exception as e:
    print(f"Connection error: {e}")
    exit(1)

# Start MQTT loop in a separate thread
client.loop_start()

# Run plotting in the main thread
update_plot()