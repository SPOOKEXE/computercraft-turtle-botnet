local fs, turtle, peripheral, sleep, http, textutils, read
-- ^ IGNORE ABOVE IN PRODUCTION

local socket = {}

socket.JobEnums = {
	DoesTurtleExist = 1,
	Initialize = 2,
	GetCurrentJob = 3,
	SetJobResults = 4,
}

socket.ServerURL = '127.0.0.1:500'

function socket.PostAndReceiveJSON( message_json )
	local websocket, errmsg = http.websocket(socket.ServerURL)
	assert( websocket, errmsg )
	websocket.send( textutils.serialiseJSON(message_json) )
	local response = websocket.receive()
	websocket.close()
	return textutils.unserialiseJSON( response )
end

function socket.DoesTurtleExist( turtle_id )
	return socket.PostAndReceiveJSON({
		job = socket.JobEnums.DoesTurtleExist,
		uid = turtle_id,
	})
end

function socket.Initialize( turtle_id, xyz, direction )
	return socket.PostAndReceiveJSON({
		job = socket.JobEnums.Initialize,
		uid = turtle_id,
		xyz = xyz,
		direction = direction,
	})
end

function socket.GetCurrentJob( turtle_id )
	return socket.PostAndReceiveJSON({
		job = socket.JobEnums.GetCurrentJob,
		uid = turtle_id,
	})
end

function socket.SetJobResults( turtle_id, values )
	return socket.PostAndReceiveJSON({
		job = socket.JobEnums.SetJobResults,
		uid = turtle_id,
		results = values,
	})
end

return socket
