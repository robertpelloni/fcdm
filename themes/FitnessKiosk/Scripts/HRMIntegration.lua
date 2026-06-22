-- themes/FitnessKiosk/Scripts/HRMIntegration.lua
-- v2.5.0 HRM Mock Integration

function GetCurrentHeartRate()
    -- Simulated HRM Input (e.g. from ANT+ or BLE relay)
    -- In a real kiosk, this might read from a local file or socket
    return 135
end

function GetHRZone(hr, age)
    local maxHR = 220 - age
    local percent = hr / maxHR

    if percent < 0.6 then return "Zone 1 (Recovery)"
    elseif percent < 0.7 then return "Zone 2 (Fat Burn)"
    elseif percent < 0.8 then return "Zone 3 (Aerobic)"
    elseif percent < 0.9 then return "Zone 4 (Anaerobic)"
    else return "Zone 5 (Max)"
    end
end
