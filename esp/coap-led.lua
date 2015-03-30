cs=coap.Server()
cs:listen(5683)

buffer=""
cs:var("buffer") -- get coap://localhost:5683/v1/v/buffer


ledpin=4
cs:var("ledpin") -- get coap://localhost:5683/v1/v/ledpin

function setLedPin(payload)
  -- TODO: error handling
  ledpin = tonumber(payload)  
  return ledpin
end
cs:func("setLedPin")

function setLeds(payload) -- post coap://192.168.18.103:5683/v1/f/setLeds

  buffer=payload
  print(buffer)
  print(payload)
  ws2812.writergb(ledpin,buffer)
  return "ok"..buffer
end
cs:func("setLeds")
-- todo: set a single led
