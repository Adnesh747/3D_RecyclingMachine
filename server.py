import SimpleHTTPServer
import SocketServer
import socket
import urlparse
import time
import threading

# Global variables to store the last values
last_values = {
    'GrinderSpeed': 0,
    'ExtruderTemp': 180,
    'HeatingTemp': 200,
    'AugerSpeed': 0,
    'GrinderPower': 'off',
    'HeatingPower': 'off',
    'Error': 'Machine is off',
    'ActualElementTemp': 180,
    'ActualExtruderTemp': 200,
    'MachineStatus':3,
    'AutoMode': 'off'
}

# Define the HTML content template
html_template = """<!DOCTYPE html>
<html>
<head><title>Raspberry Pi HTTP Server</title></head>
<body>
<h1>Raspberry Pi HTTP Server</h1>
<p>Hello, World!</p>
<p>Last Values:</p>
<ul>
<li>Grinder Speed: {}</li>
<li>Extruder Temp: {}</li>
<li>Heating Temp: {}</li>
<li>Auger Speed: {}</li>
<li>Grinder Power: {}</li>
<li>Heating Power: {}</li>
<li>Error: {}</li>
<li>Actual Element Temp: {}</li>
<li>Actual Extruder Temp: {}</li>
<li>MachineStatus: {}</li>
<li>AutoMode: {}</li>
</ul>
</body>
</html>"""

# Define the custom request handler
class MyRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_GET(self):
        global last_values  # Access the global variable

        # Parse the query parameters from the URL
        parsed_url = urlparse.urlparse(self.path)
        query_params = urlparse.parse_qs(parsed_url.query)

        # Update the last values
        for key, value in query_params.iteritems():
            if key in last_values:
                last_values[key] = value[0]

        # Generate the HTML content with the last values
        html_content = html_template.format(
            last_values['GrinderSpeed'],
            last_values['ExtruderTemp'],
            last_values['HeatingTemp'],
            last_values['AugerSpeed'],
            last_values['GrinderPower'],
            last_values['HeatingPower'],
            last_values['Error'],
            last_values['ActualElementTemp'],
            last_values['ActualExtruderTemp'],
            last_values['MachineStatus'],
            last_values['AutoMode']
        )

        # Send the HTTP response
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(html_content)

# Function to write grinder speed to a file
def write_grinder_speed(id):
    try:
        with open("/home/pi/grinderspeed", "w") as f:
            f.write(str(id))
    except Exception as e:
        print("Failed to write grinder speed:", e)
def write_grinderon(id):
    try:
        with open("/home/pi/grinderon","w") as f:
            f.write(str(id))
    except Exception as e:
        print("Failed to write grinder on:",e)

def write_ExtruderTemp(id):
    try:
        with open("/home/pi/ExtruderTemp","w") as f:
            f.write(str(id))
    except Exception as e:
        print("Failed to write ExtruderTemp:",e)
def write_HeatingTemp(id):
    try:
        with open("/home/pi/HeatingTemp","w") as f:
            f.write(str(id))
    except Exception as e:
        print("Failed to write HeatingTemp:",e)
def write_AugerSpeed(id):
    try:
        with open("/home/pi/AugerSpeed","w") as f:
            f.write(str(id))
    except Exception as e:
        print("Failed to write AugerSpeed:",e)
def write_HeatingPower(id):
    try:
        with open("/home/pi/HeatingPower","w") as f:
            f.write(str(id))
    except Exception as e:
        print("Failed to write HeatingPower:",e)
def read_error():
   try:
        f = open("/home/pi/errormess","r")
        id = f.read()
        f.close()
   except:
        id = "0"
   return id
def read_ActualElementTemp():
   try:
        f = open("/home/pi/ActualElementTemp","r")
        id = f.read()
        f.close()
   except:
        id = "0"
   return id
def read_ActualExtruderTemp():
   try:
        f = open("/home/pi/ActualExtruderTemp","r")
        id = f.read()
        f.close()
   except:
        id = "0"
   return id
def write_automode(id):
    try:
        with open("/home/pi/automode","w") as f:
            f.write(str(id))
    except Exception as e:
        print("Failed to write Automode:",e)
# Function to periodically call write_grinder_speed with the current GrinderSpeed
def periodic_task():
    while True:
        write_grinderon(last_values['GrinderPower'])
        write_HeatingPower(last_values['HeatingPower'])
        write_automode(last_values['AutoMode'])
        if (str(last_values['AutoMode']) == "off"):
            write_ExtruderTemp(last_values['ExtruderTemp'])
            write_HeatingTemp(last_values['HeatingTemp'])
            write_AugerSpeed(last_values['AugerSpeed'])
            write_grinder_speed(last_values['GrinderSpeed'])

        last_values['Error'] = read_error()
        last_values['ActualElementTemp'] = read_ActualElementTemp()
        last_values['ActualExtruderTemp'] = read_ActualExtruderTemp()
        time.sleep(0.5)  # Sleep for half a second

# Set up the HTTP server
PORT = 8000
httpd = SocketServer.TCPServer(("", PORT), MyRequestHandler)
print("Server running at http://localhost:{}/".format(PORT))

# Start the server
server_thread = threading.Thread(target=httpd.serve_forever)
server_thread.daemon = True
server_thread.start()

# Start the periodic task
periodic_thread = threading.Thread(target=periodic_task)
periodic_thread.daemon = True
periodic_thread.start()

# Wait for the server to be stopped
try:
    while True:
        time.sleep(0.1)
except KeyboardInterrupt:
    print("Server stopped")
    httpd.shutdown()
    httpd.server_close()
