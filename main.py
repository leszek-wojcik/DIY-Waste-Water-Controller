import gc
import webrepl
import micropython
from html import *
from machine import Timer
import time
import network
import socket
from WWC import WWC
import ure
import btree
import machine
import sys

controller = WWC()
webrepl.start()


def scheduleExp(arg):
    controller.checkControl()
    gc.collect()

def timerExp(arg):
    micropython.schedule(scheduleExp, None)

def machineReset(arg):
    machine.reset()


tim = Timer(-1)
tim.init(period=1000, callback=timerExp)
tim1 = Timer(-1)
tim1.init(period=36000000, callback=machineReset)


datere = ure.compile("\/\?date=(\d\d\d\d)-(\d\d)-(\d\d)" )
timere = ure.compile("\/\?time=(\d\d)\%3A(\d\d)")
controlmethodre = ure.compile("\/\?control_method=(\w*)")
controlre = ure.compile("\/\?control=(\w*)")
reminderre = ure.compile("\/\?reminder=(\d\d\d\d)-(\d\d)-(\d\d)" )


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(1)

while True:

    try:
        conn, addr = s.accept()
        conn.setblocking(True)
        request = conn.recv(512)
        #print(request)

        for i in request.split():

            result = datere.match(i)
            if(result):
                year, month, day, hour, minutes, seconds = controller.rtc.read_datetime()
                year = int( result.group(1))
                month = int( result.group(2))
                day = int(result.group(3))
                controller.rtc.write_datetime (year,month,day,hour,minutes,seconds)
                controller.checkControl()
                break

            result = timere.match(i)
            if(result):
                year, month, day, hour, minutes, seconds = controller.rtc.read_datetime()
                hour = int( result.group(1))
                minutes = int( result.group(2))
                controller.rtc.write_datetime (year,month,day,hour,minutes,0)
                controller.checkControl()
                break

            result = controlmethodre.match(i)
            if(result):
                if (result.group(1) == b'auto'):
                    controller.manual_control = False
                    controller.setAutoSchedule()
                elif (result.group(1) == b'manual'):
                    controller.manual_control = True
                elif (result.group(1) == b'holiday'):
                    controller.manual_control = False
                    controller.setHolidaySchedule()
                controller.checkControl()
                break

            result = controlre.match(i)
            if(result):
                if(result.group(1) == b'circulation'):
                    controller.manual_circulation = not controller.manual_circulation
                if(result.group(1) == b'areation'):
                    controller.manual_areation = not controller.manual_areation
                controller.checkControl()
                break

            result = reminderre.match(i)
            if(result):
                controller.db["year"] = result.group(1)
                controller.db["month"] = result.group(2)
                controller.db["day"] = result.group(3)
                controller.db.flush()
                controller.checkControl()
                break
    

        conn.write(html_head)
        conn.write(html_left_column_head)
        conn.write(html_left_column_manual_control % controller.getControl())
        conn.write(html_left_column_areation % controller.getAreation())
        conn.write(html_left_column_circulation % controller.getCirculation())
        conn.write(html_left_column_controller_time % str(controller.rtc.read_datetime()))
        conn.write(html_left_column_controller_temperature % controller.dht12.temperature())
        conn.write(html_left_column_controller_humidity % controller.dht12.humidity())
        conn.write(html_left_column_service_reminder % controller.calculateServiceTime() )
        conn.write(html_left_column_end)
        conn.write(html_right_column_head)
        conn.write(html_right_column_time)
        conn.write(html_right_column_reminder)
        conn.write(html_right_column_control_head)
        conn.write(html_right_column_control_form)
        conn.write(html_right_column_about)
        conn.write(html_footer)
        conn.close()
    except KeyboardInterrupt:
        print ("stopping program and timers")
        tim.deinit()
        tim1.deinit()
        sys.exit(0)
    except OSError:
        print ("OSError")
        conn.close()

    gc.collect()
    micropython.mem_info()


