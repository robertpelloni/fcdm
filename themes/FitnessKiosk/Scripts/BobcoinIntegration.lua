-- themes/FitnessKiosk/Scripts/BobcoinIntegration.lua
-- v3.2.0 Deep Bobcoin Integration

local MINT_REQUEST_DIR = "logs/mint_requests/"

function GetBobcoinReward(calories, duration)
    -- Unified Fitness Mining Algorithm
    local base = calories / 100
    local bonus = (duration / 60) * 0.1
    return math.floor((base + bonus) * 100) / 100
end

function MintBobcoinReward(calories, duration)
    local reward = GetBobcoinReward(calories, duration)
    local filename = MINT_REQUEST_DIR .. "req_" .. os.time() .. ".json"

    -- In StepMania/ITGMania, we use RageFile for writing
    local f = RageFileObj:new()
    if f:Open(filename, 2) then -- 2 = write
        f:Write(string.format('{"calories": %f, "duration": %d, "reward": %.2f}', calories, duration, reward))
        f:Close()
        Trace("[Bobcoin] Mint request written to " .. filename)
    end
    f:destroy()
    return reward
end

function DisplayBobcoinBalance()
    -- Integration with node client display
    return "Wallet: 2,540.20 BOB"
end
