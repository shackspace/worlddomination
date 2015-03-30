
local dirhost="spaceapi.net"
local dirip="93.92.148.20"
local path="directory.json"
local f = nil
local head=true
local function get_dir()

    function open_file()
        print('connected')
        file.open(path,'w+')
        head=true
    end

    function store_json(conn, pl) 
        if head then
            print('head')
            _,_,pl = string.find(pl,"\r\n\r\n(.*)")
            head = false
        end
        print('writing')
        file.write(pl)
    end

    function close_file()
        print('closed')
        file.close()
    end
    
    local conn=net.createConnection(net.TCP, false) 
    conn:on("connection",open_file)
    conn:on("receive",store_json )
    conn:on("disconnection",close_file)
    conn:connect(80,dirip)
    conn:send("GET /"..path.." HTTP/1.0\r\nHost: "..dirhost.."\r\n"
        .."Connection: keep-alive\r\nAccept: */*\r\n\r\n")
end

return get_dir
