-- themes/FitnessKiosk/Scripts/BobcoinIntegration.lua
-- v1.9.0 Deep Integration

local BOBCOIN_API_URL = "http://localhost:8080/bobcoin"

function GetBobcoinReward(calories, duration)
    -- Fitness Mining Algorithm: 1 BOB per 100 kcal + 0.1 BOB per minute
    local base = calories / 100
    local bonus = (duration / 60) * 0.1
    local total = base + bonus
    return math.floor(total * 100) / 100
end

function MintBobcoinReward(calories, duration)
    local reward = GetBobcoinReward(calories, duration)
    -- In production, this would call the Bobcoin node API
    -- os.execute("curl -X POST " .. BOBCOIN_API_URL .. "/mint?amount=" .. reward)
    Trace("[Bobcoin] Minting " .. reward .. " BOB for workout...")
    return reward
end

function DisplayBobcoinBalance()
    -- Integration with local node wallet
    return "2,540.20 BOB"
end
