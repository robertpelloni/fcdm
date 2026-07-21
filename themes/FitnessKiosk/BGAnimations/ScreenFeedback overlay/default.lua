local t = Def.ActorFrame{
    OnCommand=function(self)
        -- Auto-advance after 10 seconds if no input
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
    Text="HOW WAS YOUR WORKOUT?",
    InitCommand=function(self)
        self:Center():y(_screen.cy - 100):zoom(1.2)
    end
}

t[#t+1] = Def.ActorFrame{
    InitCommand=function(self) self:Center() end,

    LoadFont("Common Normal")..{
        Text="[LEFT] TOO EASY",
        InitCommand=function(self) self:y(-20):zoom(0.8):x(-150) end
    },
    LoadFont("Common Normal")..{
        Text="[START] PERFECT",
        InitCommand=function(self) self:y(-20):zoom(0.8):x(0) end
    },
    LoadFont("Common Normal")..{
        Text="[RIGHT] TOO HARD",
        InitCommand=function(self) self:y(-20):zoom(0.8):x(150) end
    }
}

t[#t+1] = LoadFont("Common Normal")..{
    Text="Step on a panel to give feedback",
    InitCommand=function(self)
        self:Center():y(_screen.cy + 100):zoom(0.6):diffusealpha(0.7)
    end
}

-- Input handling
t[#t+1] = Def.Actor{
    InputMessageCommand=function(self, params)
        if params.type == "FirstPress" then
            if params.button == "MenuLeft" or params.button == "Left" then
                -- Log: Too Easy
                Trace("FEEDBACK: TOO EASY")
                self:GetParent():queuecommand("Off")
            elseif params.button == "Start" then
                -- Log: Perfect
                Trace("FEEDBACK: PERFECT")
                self:GetParent():queuecommand("Off")
            elseif params.button == "MenuRight" or params.button == "Right" then
                -- Log: Too Hard
                Trace("FEEDBACK: TOO HARD")
                self:GetParent():queuecommand("Off")
            end
        end
    end
}

return t
