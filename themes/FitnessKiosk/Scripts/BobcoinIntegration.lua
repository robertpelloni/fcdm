-- themes/FitnessKiosk/Scripts/BobcoinIntegration.lua
-- Integration for github.com/robertpelloni/bobcoin

function GetBobcoinReward(calories, duration)
    -- Fitness Mining: 1 Bobcoin per 100 kcal or 10 mins of workout
    local reward = (calories / 100) + (duration / 600)
    return math.floor(reward * 100) / 100
end

function DisplayBobcoinBalance()
    -- Mock interface to Bobcoin Wallet
    return "1,234.56 BOB"
end
