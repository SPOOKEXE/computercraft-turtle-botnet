
import traceback
import os

from computercraft import (CCWorld, CCWorldAPI, CCTurtle)
from turtle_botnet import (TurtleWebsocket, BehaviorTrees, create_turtle_sequencer)
from turtle_bt import (BehaviorTrees, BaseBehaviorTree)

def load_turtles( world : CCWorld ) -> None:
	try:
		for turtle in list(world.turtles_map.values()):
			# TODO: put turtles in the correct behavior tree that it was last in
			new_sequencer = create_turtle_sequencer( world, turtle )
			BehaviorTrees.INITIALIZER.append_sequencer( new_sequencer )
	except Exception as exception:
		print('Failed to load turtle into behavior tree:')
		traceback.print_exception( exception )

def save_world_data( world : CCWorld, filepath : str ) -> None:
	for key, item in list(BehaviorTrees.__dict__.items()):
		if type(item) == BaseBehaviorTree:
			print( f'Stopping behavior tree: {key}' )
			item.stop_auto_updater()

	with open(filepath, 'wb') as file:
		file.write( CCWorldAPI.serialize( world ) )

def load_world_data( filepath : str ) -> CCWorld:
	# no world data exists
	if not os.path.exists( filepath ):
		return CCWorld()
	# attempt to load world data
	try:
		print('Attempting to load any saved world')
		with open(filepath, 'rb') as file:
			data = file.read()
		print('Read World Data')
		world = CCWorldAPI.deserialize( data )
		print('Loaded world data from file!')
	except Exception as exception:
		traceback.print_exception( exception )
		print('Created a fresh world!')
		world = CCWorld()
	# return the new world
	return world

if __name__ == '__main__':

	filepath = 'world_out.dat'

	# load world + turtles
	world = load_world_data(filepath)

	print( [t.uid for t in list(world.turtles_map.values())] )

	if len(world.turtle_ids) > 0:
		print(f'Loading the { len(world.turtle_ids) } turtles that have been saved!')
		load_turtles( world )

	# start behavior trees
	for key, item in list(BehaviorTrees.__dict__.items()):
		if type(item) == BaseBehaviorTree:
			print( f'Starting behavior tree: {key}' )
			item.start_auto_updater()

	ccwebsocket = TurtleWebsocket( world )
	ccwebsocket.start()

	# stop all behavior trees
	for key, item in list(BehaviorTrees.__dict__.items()):
		if type(item) == BaseBehaviorTree:
			print( f'Starting behavior tree: {key}' )
			item.stop_auto_updater()

	# save world
	save_world_data( world, filepath )
