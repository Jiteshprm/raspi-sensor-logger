#!/usr/bin/python3 -u
from http.server import BaseHTTPRequestHandler,HTTPServer
from subprocess import call

# https://stackoverflow.com/questions/60757496/how-to-run-bash-script-from-nginx

PORT_NUMBER = 8080
autopull = '/opt/raspi-sensor-logger/esp_update_delete/esp_update_delete.sh'
command = [autopull]


# This class will handles any incoming request from
# the browser
class myHandler(BaseHTTPRequestHandler):

    # Handler for the GET requests
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        # Send the html message
        self.wfile.write(("running {}".format(autopull)).encode())
        call(command)
        return


try:
    # Create a web server and define the handler to manage the
    # incoming request
    server = HTTPServer(('', PORT_NUMBER), myHandler)
    print ('Started httpserver on port ' , PORT_NUMBER)

    # Wait forever for incoming http requests
    server.serve_forever()

except KeyboardInterrupt:
    print ('^C received, shutting down the web server')
    server.socket.close()