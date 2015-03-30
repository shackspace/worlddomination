cs=coap.Server()
cs:listen(5683)

buffer=""
cs:var("buffer") -- get coap://localhost:5683/v1/v/buffer


local ledpin=7
cs:var("ledpin") -- get coap://localhost:5683/v1/v/ledpin

function setLedPin(payload)
  -- TODO: error handling
  ledpin = tonumber(payload)  
  return ledpin
end
cs:fun("setLedPin")

function setLeds(payload) -- post coap://192.168.18.103:5683/v1/f/setLeds

  buffer=payload
  ws2812.writergb(ledpin,buffer)
  return "ok"
end
cs:fun("setLeds")
-- todo: set a single led
