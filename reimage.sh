esptool.py --port /dev/ttyUSB0 erase_flash
esptool.py --port /dev/ttyUSB0 --baud 460800 write_flash --flash_size=detect 0 esp8266-20180511-v1.9.4.bin
ampy put main.py 
ampy put boot.py 
ampy put DHT12.py 
ampy put DS1307.py 
ampy put html.py 
ampy put WWC.py
