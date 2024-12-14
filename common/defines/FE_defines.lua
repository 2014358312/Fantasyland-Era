-- modify game start&end date
NDefines.NGame.START_DATE = "1000.1.1.12"
NDefines.NGame.END_DATE = "1030.1.1.1"
-- modify rules of volunteers
NDefines.NDiplomacy.VOLUNTEERS_PER_TARGET_PROVINCE = 0
NDefines.NDiplomacy.VOLUNTEERS_PER_COUNTRY_ARMY = 0
NDefines.NDiplomacy.VOLUNTEERS_DIVISIONS_REQUIRED = 0
-- Pax Bratainnica map style
NDefines_Graphics.NMapMode.CONSTRUCTION_MAP_MODE_BUILDING_DEFAULT_COLOR = { 0.43, 0.22, 0.22, 0.25 }			-- Color of states/provinces that can't be built on
NDefines_Graphics.NMapMode.CONSTRUCTION_MAP_MODE_BUILDING_MAX_LEVEL_COLOR = { 0.05, 0.1, 0.7, 0.4 } 			-- Color of states/provinces where current building level is maxed out (max is current max level, not final max level) of a building type
NDefines_Graphics.NMapMode.CONSTRUCTION_MAP_MODE_BUILDING_LEVEL_LOW_COLOR = { 0.05, 0.22, 0.0, 0.4 }
NDefines_Graphics.NMapMode.CONSTRUCTION_MAP_MODE_BUILDING_LEVEL_HI_COLOR = { 0.4, 0.9, 0.0, 0.5 }
NDefines_Graphics.NGraphics.DRAW_MAP_OBJECTS_CUTOFF = 550.0					-- Remove map objects at this distance
NDefines.NGraphics.SUN_HEIGHT = 1200
NDefines.NGraphics.SUN_INTENSITY = 0.9
NDefines_Graphics.NGraphics.BLOOM_SCALE = 0.0
NDefines.NGraphics.COUNTRY_COLOR_SATURATION_MODIFIER = 0.9
NDefines.NGraphics.GRADIENT_BORDERS_CAMERA_DISTANCE_OVERRIDE_COUNTRY = 0.08
-- modify national spirit slot
NDefines_Graphics.NGraphics.POLITICAL_GRID_SMALL_BOX_LIMIT = 8				-- Limit for gridbox in political view before it will be replaced with extended gridbox
-- modify state building slot
NDefines.NBuildings.MAX_SHARED_SLOTS = 50									-- Max slots shared by factories
