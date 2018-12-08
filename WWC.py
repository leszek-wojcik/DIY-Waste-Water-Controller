import gc
from machine import Pin, I2C, Timer
import time
import network
from DHT12 import DHT12
from DS1307 import DS1307
import btree
import machine


class WWC:
    def __init__(self):
        print ("WWC initialization")
        self.d3 = Pin(0, Pin.OUT)
        self.d4 = Pin(2, Pin.OUT)

        self.i2c = I2C(scl=Pin(5), sda=Pin(4), freq=100000)

        self.manual_control = False;
        self.manual_circulation = False;
        self.manual_areation = False;

        self.initDatabase()
        self.initNetwork()
        self.initDht()
        self.initRTC()

    def enableCirculation(self):
        self.d4.on()

    def disableCirculation(self):
        self.d4.off()

    def getCirculation(self):
        return bool(self.d4.value())
    
    def enableAreation(self):
        self.d3.off()

    def disableAreation(self):
        self.d3.on()

    def getAreation(self):
        return not bool(self.d3.value())


    def initNetwork(self):
        print ("network initialization")
        self.sta_if =  network.WLAN(network.STA_IF)
        self.sta_if.active(True)
        self.sta_if.connect("fcukgoogl","hypersecpass")
        time.sleep(5) 
        print(self.sta_if.ifconfig())
#        self.ap_if = network.WLAN(network.AP_IF)
#        self.ap_if.config(essid='DIY_WWC', authmode=network.AUTH_WPA_WPA2_PSK, password="hypersecpass")
#        time.sleep(5) 
#        print(self.ap_if.ifconfig())

    def initDht(self):
        print ("dht12 initialization")
        self.dht12 = DHT12(self.i2c)
        self.dht12.measure()
        print (self.dht12.temperature())
        print (self.dht12.humidity())


    def initRTC(self):
        print ("RTC intialization")
        self.rtc = DS1307(self.i2c)
        print(self.rtc.read_datetime())


    def setAutoSchedule(self):
        print("Auto schedule")
        self.currentAreationSchedule = [ ("00:00","01:30"), 
                                         ("02:00","03:30"),
                                         ("04:00","05:30"),
                                         ("06:00","07:30"),
                                         ("08:00","09:30"),
                                         ("10:00","11:30"),
                                         ("12:00","13:30"),
                                         ("14:00","15:30"),
                                         ("16:00","17:30"),
                                         ("18:00","19:30"),
                                         ("20:00","21:30"),
                                         ("22:00","23:30") ]

        self.currentCirculationSchedule = [("23:40","23:55")]
        self.db["sched"] = b"auto"
        self.db.flush()

    def setHolidaySchedule(self):
        print("Holiday schedule")
        self.currentAreationSchedule = [ ("00:00","01:00"), 
                                         ("02:00","03:00"),
                                         ("04:00","05:00"),
                                         ("06:00","07:00"),
                                         ("08:00","09:00"),
                                         ("10:00","11:00"),
                                         ("12:00","13:00"),
                                         ("14:00","15:00"),
                                         ("16:00","17:00"),
                                         ("18:00","19:00"),
                                         ("20:00","21:00"),
                                         ("22:00","23:00") ]

        self.currentCirculationSchedule = [("23:40","23:55")]
        self.db["sched"] = b"holiday"
        self.db.flush()


    def getControl(self):
        if self.manual_control:
            return "Manual"
        else:
            return (self.db["sched"]).decode()


    def initDatabase(self):        
        print ("Database initialization")
        try:
            f = open("mydb", "r+b")
        except OSError:
            f = open("mydb", "w+b")

        self.db = btree.open(f)
    
        try:
            if (self.db["sched"] == b"holiday"):
                self.setHolidaySchedule()
            else:
                self.setAutoSchedule()
        except KeyError:
                self.setAutoSchedule()


    def checkControl(self):
        year, month, day, hour, minutes, seconds = self.rtc.read_datetime()
        curtime = time.mktime( (year, month, day, hour, minutes, seconds, None, None))

        areation_enable_flag = False
        circulation_enable_flag = False

        for begin, end in self.currentAreationSchedule:
            begin = time.mktime ( 
                (year,month,day , int(begin.split(':')[0]), int(begin.split(':')[1]), 0, None, None))
            end = time.mktime ( 
                (year,month,day , int(end.split(':')[0]), int(end.split(':')[1]), 0, None, None))

            if begin < curtime < end:
                areation_enable_flag = True

        for begin, end in self.currentCirculationSchedule:
            begin = time.mktime ( 
                (year,month,day , int(begin.split(':')[0]), int(begin.split(':')[1]), 0, None, None))
            end = time.mktime ( 
                (year,month,day , int(end.split(':')[0]), int(end.split(':')[1]), 0, None, None))

            if begin < curtime < end:
                circulation_enable_flag = True


        # Measure temperature and humidity
        self.dht12.measure()
        
        if (self.manual_control == False):
            if (areation_enable_flag):
                self.enableAreation()
            else:
                self.disableAreation()

            if (circulation_enable_flag):
                self.enableCirculation()
            else:
                self.disableCirculation()

        else:
            if (self.manual_areation):
                self.enableAreation()
            else:
                self.disableAreation()

            if (self.manual_circulation):
                self.enableCirculation()
            else:
                self.disableCirculation()


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
