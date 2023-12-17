local fs, turtle, peripheral, sleep
-->> IGNORE ABOVE IN PRODUCTION <<--

local SIGN_ROTATION_TO_DIRECTION = {
	['8'] = 'south',
	['12'] = 'west',
	['0'] = 'north',
	['4'] = 'east',
}

local function readInventory()
	local items = { nil, nil, nil, nil, nil, nil, nil, nil, nil, nil, nil, nil, nil, nil, nil, nil }
	for index = 1, 16 do
		local data = turtle.getItemDetail( index )
		if data then
			items[#items+1] = data
		end
	end
	return items
end

local function findItemSlotsByPattern( pattern )
	local slots = { nil, nil, nil, nil, nil, nil, nil, nil, nil, nil, nil, nil, nil, nil, nil, nil }
	for index = 1, 16 do
		local data = turtle.getItemDetail( index )
		if data and string.find(data.name, pattern) then
			slots[#slots+1] = index
		end
	end
	return slots
end

local function findEmptyItemSlot()
	for index = 1, 16 do
		if not turtle.getItemDetail( index ) then
			return index
		end
	end
	return false
end

local function findFacingDirection()
	local signSlots = findItemSlotsByPattern( 'minecraft:(%a+)_sign' )
	if #signSlots == 0 then
		return -1
	end
	-- place a sign down
	turtle.select(signSlots[1])
	turtle.place()
	-- read the sign data
	local _, detail = turtle.inspect()
	-- dig the sign back up
	turtle.dig()
	-- return the direction
	return SIGN_ROTATION_TO_DIRECTION[ tostring(detail.state.rotation) ] or -1
end

local function getEquippedItems()
	local index = findEmptyItemSlot()
	if not index then
		return false
	end
	local equipped = { false, false }
	turtle.select( index )
	turtle.equipLeft()
	equipped[1] = turtle.getItemDetail() or false
	turtle.equipLeft()
	turtle.equipRight()
	equipped[2] = turtle.getItemDetail() or false
	turtle.equipRight()
	return equipped
end

local function populateDisk()
	if not fs.isDir('/disk') then
		error("No disk inserted into disk drive.")
	end
	local source = fs.open('startup.lua', 'r').readAll()
	-- create a new startup script inside the turtle that loads the actual turtle brain into the turtle itself
	source = 'local SRC = [===[' .. source .. ']' .. '===]'
	source = source..string.format([[
		file = fs.open('startup.lua', 'w')
		file.write(SRC)
		file.close()
		shell.execute('reboot')
	]], source)
	local file = fs.open('/disk/startup', 'w')
	file.write(source)
	file.close()
end

-- NOTE: make sure to have a pickaxe equipped in left hand
local function procreate( disk_drive_slot, floppy_slot, turtle_slot, fuel_slot )
	-- place the disk drive
	turtle.select(disk_drive_slot)
	turtle.place()
	-- place floppy inside disk drive
	turtle.select(floppy_slot)
	turtle.drop( 1 )
	-- write the turtle source to the disk drive floppy
	populateDisk()
	-- go upward and place new turtle
	turtle.up()
	turtle.select(turtle_slot)
	turtle.place()
	-- give the new turtle some fuel
	turtle.select(fuel_slot)
	turtle.drop(4) -- TODO: check fuel type and give an amount based on that
	-- turn on the turtle and let it load the brain
	peripheral.call('front', 'turnOn')
	peripheral.call('front', 'reboot')
	sleep(2)
	-- go down and pickup the floppy/disk drive
	turtle.down()
	turtle.select(floppy_slot) -- floppy
	turtle.suck(1)
	turtle.select(disk_drive_slot) -- disk drive
	turtle.dig('left')
end

local function getTurtleInfo()
	return {
		fuel = turtle.getFuelLevel(),
		inventory = readInventory(),
		equipped = getEquippedItems(),
	}
end

local actions = {
	-- Movement actions
	forward = turtle.forward,
	backward = turtle.backward,
	up = turtle.up,
	down = turtle.down,
	turnLeft = turtle.turnLeft,
	turnRight = turtle.turnRight,

	-- World-interaction actions
	attackFront = turtle.attack,
	attackAbove = turtle.attackUp,
	attackBelow = turtle.attackDown,
	digFront = turtle.dig,
	digAbove = turtle.digUp,
	digBelow = turtle.digDown,
	placeFront = turtle.place,
	placeAbove = turtle.placeUp,
	placeBelow = turtle.placeDown,
	detectFront = turtle.detect,
	detectAbove = turtle.detectUp,
	detectBelow = turtle.detectDown,
	inspectFront = turtle.inspect,
	inspectAbove = turtle.inspectUp,
	inspectBelow = turtle.inspectDown,
	compareFront = turtle.compare,
	compareAbove = turtle.compareUp,
	compareBelow = turtle.compareDown,
	dropFront = turtle.drop,
	dropAbove = turtle.dropUp,
	dropBelow = turtle.dropDown,
	suckFront = turtle.suck,
	suckAbove = turtle.suckUp,
	suckBelow = turtle.suckDown,

	-- Inventory management actions
	craftItems = turtle.craft,
	selectSlot = turtle.select,
	getSelectedSlot = turtle.getSelectedSlot,
	getItemCountInSlot = turtle.getItemCount,
	getItemSpaceInSlot = turtle.getItemSpace,
	getItemDetailsInSlot = turtle.getItemDetail,
	equipLeft = turtle.equipLeft,
	equipRight = turtle.equipRight,
	refuel = turtle.refuel,
	getFuelLevel = turtle.getFuelLevel,
	getFuelLimit = turtle.getFuelLimit,
	transferTo = turtle.transferTo,

	-- CUSTOMS
	getTurtleInfo = getTurtleInfo,
	getDirectionFromSign = findFacingDirection,
	readInventory = readInventory,
	findItemSlotsByPattern = findItemSlotsByPattern,
	getEquippedItems = getEquippedItems,
	procreate = procreate,
}

return actions
