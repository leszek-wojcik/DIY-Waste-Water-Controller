from machine import Pin, I2C, Timer
import time
import network
import socket
from DHT12 import DHT12
from DS1302 import DS1302
from html import html
from WWC import WWC
import ure
import micropython
import btree
import machine

controller = WWC()

def scheduleExp(arg):
    controller.checkControl()

def timerExp(arg):
    micropython.schedule(scheduleExp, None)


tim = Timer(-1)
tim.init(period=5000, callback=timerExp)

datere = ure.compile("\/\?date=(\d\d\d\d)-(\d\d)-(\d\d)" )
timere = ure.compile("\/\?time=(\d\d)\%3A(\d\d)")
controlmethodre = ure.compile("\/\?control_method=(\w*)")
controlre = ure.compile("\/\?control=(\w*)")
reminderre = ure.compile("\/\?reminder=(\d\d\d\d)-(\d\d)-(\d\d)" )

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

while True:

    conn, addr = s.accept()
    conn.setblocking(True)
    print("Got a connection from %s" % str(addr))
    request = conn.recv(1024)
    print(request)


    for i in request.split():
        result = datere.match(i)
        if(result):
            print("found date")
            year, month, day, hour, minutes, seconds = controller.rtc.read_datetime()
            year = int( result.group(1))
            month = int( result.group(2))
            day = int(result.group(3))
            controller.rtc.write_datetime (year,month,day,hour,minutes,seconds)
            break

        result = timere.match(i)
        if(result):
            print("found time")
            print(result.group(1))
            print(result.group(2))
            year, month, day, hour, minutes, seconds = controller.rtc.read_datetime()
            hour = int( result.group(1))
            minutes = int( result.group(2))
            controller.rtc.write_datetime (year,month,day,hour,minutes,0)
            break

        result = controlmethodre.match(i)
        if(result):
            print("found control_method")
            print(controller.manual_control)
            if (result.group(1) == b'auto'):
                controller.manual_control = False
            elif (result.group(1) == b'manual'):
                controller.manual_control = True
            break

        result = controlre.match(i)
        if(result):
            print("found control")
            if(result.group(1) == b'circulation'):
                controller.manual_circulation = not controller.manual_circulation
            if(result.group(1) == b'areation'):
                controller.manual_areation = not controller.manual_areation
            break

        result = reminderre.match(i)
        if(result):
            print("found reminder")
            controller.db["year"] = result.group(1)
            controller.db["month"] = result.group(2)
            controller.db["day"] = result.group(3)
            controller.db.flush()
            break
    

    response = html % (str(controller.manual_control), str(controller.d3.value()), str(controller.d4.value()), str(controller.rtc.read_datetime()), controller.dht12.temperature(), controller.dht12.humidity(), controller.calculateServiceTime()  ) 


    try:
        conn.write(response)
    except OSError:
        machine.reset()

    conn.close()


