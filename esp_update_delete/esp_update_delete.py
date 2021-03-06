#!/usr/bin/python3 -u
from http.server import BaseHTTPRequestHandler,HTTPServer
from subprocess import call
import os

# https://stackoverflow.com/questions/60757496/how-to-run-bash-script-from-nginx

PORT_NUMBER = 8080
autopull = '/opt/raspi-sensor-logger/esp_update_delete/esp_update_delete.sh'
command = [autopull]
sketch_update_file_path='/home/birdofprey/esp8266/OutdoorWeatherStation.ino.esp8285.bin'


# This class will handles any incoming request from
# the browser
class myHandler(BaseHTTPRequestHandler):

    # Handler for the GET requests
    def do_GET(self):
        try:
            if self.path.endswith(".bin"):
                print ('Sending: ', self.path)
                file_size = os.stat(sketch_update_file_path).st_size
                print ('File Size: ', file_size)
                f = open(sketch_update_file_path, 'rb')
                self.send_response(200)
                self.send_header('Content-Type', 'text/plain')
                self.send_header('Content-Length', file_size)
                self.end_headers()
                # Send the html message
                print ('Writing Content...')
                self.wfile.write(f.read())
                print ('Closing File...')
                f.close()
                print ('Deleting File...')
                # call(command)
                os.remove(sketch_update_file_path)
                return
            else:
                print ('Error, File Not Found 404: ', self.path)
                self.send_error(404, 'File Not Found: %s' % self.path)
        except IOError:
            print ('Error, File Not Found 404: ', self.path)
            self.send_error(404, 'File Not Found: %s' % self.path)


class TimeoutingHTTPServer(HTTPServer):
    def finish_request(self, request, client_address):
        request.settimeout(10)  # Really short timeout as there is only 1 thread
        HTTPServer.finish_request(self, request, client_address)


try:
    # Create a web server and define the handler to manage the
    # incoming request
    server = TimeoutingHTTPServer(('', PORT_NUMBER), myHandler)
    print ('Started http server on port ', PORT_NUMBER)

    # Wait forever for incoming http requests
    server.serve_forever()

except KeyboardInterrupt:
    print ('^C received, shutting down the web server')
    server.socket.close()
