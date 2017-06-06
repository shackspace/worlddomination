local ledpin=4
local dns_working=false
local timeout=10000
local tmrid=5
local tmrid2=4
local function write_status()
    dns_working=false
    if wifi.sta.getip() then
        sk=net.createConnection(net.TCP, 0)
        sk:dns("www.google.com",function(conn,ip)
            dns_working=true
        end)
        -- 500ms timeout
        tmr.alarm(tmrid2,500,function()
            if not dns_working then
                ws2812.writergb(ledpin,string.char(255,255,0))
            else
                ws2812.writergb(ledpin,string.char(0,255,0))
            end
        end)
    else
        ws2812.writergb(ledpin,string.char(255,0,0))
    end
    --tmr.alarm(3,timeout/2,function () ws2812.writergb(ledpin,string.char(0,0,0))end)
    tmr.alarm(tmrid,timeout,write_status)
end
ws2812.writergb(ledpin,string.char(255,0,255))
tmr.alarm(tmrid,timeout,write_status)
