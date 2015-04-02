#!/usr/bin/python
import json
import sys
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

PORT_NUMBER = 8989
redirs = []

class redirHandler(BaseHTTPRequestHandler):

    def send_response(self, code, message=None):
        self.log_request(code)
        if message is None:
            if code in self.responses:
                message = self.responses[code][0]
            else:
                message = ''
        if self.request_version != 'HTTP/0.9':
            self.wfile.write("%s %d %s\r\n" %
                             (self.protocol_version, code, message))
        self.send_header('Date', self.date_time_string())

    def do_GET(self):

        redirFound = False
        for e in redirs:
            if self.path == e['source']:
                self.send_response(e['status'])
                self.send_header('Location', e['target'])
                for hdr_name, hdr_value in e['headers'].items():
                    self.send_header(hdr_name, hdr_value)
                self.end_headers()
                redirFound = True

        if not redirFound:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write("Hello World!")

try:

    json_data = open(sys.argv[1]).read()
    redirs = json.loads(json_data)

    server = HTTPServer(('', PORT_NUMBER), redirHandler)
    print 'Started httpserver on port', PORT_NUMBER

    server.serve_forever()

except KeyboardInterrupt:
    print '^C received, shutting down the web server'
    server.socket.close()
