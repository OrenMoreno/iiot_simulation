import subprocess
import os
import time
import sys
import signal
import atexit

# Store all processes to manage them later
processes = []

def clean_exit(signum=None, frame=None):
    """Clean up all processes when exiting"""
    print("Cleaning up processes...")
    for process in processes:
        try:
            process.terminate()
            process.wait(timeout=2)
        except:
            try:
                process.kill()
            except:
                pass
    sys.exit(0)

# Register clean exit handlers
atexit.register(clean_exit)
signal.signal(signal.SIGINT, clean_exit)
signal.signal(signal.SIGTERM, clean_exit)

def start_mqtt_broker():
    """Start the MQTT broker (Mosquitto)"""
    print("Starting MQTT broker...")
    try:
        # Try to start mosquitto (may fail if already running)
        broker_process = subprocess.Popen(
            ["mosquitto"], 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE
        )
        processes.append(broker_process)
        time.sleep(2)  # Give time to start
        
        # Check if broker is running
        if broker_process.poll() is not None:
            print("Note: MQTT broker may already be running or failed to start.")
            print("      If you have issues, try starting it manually with 'mosquitto'")
            return False
        return True
    except Exception as e:
        print(f"Error starting MQTT broker: {e}")
        print("Please start it manually with 'mosquitto'")
        return False

def start_script(script_name, window_title):
    """Start a Python script in a new terminal window"""
    print(f"Starting {script_name}...")
    
    if sys.platform == 'win32':
        # Windows version - use start cmd
        process = subprocess.Popen(
            f'start "{window_title}" cmd /k "cd /d {os.getcwd()} && venv\\Scripts\\activate && python {script_name}"',
            shell=True
        )
    else:
        # Unix version (not needed for this assignment but included for completeness)
        terminal_cmd = 'gnome-terminal'  # Default for Ubuntu
        process = subprocess.Popen([
            terminal_cmd, '--', 'bash', '-c',
            f'cd "{os.getcwd()}" && . venv/bin/activate && python {script_name}; exec bash'
        ])
    
    return process

def main():
    print("=== IIoT Simulation Launcher ===")
    
    # Ensure visualizations directory exists
    os.makedirs("visualizations", exist_ok=True)
    
    # First start the MQTT broker
    broker_running = start_mqtt_broker()
    time.sleep(2)  # Give broker time to start
    
    # Start sensor simulations first
    print("\nStarting sensor simulations...")
    start_script("mqtt_sensor_simulation.py", "MQTT Sensor")
    time.sleep(1)
    start_script("coap_sensor_simulation.py", "CoAP Sensor")
    time.sleep(1)
    start_script("opcua_sensor_simulation.py", "OPC UA Sensor")
    time.sleep(3)  # Give sensors time to initialize
    
    # Then start visualizations
    print("\nStarting visualizations...")
    start_script("mqtt_visualization.py", "MQTT Visualization")
    time.sleep(1)
    start_script("coap_visualization.py", "CoAP Visualization")
    time.sleep(1)
    start_script("opcua_visualization.py", "OPC UA Visualization")
    
    print("\nAll components started!")
    print("Press Ctrl+C to stop all processes\n")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        clean_exit()

if __name__ == "__main__":
    main()