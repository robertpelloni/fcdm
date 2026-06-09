-- themes/FitnessKiosk/Scripts/BobcoinIntegration.lua
-- v2.2.0 Bobcoin Integration

function GetBobcoinReward(calories, duration)
    -- Fitness Mining Algorithm: 1 BOB per 100 kcal + 0.1 BOB per minute
    local base = calories / 100
    local bonus = (duration / 60) * 0.1
    local total = base + bonus
    return math.floor(total * 100) / 100
end

function DisplayBobcoinBalance()
    -- Integration with local supernode
    return "Wallet: 2,540.20 BOB"
end
