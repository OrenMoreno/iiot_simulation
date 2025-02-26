import paho.mqtt.client as mqtt
import random
import time

broker = "localhost"
port = 1883
topic = "sensor/data"

# Callback for when the client connects to the broker
def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print(f"Connected to MQTT broker at {broker}:{port}")
    else:
        print(f"Failed to connect, return code {rc}")

# Callback for when a message is published
def on_publish(client, userdata, mid, properties=None):
    print(f"Message {mid} published")

def simulate_sensor_data():
    while True:
        temperature = random.uniform(20.0, 25.0)
        humidity = random.uniform(30.0, 50.0)
        payload = f'{{"temperature": {temperature}, "humidity": {humidity}}}'
        client.publish(topic, payload, qos=1)  # QoS 1 for confirmation
        print(f"Published: {payload}")
        time.sleep(1)

# Initialize client with updated API version
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)  # Use VERSION2 to avoid deprecation warning
client.on_connect = on_connect
client.on_publish = on_publish

# Attempt to connect
try:
    print(f"Attempting to connect to {broker}:{port}...")
    client.connect(broker, port, keepalive=60)
    client.loop_start()  # Start the network loop in a separate thread
    simulate_sensor_data()
except Exception as e:
    print(f"Connection error: {e}")
finally:
    client.loop_stop()  # Ensure the loop stops when done