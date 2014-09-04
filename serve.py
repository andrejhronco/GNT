#!/usr/bin/env python

import CGIHTTPServer
import BaseHTTPServer
import sys

if sys.argv[1:]:
    port = int(sys.argv[1])
else:
    port = 8000

server_address = ('', port)

CGIHTTPServer.CGIHTTPRequestHandler.protocol_version = "HTTP/1.0"
CGIHTTPServer.CGIHTTPRequestHandler.cgi_directories = ['/', '/cgi-bin', '/htbin']
httpd = BaseHTTPServer.HTTPServer(server_address, CGIHTTPServer.CGIHTTPRequestHandler)
sa = httpd.socket.getsockname()
print "Serving HTTP on", sa[0], "port", sa[1], "..."
httpd.serve_forever()
