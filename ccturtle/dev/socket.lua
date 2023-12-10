local fs, turtle, peripheral, sleep, http, textutils, read
-- ^ IGNORE ABOVE IN PRODUCTION

local socket = {}

socket.JobEnums = { IsNewTurtle = 1, Initialize = 2, GetNextJob = 3, ReturnJobResult = 4, }
socket.ServerURL = '127.0.0.1:500'

function socket.PostAndReceiveJSON( message_json )
	local websocket, errmsg = http.websocket(socket.ServerURL)
	assert( websocket, errmsg )
	websocket.send( textutils.serialiseJSON(message_json) )
	local response = websocket.receive()
	websocket.close()
	return textutils.unserialiseJSON( response )
end

function socket.IsNewTurtle( turtle_id )
	return socket.PostAndReceiveJSON({
		job = socket.JobEnums.GetNextJob,
		uid = turtle_id,
	})
end

function socket.Initialize( turtle_id, xyz, direction )
	return socket.PostAndReceiveJSON({
		job = socket.JobEnums.GetNextJob,
		uid = turtle_id,
		xyz = xyz,
		direction = direction,
	})
end

function socket.GetNextJob( turtle_id )
	return socket.PostAndReceiveJSON({
		job = socket.JobEnums.GetNextJob,
		uid = turtle_id,
	})
end

function socket.ReturnJobResult( turtle_id, values )
	return socket.PostAndReceiveJSON({
		job = socket.JobEnums.ReturnJobResult,
		uid = turtle_id,
		results = values,
	})
end

return socket
