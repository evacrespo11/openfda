##
# WEB SERVER
##

''''Dentro del fichero web2mod cogemos la class testHTTPRequestHandler'''

import socketserver

import buscardrug2

PORT=8011





Handler = buscardrug2.testHTTPRequestHandler
httpd = socketserver.TCPServer(("", PORT), Handler)
print("serving at port", PORT)
httpd.serve_forever()
