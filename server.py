#  coding: utf-8 
import SocketServer
import os.path


# Copyright 2013 Abram Hindle, Eddie Antonio Santos
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
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(SocketServer.BaseRequestHandler):
    
    def handle(self):

        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)
        
        
        find = self.data.split()
        
	print (find)        

#        request = find[0]
        
        URL = find[1]
        
        self.check_URL(URL)


    def check_URL(self, URL):

        
        path = "www" + URL


        if os.path.isdir(path) or os.path.exists(path):
            
            
            if os.path.isfile(path):
                
                print ("TEST: " + URL)
            
            
                content, type = self.read_file(path)
                self.request.sendall("HTTP/1.1 "+"200 " +"OK\n"+ "Content-Type: "+ type + "\n\n"+content)
            
            

                
            elif path.endswith("/"):

                new_path = path + "index.html"
                
                print ("HERE")
                
                print (URL)
                
                content, type = self.read_file(new_path)
                        
                self.request.sendall("HTTP/1.1 "+"200 " +"OK\n"+ "Content-Type: "+type + "\n\n"+content)
            

            else:
                
                self.request.sendall("HTTP/1.1 404 Not Found\n" + "Content-Type: text/plain\n"+"\n\n"+"Error 404, Page Not Found")


        else:
            self.request.sendall("HTTP/1.1 404 Not Found\n" + "Content-Type: text/plain\n"+"\n\n"+"Error 404, Page Not Found")



    def read_file(self, path):
        try:
            
            open_file = open(path,"rb")
            contains = open_file.read()
            open_file.close()

        except IOError:
            return -1
        
        
        
        
        if path.endswith(".css"):
        
            correct_mimtype = "text/css"

        if path.endswith(".html"):
            correct_mimtype = "text/html"

        print("WHAT TYPE: "+ correct_mimtype)

        return contains, correct_mimtype


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
