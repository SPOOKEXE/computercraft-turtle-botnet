
import pickle
from time import sleep

from typing import Any
from uuid import uuid4

from minecraft import (
	# consts.py
	Direction, Point3, Item,
	Inventory, Block, SolidBlock,
	Chest, Furnace,
	# world.py
	WorldAPI,
	# recipes.py
)

from .utility import (
	array_find
)

from .consts import (
	CCWorld, CCTurtle, TurtleActions
)

class CCWorldAPI(WorldAPI):

	@staticmethod
	def get_turtle_from_id( world : CCWorld, turtle_id : str ) -> CCTurtle | None:
		return world.turtles_map.get( turtle_id )

	@staticmethod
	def reinitialize_turtle( world : CCWorld, turtle_id : str ) -> None:
		turtle = CCWorldAPI.get_turtle_from_id( world, turtle_id )
		if turtle == None: return None
		turtle.is_new_turtle = True

	@staticmethod
	def create_new_turtle( world : CCWorld, id : str, position : Point3, direction : str ) -> CCTurtle:
		turtle = CCTurtle( uid=id, position=position, direction=direction )
		world.turtle_ids.append(turtle.uid)
		world.turtles_map[turtle.uid] = turtle
		WorldAPI.push_block( world, position, turtle )
		return turtle

	@staticmethod
	def destroy_turtle( world : CCWorld, turtle_id : str ) -> None:
		idx = array_find( world.turtle_ids, turtle_id )
		if idx == -1:
			return
		world.turtle_ids.pop(idx)

	@staticmethod
	def get_active_job( world : CCWorld, turtle_id : str ) -> list:
		turtle = CCWorldAPI.get_turtle_from_id( world, turtle_id )
		if turtle == None: return None
		if len(turtle.job_queue) == 0: return None
		current_job : list = turtle.job_queue[0]
		tid : str = current_job[0]
		if turtle.tracker_results.get( tid ) != None:
			return None
		return current_job[1:]

	@staticmethod
	def set_job_results( world : CCWorld, turtle_id : str, results : list ) -> None:
		turtle = CCWorldAPI.get_turtle_from_id( world, turtle_id )
		if turtle == None:
			return None
		current_job = turtle.job_queue[0]
		tid = current_job[0]
		turtle.tracker_results[tid] = results

	@staticmethod
	def yield_turtle_job( world : CCWorld, turtle_id : str, job : TurtleActions, *args ) -> dict | list | bool:
		print('YIELD TURTLE JOB: ', turtle_id, job.name)
		turtle = CCWorldAPI.get_turtle_from_id( world, turtle_id )
		if turtle == None:
			return None
		tracker_id : str = uuid4().hex
		turtle.job_queue.append([ tracker_id, job.name, *args ])
		while turtle.tracker_results.get( tracker_id ) == None:
			sleep(0.01)
		turtle.job_queue.pop(0) # remove item from queue
		return turtle.tracker_results.pop( tracker_id )

	@staticmethod
	def serialize( world : CCWorld ) -> bytes:
		return pickle.dumps( world )

	@staticmethod
	def deserialize( data : bytes ) -> CCWorld:
		return pickle.loads( data )
