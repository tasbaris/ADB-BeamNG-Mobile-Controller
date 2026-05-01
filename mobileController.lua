local M = {}
local socket = require("socket")
local udp = nil
local deviceInst = nil

-- Store previous states to emit only on changes (performance optimization)
local prevState = {
    steering = -999,
    throttle = -999,
    brake = -999,
    clutch = -999,
    handbrake = -999,
    btnUp = -1,
    btnDown = -1,
    btnStart = -1,
    btnReset = -1
}

-- Cleanup function called when extension is unloaded or game closes
local function onExtensionUnloaded()
    if deviceInst ~= nil and extensions.core_input_virtualInput then
        extensions.core_input_virtualInput.deleteDevice(deviceInst)
        deviceInst = nil
        log('I', 'mobileController', "Virtual Input Device deleted successfully.")
    end
end

local function onUpdate(dt)
    -- Initialize UDP Socket
    if not udp then
        udp = socket.udp()
        udp:settimeout(0)
        udp:setsockname("127.0.0.1", 5555)
        log('I', 'mobileController', ">>> Mobile Controller GE Extension Started (UDP: 5555) <<<")
    end

    -- Initialize Virtual Device if not exists
    if deviceInst == nil and extensions.core_input_virtualInput then
        -- 5 Axes (Steer, Gas, Brake, Clutch, Handbrake), 4 Buttons (Up, Down, Start, Reset)
        deviceInst = extensions.core_input_virtualInput.createDevice("BeamNG Mobile Controller", "bng_mobile_v1", 5, 4, 0)
        log('I', 'mobileController', "Virtual Controller created. Instance ID: " .. tostring(deviceInst))
    end

    local latest_data = nil
    -- Clear buffer and get only the most recent packet for analog controls
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

        -- Axis 0: Steering (Map: -1..1 -> 0..1 for BeamNG internal X-Axis)
        local mapped_steering = (steering + 1) / 2
        if mapped_steering ~= prevState.steering then
            extensions.core_input_virtualInput.emit(deviceInst, "axis", 0, "change", mapped_steering)
            prevState.steering = mapped_steering
        end

        -- Axis 1: Throttle (0..1)
        if throttle ~= prevState.throttle then
            extensions.core_input_virtualInput.emit(deviceInst, "axis", 1, "change", throttle)
            prevState.throttle = throttle
        end

        -- Axis 2: Brake (0..1)
        if brake ~= prevState.brake then
            extensions.core_input_virtualInput.emit(deviceInst, "axis", 2, "change", brake)
            prevState.brake = brake
        end

        -- Axis 3: Clutch (0..1)
        if clutch ~= prevState.clutch then
            extensions.core_input_virtualInput.emit(deviceInst, "axis", 3, "change", clutch)
            prevState.clutch = clutch
        end

        -- Axis 4: Handbrake (Rally Mode)
        if handbrake ~= prevState.handbrake then
            extensions.core_input_virtualInput.emit(deviceInst, "axis", 4, "change", handbrake)
            prevState.handbrake = handbrake
        end

        -- Button 0: Shift Up
        local btnUp = (gear_cmd == 1) and 1 or 0
        if btnUp ~= prevState.btnUp then
            extensions.core_input_virtualInput.emit(deviceInst, "button", 0, btnUp == 1 and "down" or "up", btnUp)
            prevState.btnUp = btnUp
        end

        -- Button 1: Shift Down
        local btnDown = (gear_cmd == -1) and 1 or 0
        if btnDown ~= prevState.btnDown then
            extensions.core_input_virtualInput.emit(deviceInst, "button", 1, btnDown == 1 and "down" or "up", btnDown)
            prevState.btnDown = btnDown
        end

        -- Button 2: Ignition / Start (T Key)
        if btn_t_cmd ~= prevState.btnStart then
            extensions.core_input_virtualInput.emit(deviceInst, "button", 2, btn_t_cmd == 1 and "down" or "up", btn_t_cmd)
            prevState.btnStart = btn_t_cmd
        end

        -- Button 3: Reset / Recover (R Key)
        if btn_r_cmd ~= prevState.btnReset then
            extensions.core_input_virtualInput.emit(deviceInst, "button", 3, btn_r_cmd == 1 and "down" or "up", btn_r_cmd)
            prevState.btnReset = btn_r_cmd
        end
    end
end

M.onUpdate = onUpdate
M.onExtensionUnloaded = onExtensionUnloaded
return M
