#!/usr/bin/python
import os
import time
import urllib2
import json

clients = ["10.0.0.125", "10.0.0.119"]
file = "/var/log/cidcall.log"


def format_number(number):
    if len(number) >= 9:
        fnum = str(number[0:3]) +\
            "-" + number[3:6] +\
            "-" + number[6:]
        return fnum
    else:
        return number

def notify_kodi(name, number):

    message = "{} {}".format(name, format_number(number))
    data = {'params': {'message': message, 'title': 'Call From:'}, 'jsonrpc': '2.0', 'id': 1, 'method': 'GUI.ShowNotification'}

    for client in clients:
        try:
            url = "http://" + client + ":8080/jsonrpc"
            req = urllib2.Request(url)
            req.add_header('Content-Type', 'application/json')
            #print
            urllib2.urlopen(req, json.dumps(data))

            #now send a Sonos notification
            sonos_url = "http://10.0.0.120:5005/Family Room/sayall/Incoming Call from {}/en-us/25".format(message)
            print sonos_url
            urllib2.urlopen(sonos_url)

        except:
            print "error: ", client

mod_time = os.path.getmtime(file)

while True:
    if mod_time < os.path.getmtime(file):
        mod_time = os.path.getmtime(file)

        logfile = open(file, "r")
        logfile_c = logfile.read()

        last_line = logfile_c.count("\n")
        lines = logfile_c.split("\n")

        new_call = lines[last_line - 1]
        print new_call

        new_call_items = new_call.split("*")
        print new_call_items
        name = "unknown"
        number = "unknown"

        for index, item in enumerate(new_call_items):
            if item == "NMBR":
                number = new_call_items[index + 1]
            if item == "NAME":
                name = new_call_items[index + 1]
        notify_kodi(name, number)
        time.sleep(10)
    time.sleep(3)
