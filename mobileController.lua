local M = {}
local socket = require("socket")
local udp = nil
local deviceInst = nil

-- Store previous states to emit only on changes (performance optimization)
local prevState = {
    steering = -999, throttle = -999, brake = -999, clutch = -999, handbrake = -999,
    btnUp = -1, btnDown = -1, btnStart = -1, btnReset = -1,
    btnLight = -1, btnESC = -1, btn4WD = -1, btnNOS = -1, btnCam = -1
}

local function onExtensionUnloaded()
    if deviceInst ~= nil and extensions.core_input_virtualInput then
        extensions.core_input_virtualInput.deleteDevice(deviceInst)
        deviceInst = nil
    end
end

local function onUpdate(dt)
    if not udp then
        udp = socket.udp()
        udp:settimeout(0)
        udp:setsockname("127.0.0.1", 5555)
    end

    if deviceInst == nil and extensions.core_input_virtualInput then
        -- 5 Axes, 13 Buttons (added Camera)
        deviceInst = extensions.core_input_virtualInput.createDevice("BeamNG Pro Controller", "bng_pro_v3", 5, 13, 0)
    end

    local latest_data = nil
    while true do
        local data = udp:receive()
        if not data then break end
        latest_data = data
    end

    if latest_data and deviceInst then
        local iter = latest_data:gmatch("[^|]+")
        local throttle = tonumber(iter()) or 0
        local brake = tonumber(iter()) or 0
        local clutch = tonumber(iter()) or 0
        local steering = tonumber(iter()) or 0
        local gear_cmd = tonumber(iter()) or 0
        local btn_t_cmd = tonumber(iter()) or 0
        local btn_r_cmd = tonumber(iter()) or 0
        local handbrake = tonumber(iter()) or 0
        
        -- New Specialized Buttons from Mobile UI
        local btn_light = tonumber(iter()) or 0
        local btn_esc = tonumber(iter()) or 0
        local btn_4wd = tonumber(iter()) or 0
        local btn_nos = tonumber(iter()) or 0
        local btn_cam = tonumber(iter()) or 0

        -- Analog Axes (0-4)
        local mapped_steering = (steering + 1) / 2
        if mapped_steering ~= prevState.steering then
            extensions.core_input_virtualInput.emit(deviceInst, "axis", 0, "change", mapped_steering)
            prevState.steering = mapped_steering
        end
        if throttle ~= prevState.throttle then extensions.core_input_virtualInput.emit(deviceInst, "axis", 1, "change", throttle); prevState.throttle = throttle end
        if brake ~= prevState.brake then extensions.core_input_virtualInput.emit(deviceInst, "axis", 2, "change", brake); prevState.brake = brake end
        if clutch ~= prevState.clutch then extensions.core_input_virtualInput.emit(deviceInst, "axis", 3, "change", clutch); prevState.clutch = clutch end
        if handbrake ~= prevState.handbrake then extensions.core_input_virtualInput.emit(deviceInst, "axis", 4, "change", handbrake); prevState.handbrake = handbrake end

        -- Standard Buttons (0-3)
        local bU = (gear_cmd == 1) and 1 or 0
        if bU ~= prevState.btnUp then extensions.core_input_virtualInput.emit(deviceInst, "button", 0, bU == 1 and "down" or "up", bU); prevState.btnUp = bU end
        local bD = (gear_cmd == -1) and 1 or 0
        if bD ~= prevState.btnDown then extensions.core_input_virtualInput.emit(deviceInst, "button", 1, bD == 1 and "down" or "up", bD); prevState.btnDown = bD end
        if btn_t_cmd ~= prevState.btnStart then extensions.core_input_virtualInput.emit(deviceInst, "button", 2, btn_t_cmd == 1 and "down" or "up", btn_t_cmd); prevState.btnStart = btn_t_cmd end
        if btn_r_cmd ~= prevState.btnReset then extensions.core_input_virtualInput.emit(deviceInst, "button", 3, btn_r_cmd == 1 and "down" or "up", btn_r_cmd); prevState.btnReset = btn_r_cmd end

        -- Pro Specialized Buttons (4-8)
        if btn_light ~= prevState.btnLight then extensions.core_input_virtualInput.emit(deviceInst, "button", 4, btn_light == 1 and "down" or "up", btn_light); prevState.btnLight = btn_light end
        if btn_esc ~= prevState.btnESC then extensions.core_input_virtualInput.emit(deviceInst, "button", 5, btn_esc == 1 and "down" or "up", btn_esc); prevState.btnESC = btn_esc end
        if btn_4wd ~= prevState.btn4WD then extensions.core_input_virtualInput.emit(deviceInst, "button", 6, btn_4wd == 1 and "down" or "up", btn_4wd); prevState.btn4WD = btn_4wd end
        if btn_nos ~= prevState.btnNOS then extensions.core_input_virtualInput.emit(deviceInst, "button", 7, btn_nos == 1 and "down" or "up", btn_nos); prevState.btnNOS = btn_nos end
        if btn_cam ~= prevState.btnCam then extensions.core_input_virtualInput.emit(deviceInst, "button", 8, btn_cam == 1 and "down" or "up", btn_cam); prevState.btnCam = btn_cam end

    end
end

M.onUpdate = onUpdate
M.onExtensionUnloaded = onExtensionUnloaded
return M
