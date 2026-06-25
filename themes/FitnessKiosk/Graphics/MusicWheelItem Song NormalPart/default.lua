local song
local steps
local fitness_level = 0

return Def.ActorFrame {
    -- We'll inherit the basic background from Simply Love or _fallback if we wanted,
    -- but for Kiosk we want it clean.

    Def.Quad {
        InitCommand=function(self)
            self:horizalign(left):zoomto(200, 40):diffuse(0,0,0,0.5)
        end
    },

    LoadFont("Common Normal")..{
        InitCommand=function(self)
            self:horizalign(left):x(5):zoom(0.8):shadowlength(1)
        end,
        SetCommand=function(self, params)
            if params.Song then
                self:settext(params.Song:GetDisplayMainTitle())
            else
                self:settext("")
            end
        end
    },

    LoadFont("Common Bold")..{
        InitCommand=function(self)
            self:horizalign(right):x(195):zoom(0.6)
        end,
        SetCommand=function(self, params)
            if params.Song then
                -- Get the steps for the current style
                local st = GAMESTATE:GetCurrentStyle():GetStepsType()
                local steps = params.Song:GetOneSteps(st, 'Difficulty_Hard') or params.Song:GetOneSteps(st, 'Difficulty_Medium') or params.Song:GetStepsByStepsType(st)[1]

                if steps then
                    local level = GetFitnessLevel(steps)
                    self:settext("LV " .. tostring(level))
                    -- Color code based on level
                    if level <= 3 then self:diffuse(0,1,0,1)
                    elif level <= 7 then self:diffuse(1,1,0,1)
                    else self:diffuse(1,0,0,1) end
                else
                    self:settext("")
                end
            else
                self:settext("")
            end
        end
    }
}
