local read
-- ^ IGNORE IN PRODUCTION

local utility = {}

function utility.StringSplit( input, separator )
	if separator == nil then separator = "%s" end
	local t = {}
	for str in string.gmatch(input, "([^"..separator.."]+)") do
		table.insert(t, str)
	end
	return t
end

function utility.IsValidCoordinatesString( value )
	local splits = utility.StringSplit(value, ' ')
	if #splits ~= 3 then
		return false, 'Incorrectly formatted, enter as "[X] [Y] [Z]".'
	end
	for _, item in ipairs(splits) do
		if tonumber(item) and (not string.find(item, '.')) and (not string.find(item, 'e')) then
			return false, 'Only whole real integer numbers are allowed as X/Y/Z coordinates.'
		end
	end
	return true, splits
end

function utility.IsValidDirection( value )
	local isDirection = (value == 'north') or (value == 'south') or (value == 'west') or (value == 'east')
	return isDirection, isDirection and value or 'Invalid direction value; must be one of "north", "south", "east" or "west".'
end

function utility.PromptUserInput( prompt, input_validator )
	print(prompt)
	local success, err = input_validator( read() )
	while not success do
		print(err)
		print(prompt)
		success, err = input_validator( read() )
	end
	return err
end

return utility
