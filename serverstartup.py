import subprocess
import time
import signal

def check_wifi():
    while True:
        # Run the ping command to check network connectivity
        result = subprocess.call(["ping", "-c", "1", "8.8.8.8"])
        if result == 0:
            return True  # WiFi is connected
        else:
            print("WiFi not connected. Retrying in 3 seconds...")
            time.sleep(3)

# Function to handle KeyboardInterrupt and stop the server
def stop_server():
    print("Stopping server...")
    server_process.terminate()
    kill_command = "sudo lsof -t -i:8000 | xargs kill -9"
    server_process.wait()  # Wait for the server process to finish
    print("Server stopped.")
    # Kill the process listening on port 8000
    subprocess.run(kill_command, shell=True)
    exit(0)

# Check WiFi connection before proceeding
if check_wifi():
    print("WiFi is connected!")

    # Define the command to start the server
    server_command = "python2.7 ~/app/server.py"

    # Define the command to run after 2 seconds
    telebit_command = "~/telebit http 8000"

    # Define the command to kill the process listening on port 8000
    kill_command = "sudo lsof -t -i:8000 | xargs kill -9"

    # Run the server command
    server_process = subprocess.Popen(server_command, shell=True)

    # Set up signal handler for KeyboardInterrupt
    signal.signal(signal.SIGINT, stop_server)

# Wait for 2 seconds
    time.sleep(1)

        # Run the telebit command
    telebit_process = subprocess.Popen(telebit_command, shell=True)

        # Wait for the telebit command to finish (optional)
    telebit_process.wait()
    try:
      while True:
         pass
    except KeyboardInterrupt:
      print("Stopping server...")
      server_process.terminate()
      kill_command = "sudo lsof -t -i:8000 | xargs kill -9"
      server_process.wait()  # Wait for the server process to finish
      print("Server stopped.")
    # Kill the process listening on port 8000
      subprocess.run(kill_command, shell=True)
      exit(0)
else:
    print("WiFi is not connected.")
