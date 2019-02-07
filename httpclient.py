#!/usr/bin/env python3
# coding: utf-8
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
import urllib.parse

def help():
    print("httpclient.py [GET/POST] [URL]\n")

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body
    
    def __str__(self):
        return self.body

class HTTPClient(object):
    #def get_host_port(self,url):

    def connect(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        return None

    def get_code(self, data):
        return None

    def get_headers(self,data):
        return None

    def get_body(self, data):
        return None
    
    def sendall(self, data):
        self.socket.sendall(data.encode('utf-8'))
        
    def close(self):
        self.socket.close()

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return buffer.decode('utf-8', 'ignore')

    def GET(self, url, args=None):
        # Must create the get request here at the target URL

        # Compose the GET Request
        # GET / HTTP/1.1
        # Host: google.com
        # User-Agent: curl/7.47.0
        # Accept: */*

        # print(args, url)

        parsed = urllib.parse.urlparse(url)
        path = parsed.path
        if path == "":
            path = "/"
        request = "GET " + path + " HTTP/1.1\n"

        # should this be parse.netloc or parsed.hostname
        host ="Host: " + parsed.hostname + "\n"
        
        # If no port given use the default port
        port = parsed.port
        if port == None:
            port = 80

        # We can say whatever we want for this I guess lol, could we spoof chrome so we dont get blocked? is that even allowed?
        userAgent = "User-Agent: benWebClientAssignment\n"

        # Accept, anything special needed here?
        accept = "Accept: */*\n"
        
        # Close the connection
        close = "Connection: close\n\r\n"

        # Format our request
        body = request + host + userAgent + accept + close
        
        # Connect to the host, send body, recieve response
        self.connect(parsed.hostname, port)
        self.sendall(body)
        response = self.recvall(self.socket)
        self.close()

        # We want to return the HTTP response from the server
        # We want this response to be formatted as an HTTPResponse object
        # So we should format it here
        response = response.splitlines()
        code = int(response[0].split()[1])
        
        # So the body is everything after the first empty line, ""
        index = response.index("")
        body = "".join(response[index+1:])

        # Body is everything after the headers
        return HTTPResponse(code,body)

    def POST(self, url, args=None):
        # Must create the get request here at the target URL

        # Compose the POST Request
        # POST / HTTP/1.1
        # Host: google.com
        # User-Agent: curl/7.47.0
        # Accept: */*
        #
        #name=ben&hair=brown

        # Must be able to post variables

        parsed = urllib.parse.urlparse(url)

        path = parsed.path
        if path == "":
            path = "/"
        request = "POST " + path + " HTTP/1.1\n"

        # should this be parse.netloc or parsed.hostname
        host ="Host: " + parsed.hostname + "\n"

        contentType = "Content-Type: application/x-www-form-urlencoded\n"
        
        # If no port given use the default port
        port = parsed.port
        if port == None:
            port = 80

        # We can say whatever we want for this I guess lol, could we spoof chrome so we dont get blocked? is that even allowed?
        userAgent = "User-Agent: benWebClientAssignment\n"

        # Accept, anything special needed here?
        accept = "Accept: */*\n"
        
        # Close the connection
        # Will this have negative consequences regarding the post request?
        close = "Connection: close\n\r\n"

        # Content is the args, so the single string form information input
        # Should this be utf8 encoded? I dont think its necessary
        # If args is None, so no content
        if args == None:
            args = ""

        # If args is a dict, not a string, we must convert to query format
        # encode invalid characters? %5Cn%5Cr
        if type(args) is dict:
            content = urllib.parse.urlencode(args)

        # Else it is a string, otherwise we are gonna crash, can only handle strings and dicts
        else:
            content = args

        # contentLength = "Content-Length: 0\n"
        # if args != None:
        contentLength = "Content-Length: " + str(len(content)) + "\n"

        # Format our request
        # print(request, host, contentType, contentLength, userAgent, accept, close, content)
        body = request + host + contentType + contentLength + userAgent + accept + close + content    

        # Connect to the host, send body, recieve response
        self.connect(parsed.hostname, port)
        self.sendall(body)
        response = self.recvall(self.socket)
        self.close()
        # print(response)

        # We want to return the HTTP response from the server
        # We want this response to be formatted as an HTTPResponse object
        # So we should format it here
        response = response.splitlines()
        code = int(response[0].split()[1])

        # So the body is everything after the first empty line, ""
        index = response.index("")
        body = "".join(response[index+1:])

        # Body is everything after the headers
        return HTTPResponse(code,body)

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            # Get the arguments in here
            if args == None:
                args = urllib.parse.urlparse(url).query
            return self.POST( url, args )
        else:
            return self.GET( url, args )
    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print(client.command( sys.argv[2], sys.argv[1] ))
    else:
        print(client.command( sys.argv[1] ))
