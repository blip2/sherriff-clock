import os
import rtc
import wifi
import socketpool
from adafruit_httpserver import Server, Request, Response
from adafruit_ntp import NTP

class Network:
    server = None

    def __init__(self):
        print()
        print("Connecting to WiFi")
        wifi.radio.connect(os.getenv('CIRCUITPY_WIFI_SSID'), os.getenv('CIRCUITPY_WIFI_PASSWORD'))
        pool = socketpool.SocketPool(wifi.radio)
        print("Connected to WiFi with IP: ", wifi.radio.ipv4_address)

        pool = socketpool.SocketPool(wifi.radio)

        self.server = Server(pool, "/static", debug=True)
        self.server.start(str(wifi.radio.ipv4_address))

        self.base = self.server.route("/")(self.base)

        #ntp = NTP(pool, tz_offset=0)
        #rtc.RTC().datetime = ntp.datetime


    def base(self, request: Request):
        return Response(request, "OK")
