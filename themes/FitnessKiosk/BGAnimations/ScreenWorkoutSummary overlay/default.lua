local t = Def.ActorFrame{
    OnCommand=function(self)
        -- Auto-advance after 10 seconds
        self:sleep(10):queuecommand("Off")
    end,
    OffCommand=function(self)
        SCREENMAN:GetTopScreen():StartTransitioningByOutEnum('NextScreen')
    end,
}

t[#t+1] = Def.Quad{
    InitCommand=function(self)
        self:FullScreen():diffuse(0,0,0,1)
    end
}

t[#t+1] = LoadFont("Common Bold")..{
    Text="WORKOUT SUMMARY",
    InitCommand=function(self)
        self:Center():y(_screen.cy - 150):zoom(1.5)
    end
}

-- Stats
local stats = {
    { label="TIME", value=function() return SecondsToMSS(STATSMAN:GetCurStageStats():GetGameplaySeconds()) end },
    { label="CALORIES", value=function() return math.floor(STATSMAN:GetCurStageStats():GetPlayerStageStats(PLAYER_1):GetCaloriesBurned()) .. " kcal" end },
    { label="FITNESS LV", value=function()
        local steps = GAMESTATE:GetCurrentSteps(PLAYER_1)
        return steps and GetFitnessLevel(steps) or "N/A"
    end },
}

for i, stat in ipairs(stats) do
    t[#t+1] = LoadFont("Common Normal")..{
        Text=stat.label .. ":",
        InitCommand=function(self)
            self:Center():y(_screen.cy - 50 + (i-1)*40):x(-100):horizalign(left):zoom(0.8)
        end
    }
    t[#t+1] = LoadFont("Common Bold")..{
        InitCommand=function(self)
            self:Center():y(_screen.cy - 50 + (i-1)*40):x(100):horizalign(right):zoom(0.8)
            self:settext(stat.value())
        end
    }
end

t[#t+1] = LoadFont("Common Normal")..{
    Text="Press START to continue",
    InitCommand=function(self)
        self:Center():y(_screen.cy + 150):zoom(0.6):diffusealpha(0.5)
    end
}

-- Input handling
t[#t+1] = Def.Actor{
    InputMessageCommand=function(self, params)
        if params.type == "FirstPress" and params.button == "Start" then
            self:GetParent():queuecommand("Off")
        end
    end
}

return t
