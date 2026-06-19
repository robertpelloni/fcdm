local t = Def.ActorFrame{
    InitCommand=function(self)
        self:xy(SCREEN_WIDTH - 100, SCREEN_CENTER_Y) -- Position on the right side
    end,
    OnCommand=function(self)
        local topScreen = SCREENMAN:GetTopScreen()
        if topScreen then
            topScreen:AddInputCallback(function(event)
                if event and event.PlayerNumber and event.button then
                    local panel = self:GetChild("HardwareMinimap"):GetChild("Panel_"..event.button)
                    if panel then
                        panel:playcommand("UpdatePanel", event)
                    end
                end
            end)
        end
    end
}

local panel_size = 20
local spacing = 22

-- 3x3 Minimap for 9-panel FSR hardware
local minimap = Def.ActorFrame{
    Name="HardwareMinimap",
    InitCommand=function(self)
        self:zoom(1.5)
    end
}

local function GetPanelColor(is_pressed)
    if is_pressed then
        return color("0,1,0,1") -- Green when pressed
    else
        return color("0.2,0.2,0.2,0.8") -- Dark gray idle
    end
end

local mapping = {
    {"UpLeft", "Up", "UpRight"},
    {"Left", "Center", "Right"},
    {"DownLeft", "Down", "DownRight"}
}

for row=1, 3 do
    for col=1, 3 do
        local btn = mapping[row][col]
        minimap[#minimap+1] = Def.Quad{
            Name="Panel_"..btn,
            InitCommand=function(self)
                self:xy((col-2)*spacing, (row-2)*spacing)
                self:zoomto(panel_size, panel_size)
                self:diffuse(GetPanelColor(false))
            end,
            UpdatePanelCommand=function(self, params)
                if params.PlayerNumber == PLAYER_1 and params.button == btn then
                    if params.type == "InputEventType_FirstPress" then
                        self:diffuse(GetPanelColor(true))
                    elseif params.type == "InputEventType_Release" then
                        self:diffuse(GetPanelColor(false))
                    end
                end
            end
        }
    end
end

t[#t+1] = minimap

return t
