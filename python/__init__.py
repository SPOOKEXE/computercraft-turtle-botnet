
import traceback

from computercraft import CCWorld, CCWorldAPI
from turtle_botnet import TurtleWebsocket, BehaviorTrees, create_turtle_sequencer
from turtle_bt import BehaviorTrees, BaseBehaviorTree

if __name__ == '__main__':

	try:
		print('Attempting to load any saved world')
		with open('world_out.dat', 'rb') as file:
			data = file.read()
		print('Read World Data')
		world = CCWorldAPI.deserialize( data )
		print('Loaded world data from file!')
	except Exception as exception:
		traceback.print_exception( exception )
		print('Created a fresh world!')
		world = CCWorld()

	print( [t.uid for t in list(world.turtles_map.values())] )

	def load_turtles( world : CCWorld ) -> None:
		try:
			for turtle in list(world.turtles_map.values()):
				new_sequencer = create_turtle_sequencer( world, turtle )
				BehaviorTrees.INITIALIZER.append_sequencer( new_sequencer )
		except Exception as exception:
			print('Failed to load turtle into behavior tree:')
			traceback.print_exception( exception )

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

	with open('world_out.dat', 'wb') as file:
		file.write( CCWorldAPI.serialize( world ) )
