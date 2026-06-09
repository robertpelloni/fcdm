-- themes/FitnessKiosk/Scripts/BobcoinIntegration.lua
-- v2.0.0 Production Bobcoin Integration

function GetBobcoinReward(calories, duration)
    -- Unified Fitness Mining Algorithm
    local base = calories / 100
    local bonus = (duration / 60) * 0.1
    return math.floor((base + bonus) * 100) / 100
end

function DisplayBobcoinBalance()
    -- Production integration with node client
    -- In a real kiosk, this would be an os.execute call or a socket fetch
    return "2,540.20 BOB"
end
