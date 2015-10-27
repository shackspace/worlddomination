wifi.setmode(wifi.STATION)
wifi.sta.config("shack","<shack-pw>")
dofile("coap-led.lua")
