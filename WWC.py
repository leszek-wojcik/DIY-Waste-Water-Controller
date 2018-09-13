from machine import Pin, I2C, Timer
import time
import network
import socket
from DHT12 import DHT12
from DS1302 import DS1302
from html import html
import ure
import micropython
import btree
import machine


class WWC:
    def __init__(self):
        print ("WWC initialization")
        self.d3 = Pin(0, Pin.OUT)
        self.d4 = Pin(2, Pin.OUT)
        self.d3.off()
        self.d4.off()

        self.manual_control = False;
        self.manual_circulation = False;
        self.manual_areation = False;

        self.initNetwork()
        self.initDht()
        self.initRTC()
        self.initDatabase()
        

    def initNetwork(self):
        print ("network initialization")
        self.sta_if =  network.WLAN(network.STA_IF)
        self.sta_if.active(True)
        self.sta_if.connect("fcukgoogl","mostadvancedsec")
        print(self.sta_if.ifconfig())


    def initDht(self):
        print ("dht12 initialization")
        self.i2c = I2C(scl=Pin(5), sda=Pin(4), freq=100000)
        self.dht12 = DHT12(self.i2c)
        self.dht12.measure()
        print (self.dht12.temperature())
        print (self.dht12.humidity())


    def initRTC(self):
        print ("RTC intialization")
        self.rtc = DS1302()
        print(self.rtc.read_datetime())


    def initDatabase(self):        
        print ("Database initialization")
        try:
            f = open("mydb", "r+b")
        except OSError:
            f = open("mydb", "w+b")

        self.db = btree.open(f)

        self.areation_schedule = [  ("7:40","23:59"), 
                          ("21:00","21:05") ]

        self.circulation_schedule = [("7:41","20:20"), 
                          ("21:00","21:45") ]


    def checkControl(self):
        year, month, day, hour, minutes, seconds = self.rtc.read_datetime()
        curtime = time.mktime( (year, month, day, hour, minutes, seconds, None, None))

        areation_enable = False
        circulation_enable = False

        for begin, end in self.areation_schedule:
            begin = time.mktime ( 
                (year,month,day , int(begin.split(':')[0]), int(begin.split(':')[1]), 0, None, None))
            end = time.mktime ( 
                (year,month,day , int(end.split(':')[0]), int(end.split(':')[1]), 0, None, None))

            if begin < curtime < end:
                areation_enable = True

        for begin, end in self.circulation_schedule:
            begin = time.mktime ( 
                (year,month,day , int(begin.split(':')[0]), int(begin.split(':')[1]), 0, None, None))
            end = time.mktime ( 
                (year,month,day , int(end.split(':')[0]), int(end.split(':')[1]), 0, None, None))

            if begin < curtime < end:
                circulation_enable = True


        # Measure temperature and humidity
        self.dht12.measure()
        
        if (self.manual_control == False):
            if (areation_enable):
                self.d3.on()
            else:
                self.d3.off()

            if (circulation_enable):
                self.d4.on()
            else:
                self.d4.off()

        else:
            if (self.manual_areation):
                self.d3.on()
            else:
                self.d3.off()

            if (self.manual_circulation):
                self.d4.on()
            else:
                self.d4.off()


    def calculateServiceTime(self):
        try:
            year = int(self.db["year"].decode("ascii"))
            month = int(self.db["month"].decode("ascii"))
            day = int(self.db["day"].decode("ascii"))
        except KeyError:
            return "N/A"

        end = time.mktime((year,month,day,0,0,0,None,None))
        year, month, day, hour, minutes, seconds = self.rtc.read_datetime()
        curtime = time.mktime( (year, month, day, hour, minutes, seconds, None, None))

        if (end - curtime) < 0:
            return "Overdue"
        else:
            return str(round( (end - curtime)/86400)) + " days"
