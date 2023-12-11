local os, read, textutils, sleep
-- ^ IGNORE IN PRODUCTION

local socket = require('socket')
local utility = require('utility')
local actions = require('actions')

local TURTLE_UNIQUE_ID = tostring( os.getComputerID() )
print('Unique ID:', TURTLE_UNIQUE_ID)

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

	xyz_coords = { tonumber(xyz_coords[1]), tonumber(xyz_coords[2]), tonumber(xyz_coords[3]) }

	-- direction
	print('What is the direction the turtle facing?')
	print('You can check this by pressing F3 and on the right side under "Targeted Block" there is "facing:VALUE".')
	print('The direction can be: "north", "south", "east" or "west".')
	local direction = utility.PromptUserInput('>', utility.IsValidDirection )

	return xyz_coords, direction
end

local function StartupSequence()
	local response = socket.DoesTurtleExist( TURTLE_UNIQUE_ID )
	-- print( textutils.serialiseJSON( response ) )
	if not response['success'] then
		return false, 'Could not check if the turtle exists.'
	end

	if response['data'] == true then
		return true, 'Turtle already exists!'
	elseif response['data'] == 1 then
		print('The turtle needs to be re-initialized!')
	else
		print('The turtle does not exist!')
	end

	local xyz, direction = InitializeTurtlePrompt()
	response = socket.Initialize( TURTLE_UNIQUE_ID, xyz, direction )
	-- print( textutils.serialiseJSON( response ) )
	return response['success'], response['success'] and 'Turtle has been created' or 'Turtle failed to be created: ' .. tostring( response.message )
end

print('== Turtle Startup Sequence ==')
local success, err = StartupSequence()
if not success then
	error(err)
end

print(err)

print('== Turtle Main Loop ==')

local function ParseJobResponse( response )
	local job_args = response['data']

	if not job_args then
		print('No jobs are available from the server.')
		return
	end

	local job_name = table.remove(job_args, 1)

	local actionFunc = actions[job_name]
	if actionFunc then
		local results = { actionFunc( table.unpack(job_args) ) }
		socket.SetJobResults( TURTLE_UNIQUE_ID, results )
	else
		print('Target job does not exist!', job_name)
		socket.SetJobResults( TURTLE_UNIQUE_ID, false )
	end
end

while true do
	local response = socket.GetCurrentJob( TURTLE_UNIQUE_ID )
	print( textutils.serialiseJSON(response) )

	if response['success'] then
		ParseJobResponse( response )
	else
		print('Failed to get next job because of a server error:')
		print( response['message'] )
	end

	sleep(1)
end
