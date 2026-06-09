local t = Def.ActorFrame{
	Name="StepsDisplayList",
	InitCommand=function(self) self:xy(_screen.cx-26, _screen.cy + 67) end,
	OnCommand=function(self) self:queuecommand("RedrawStepsDisplay") end,
	CurrentSongChangedMessageCommand=function(self) self:queuecommand("RedrawStepsDisplay") end,

	RedrawStepsDisplayCommand=function(self)
		local song = GAMESTATE:GetCurrentSong()
		if song then
			local st = GAMESTATE:GetCurrentStyle():GetStepsType()
			local steps = song:GetStepsByStepsType(st)
			-- Sort steps by meter or difficulty
			table.sort(steps, function(a,b) return a:GetMeter() < b:GetMeter() end)

			for i=1,5 do
				local item = self:GetChild("Grid"):GetChild("Meter_"..i)
				if steps[i] then
					local level = GetFitnessLevel(steps[i])
					item:playcommand("Set", {Level=level})
				else
					item:playcommand("Unset")
				end
			end
		end
	end,
}

local Grid = Def.ActorFrame{
	Name="Grid",
}

for RowNumber=-2, 2 do
	local idx = RowNumber + 3
	Grid[#Grid+1] = Def.Quad{
		Name="MeterBackground_"..idx,
		InitCommand=function(self)
			self:diffuse(0,0,0,0.8):zoomto(30, 28):y(30*RowNumber)
		end
	}

	Grid[#Grid+1] = LoadFont("Common Bold")..{
		Name="Meter_"..idx,
		InitCommand=function(self)
			self:y(30*RowNumber):zoom(0.5)
		end,
		SetCommand=function(self, params)
			self:settext(tostring(params.Level))
			if params.Level <= 3 then self:diffuse(0,1,0,1)
			elif params.Level <= 7 then self:diffuse(1,1,0,1)
			else self:diffuse(1,0,0,1) end
		end,
		UnsetCommand=function(self) self:settext("") end,
	}
end

t[#t+1] = Grid
return t
