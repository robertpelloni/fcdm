local t = Def.ActorFrame{}

t[#t+1] = Def.Actor{
    OnCommand=function(self)
        -- Instantly assign standard game conditions and jump directly to song selection
        GAMESTATE:SetCurrentGame("dance") -- or "pump" / "smx" based on global pad setting
        GAMESTATE:SetCurrentStyle("single")
        GAMESTATE:JoinPlayer(PLAYER_1)
        SCREENMAN:GetTopScreen():SetNextScreenName("ScreenSelectMusic"):StartTransitioning("SM_GoToNextScreen")
    end
}

return t
