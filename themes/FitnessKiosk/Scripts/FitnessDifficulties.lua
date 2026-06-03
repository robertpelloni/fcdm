function GetFitnessLevel(stepsObject)
    local nps = stepsObject:GetRadarValues(PLAYER_1):GetValue('RadarCategory_NotesPerSecond')

    -- Linear normalization mapping Notes Per Second straight to a standard 1-10 fitness scale
    if nps < 2.0 then return 1       -- Light walking pace
    elseif nps > 9.5 then return 10   -- Elite high-stamina threshold sprint
    else
        return math.floor(((nps - 2.0) / (9.5 - 2.0)) * 9) + 1
    end
end
