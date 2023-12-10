local os, read
-- ^ IGNORE IN PRODUCTION

local state = require('dev.state')
local socket = require('dev.socket')
local utility = require('dev.utility')
local actions = require('dev.actions')

local TURTLE_UNIQUE_ID = os.getComputerID()
print('Loading turtle of unique id:', TURTLE_UNIQUE_ID)

state.LoadSettings( 'turtle_state.json' )

state.CreateState('is_new', {description = 'Marks if the turtle is a new turtle.', default=true, type='bool'})
state.CreateState('current_job', { description = 'The current job id.', default='none', type='string', })
state.CreateState('current_args', { description = 'The current job args.', default={}, type='table', })
state.CreateState('current_tracker', { description = 'The current job tracker id.', default='none', type='string', })

local function InitializeTurtlePrompt()
	-- initial prompt
	print('Welcome to the ComputerCraft Turtle HIVE')
	print('Make sure to have all the requirements inside the turtle.')
	print('You can check the requirements on the repository README page.')
	print()
	print('Press any key to continue.')
	read() -- wait for user input

	-- coordinates
	print('What is the X/Y/Z coordinate of the TURTLE block?')
	print('Enter in the following format: "[X] [Y] [Z]" where there are spaces inbetween the integers.')
	local xyz_coords = utility.PromptUserInput('>', utility.IsValidCoordinatesString )

	-- direction
	print('What is the direction the turtle facing?')
	print('You can check this by pressing F3 and on the right side under "Targeted Block" there is "facing:VALUE".')
	print('The direction can be: "north", "south", "east" or "west".')
	local direction = utility.AskForUserInput('>', utility.IsValidDirection )

	return xyz_coords, direction
end

local results = { socket.IsNewTurtle( TURTLE_UNIQUE_ID ) }
print(results)

-- if state.GetState('is_new') == true then
-- 	local xyz, direciton = InitializeTurtlePrompt()
-- end
