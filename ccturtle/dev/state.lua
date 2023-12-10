local settings
-- ^ IGNORE IN PRODUCTION

local state = {}

function state.SaveSettings( path )
	settings.save( path )
end

function state.LoadSettings( path )
	settings.load( path )
end

function state.GetState( stateName )
	return settings.get( stateName )
end

function state.SetState( stateName, stateValue )
	settings.set( stateName, stateValue )
end

function state.CreateState( stateName, stateData )
	settings.define( stateName, stateData )
end

function state.StateArrayAppend( stateName, value )
	local concurrent = state.GetState( stateName )
	table.insert( concurrent, value )
	state.SetState( stateName, concurrent )
end

function state.StateDictionaryUpdate( stateName, dictionary )
	local concurrent = state.GetState( stateName )
	for index, value in pairs( dictionary ) do
		concurrent[index] = value
	end
	state.SetState( stateName, concurrent )
end

function state.UnsetState( stateName )
	settings.unset( stateName )
end

return state
