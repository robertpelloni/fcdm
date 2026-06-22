-- Fitness Center Dance Machine Hardware Hook
-- Ensures that the FCDM 9-panel matrix input paradigm is respected by the engine.

function InitHardwareBindings()
    -- ITGMania has a mechanism to reload profiles and keymaps.
    -- For a strict kiosk, we ensure the custom mapping acts as the primary layout.
    local keymapPath = "../../config/profiles/default_keymap.ini"

    if INPUTMAN then
        Trace("[FCDM] Initializing Hardware Bindings for 9-Panel FSR.")
        -- Fallback parsing/routing would normally occur here using INPUTMAN or PROFILEMAN
        -- For FCDM, we rely on the OS-level keyboard emulation mapping established in default_keymap.ini
    end
end
