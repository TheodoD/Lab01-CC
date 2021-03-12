from http.server import HTTPServer, BaseHTTPRequestHandler
import json

# open json file and give it to data variable as a dictionary
from urllib.parse import parse_qs, urlparse

with open("db.json") as data_file:
    data = json.load(data_file)


# Defining a HTTP request Handler class
class ServiceHandler(BaseHTTPRequestHandler):
    def do_GET(self):

        length = int(self.headers['Content-Length'])
        content = self.rfile.read(length)
        temp = json.loads(content.decode())

        ok = 0

        for x in data:
            if temp['ser'] in x:
                self.send_response(200)
                self.send_header("Content-type", "JSON")
                self.end_headers()
                self.wfile.write(json.dumps(data[x]).encode())
                ok = 1

        if ok == 0:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(json.dumps("Id not found").encode())







    def do_POST(self):
        length = int(self.headers['Content-Length'])
        content = self.rfile.read(length)
        temp = json.loads(content.decode())

        for i in temp:
            if not temp[i].isalpha():
                self.send_response(400)
                self.end_headers()
                self.wfile.write(json.dumps("Names should contain only letters").encode())
                return


        key = 0
        # getting key and value of the data dictionary
        for key, value in data.items():
            pass
        index = int(key) + 1
        data[str(index)] = str(temp)
        # write the changes to the json file
        with open("db.json", 'w+') as file_data:
            json.dump(data, file_data)

        self.send_response(200)
        self.send_header("Content-type", "JSON")
        self.end_headers()
        self.wfile.write(json.dumps("Oke").encode())



    def do_PUT(self):
        length = int(self.headers['Content-Length'])
        content = self.rfile.read(length)
        temp = json.loads(content.decode())

        # check if key is in data
        for x in temp:
            if x in data:
                data[x] = temp[x]
                # write the changes to file
                with open("db.json", 'w+') as file_data:
                    json.dump(data, file_data)

                self.send_response(200)
                self.send_header("Content-type", "JSON")
                self.end_headers()
                self.wfile.write(json.dumps("Oke").encode())
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(json.dumps("Id not found").encode())

    def do_DELETE(self):
        length = int(self.headers['Content-Length'])
        content = self.rfile.read(length)
        temp = json.loads(content.decode())
        print(temp)

        ok = 0
        for x in data:
            if temp['ser'] in x:
                ok = 1
                del data[x]
                with open("db.json", 'w+') as file_data:
                    json.dump(data, file_data)
                self.send_response(200)
                self.send_header("Content-type", "JSON")
                self.end_headers()
                self.wfile.write(json.dumps("Oke").encode())

        if ok == 0:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(json.dumps("Id not found").encode())


# Server Initialization
server = HTTPServer(('127.0.0.1', 8080), ServiceHandler)
server.serve_forever()