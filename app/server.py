# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer
from sys import version as python_version
from cgi import parse_header, parse_multipart
from urllib.parse import parse_qs
import time
import sys
import json
import locale
import os
import base64
from datetime import date, datetime

def fileToString(fileName) :
    fileContents = ""
    with open(fileName, 'r') as myfile:
        fileContents = myfile.read()
    return fileContents

def fileToBytes(fileName) :
    with open(fileName, 'rb') as myfile:
        fileContents = myfile.read()
    return fileContents

def getMasthead(server_name, path) :
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    pageContent = fileToString("masthead-p1.html")
    pageContent = pageContent + "https://" + str(server_name) + path
    pageContent = pageContent + fileToString("masthead-p2.html")
    return pageContent

def getPageContent(path) :
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    pageContent = fileToString("page.body.html")
    return pageContent

class APIEndPoint:
    method = ""
    getParams = {}
    postParams = {}
    path = ""
    server = ""
    
def getParamsFromPath(path) :
    getParamsDict = {}
    if "?" in path:
        pathSplit = path.split("?", 1)
        print(str(pathSplit))
        if "&" in pathSplit[1]:
            paramsRaw = pathSplit[1].split("&")
            for pRaw in paramsRaw:
                pSplit = pRaw.split("=")
                if len(pSplit) == 2:
                    getParamsDict[str(pSplit[0])] = str(pSplit[1])
        elif "=" in pathSplit[1]:
            pSplit = pathSplit[1].split("=")
            if len(pSplit) == 2:
                getParamsDict[str(pSplit[0])] = str(pSplit[1])
    return getParamsDict

def dictToParagraph(dictionary, title) :
    pString = "<p>" + title + "<br /><ul>"
    for key in dictionary:
        pString = pString + "<li>" + str(key) + ": " + str(dictionary[key]) + "</li>"
    pString = pString + "</ul></p>"
    return pString

def validMediaFile(path) :
    valid = False
    fileString = True
    fileType = ""
    contentType = ""
    byteTypes = [".jpg", ".ico", ".eot", ".ttf", ".woff", ".woff2"]
    validTyes = {
        ".css": "text/css",
        ".css.map": "text/css",
        ".js": "application/javascript", 
        ".js.map": "application/javascript", 
        ".min.map": "application/javascript",
        ".ico": "image/ico",
        ".jpg": "image/jpeg",
        ".eot": "application/vnd.ms-fontobject",
        ".ttf": "application/x-font-ttf",
        ".woff": "application/font-woff",
        ".woff2": "application/font-woff2",
        ".svg": "image/svg+xml"
    }
    for ft, ct in validTyes.items():
        negcharcount = len(ft) * -1
        if valid == False:
            if path[negcharcount:] == ft:
                fileType = ft
                contentType = ct
                valid = True
    if fileType in byteTypes:
        fileString = False
    if valid:
        print(path + " is a valid " + fileType + " file. " + contentType)
    else:
        print(path + " is not a valid mediafile")
    return [valid, fileType, contentType, fileString]

serverPort = 8080

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.respond("GET")
    def do_POST(self):
        self.respond("POST")
    def respond(self, method):
        endpoint = APIEndPoint()
        endpoint.method = method
        endpoint.path = self.path.split("?")[0]
        endpoint.server = os.environ["FQDN"]
        endpoint.getParams = {}
        endpoint.postParams = {}
        mediacheck = validMediaFile(endpoint.path)
        mediafile = mediacheck[0]
        mediafileType = mediacheck[1]
        mediafileContentType = mediacheck[2]
        mediafileString = mediacheck[3]
        if mediafile:
            filepath = endpoint.path[1:]
            try:
                if mediafileString:
                    fileContents = fileToString(filepath)
                else:
                    fileBytes = fileToBytes(filepath)
                self.send_response(200)
                self.send_header("Content-type", mediafileContentType)
                self.end_headers()
                if mediafileString:
                    self.wfile.write(bytes(fileContents, encoding="utf8"))
                else:
                    self.wfile.write(fileBytes)
            except:
                self.send_response(400)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                # Time to build the actual webpage. First start off with the opening tag
                self.wfile.write(bytes("<!DOCTYPE html><html lang=\"en\">", "utf-8"))
                # Next pull in the <head> tag from our handy head.html file.
                #self.wfile.write(bytes(fileToString("head.html"), "utf-8"))
                #Begin the html body
                self.wfile.write(bytes("<body>Oops</body></html>", "utf-8"))
        else:
            print("Trying to build " + endpoint.path + " as an html page. After " + endpoint.method + " request.")
            endpoint.getParams = getParamsFromPath(self.path)
            if endpoint.method == "POST":
                ctype, pdict = parse_header(self.headers['content-type'])
                if ctype == 'multipart/form-data':
                    postvars = parse_multipart(self.rfile, pdict)
                elif ctype == 'application/x-www-form-urlencoded':
                    length = int(self.headers['content-length'])
                    postvars = parse_qs(
                            self.rfile.read(length), keep_blank_values=1)
                else:
                    postvars = {}
                if len(postvars) > 0:
                    for key in postvars.keys():
                        pvlist = postvars[key]
                        if len(pvlist) == 1:
                            endpoint.postParams[key.decode("utf-8")] = postvars[key][0].decode("utf-8")
                        else:
                            pvstringlist = []
                            for pv in postvars[key]:
                                pvstringlist.append(pv.decode("utf-8"))
                            endpoint.postParams[key.decode("utf-8")] = pvstringlist
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            # Time to build the actual webpage. First start off with the opening tag
            self.wfile.write(bytes("<!DOCTYPE html><html lang=\"en\">", "utf-8"))
            # Next pull in the <head> tag from our handy head.html file.
            self.wfile.write(bytes(fileToString("head.html"), "utf-8"))
            #Begin the html body
            self.wfile.write(bytes("<body>", "utf-8"))
            #Page navigation
            self.wfile.write(bytes(getMasthead(os.environ["FQDN"], endpoint.path), "utf-8"))
            #Page content
            #self.wfile.write(bytes(getPageContent(self.path), "utf-8"))
            self.wfile.write(bytes(fileToString("page.body.top.html"), "utf-8"))
            self.wfile.write(bytes("<p>This is some page content. Below is all the info about your request</p>", "utf-8"))
            self.wfile.write(bytes("<h3>Headers</h3>", "utf-8"))
            self.wfile.write(bytes(dictToParagraph(self.headers, "Request Headers"), "utf-8"))
            self.wfile.write(bytes("<h3>Parameters</h3>", "utf-8"))
            self.wfile.write(bytes(dictToParagraph(endpoint.getParams, "GET Parameters"), "utf-8"))
            self.wfile.write(bytes(dictToParagraph(endpoint.postParams, "POST Parameters"), "utf-8"))
            self.wfile.write(bytes(fileToString("page.body.bottom.html"), "utf-8"))
            #Page footer
            self.wfile.write(bytes("<hr>", "utf-8"))
            self.wfile.write(bytes(fileToString("footer.html"), "utf-8"))
            self.wfile.write(bytes("</body></html>", "utf-8"))
            #Done :)

if __name__ == "__main__":        
    webServer = HTTPServer(("", serverPort), MyServer)
    print("Server started http://localhost:%s" % (serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
