
import json
import traceback

from typing import Any
from websockets.server import WebSocketServerProtocol
from enum import Enum

from computercraft import (
	CCWorld, CCWorldAPI, CCTurtle, BaseWebSocket
)

from minecraft import (
	Point3
)

from turtle_bt import (
	BehaviorTrees, create_turtle_sequencer
)

def is_valid_xyz( xyz : list ) -> bool:
	if type(xyz) != list or len(xyz) != 3:
		return False
	if type(xyz[0]) != int or type(xyz[1]) != int or type(xyz[2]) != int:
		return False
	return True

def is_valid_direction( direction : str ) -> bool:
	return direction == 'north' or direction == 'south' or direction == 'east' or direction == 'west'

class SocketJobEnums(Enum):
	DoesTurtleExist = 1
	Initialize = 2
	GetCurrentJob = 3
	SetJobResults = 4

class TurtleWebsocket( BaseWebSocket ):

	world : CCWorld

	def __init__( self, world : CCWorld, *args, **kwargs ):
		super().__init__( *args, **kwargs )
		self.world = world

	def dump_json2( self, value : Any, indent=None ) -> str:
		return json.dumps(value, separators=(',', ':'), indent=indent)

	def construct_response( self, success : bool = True, data : Any = None, message : str | None = None ) -> dict:
		return {
			'success' : success,
			'data' : data,
			'message' : message
		}

	async def does_turtle_exist( self, turtle_id : str ) -> bool:
		'''
		Check if the turtle exists.
		'''
		does_exist = CCWorldAPI.get_turtle_from_id( self.world, turtle_id )
		return self.construct_response( data = does_exist != None )

	async def create_turtle( self, turtle_id : str, xyz : list, direction : str ) -> None:
		'''
		Create a new turtle.
		'''
		turtle = CCWorldAPI.get_turtle_from_id( self.world, turtle_id )
		if turtle != None:
			return self.construct_response( message='The turtle already exists!' )

		if not is_valid_xyz( xyz ):
			return self.construct_response(
				success=False,
				message='The XYZ co-ordinates you have provided are invalid.'
			)

		if not is_valid_direction( direction ):
			return self.construct_response(
				success=False,
				message='The direction you have provided is invalid.'
			)

		print(f'Create turtle of id { turtle_id } at { xyz } facing { direction }!')

		new_turtle = CCWorldAPI.create_new_turtle(
			self.world,
			turtle_id,
			Point3(x=xyz[0], y=xyz[1], z=xyz[2]),
			direction
		)

		try:
			new_sequencer = create_turtle_sequencer( self.world, new_turtle )
			BehaviorTrees.INITIALIZER.append_sequencer( new_sequencer )
		except Exception as exception:
			print('Failed to append turtle to behavior tree:')
			traceback.print_exception( exception )

		return self.construct_response( message='Turtle has been created!' )

	async def destroy_turtle( self, turtle_id : str ) -> None:
		'''
		Destroy the target turtle.
		'''
		if not CCWorldAPI.does_turtle_exist( self.world, turtle_id ):
			return self.construct_response( message='The turtle does not exist!' )
		CCWorldAPI.destroy_turtle( self.world, turtle_id )
		return self.construct_response( message='The turtle has been destroyed!' )

	async def get_current_turtle_job( self, turtle_id : str ) -> list | None:
		'''
		Get the current turtle job if available.
		'''
		turtle : CCTurtle = CCWorldAPI.get_turtle_from_id( self.world, turtle_id )
		if turtle == None:
			return self.construct_response(
				success=False,
				message='The turtle does not exist!'
			)

		print(turtle)

		if turtle.active_job == None and len(turtle.job_queue) > 0:
			next_job = turtle.job_queue.pop(0)
			turtle.active_job = next_job.pop(0)
			turtle.active_args = next_job

		job = turtle.active_job
		if job == None:
			return self.construct_response( data =False )

		args = turtle.active_args
		return self.construct_response( data = [ job, *args ] )

	async def set_turtle_job_results( self, turtle_id : str, results : list ) -> None:
		'''
		Set the result of a turtle's job.
		'''
		if not CCWorldAPI.get_turtle_from_id( self.world, turtle_id ):
			return self.construct_response(
				success=False,
				message='The turtle does not exist!'
			)

		if type(results) != list:
			return self.construct_response(
				success=False,
				message=f'The results is an invalid type, expected list but got { type(results) }'
			)

		CCWorldAPI.set_job_results(
			self.world,
			turtle_id,
			results
		)

		return self.construct_response( message='The results have been set.' )

	async def handle_turtle_request( self, data : dict ) -> dict:
		'''
		Handle an incoming turtle API request.
		'''
		tid = data.get('uid')
		if tid == None or type(tid) != str:
			return self.construct_response(
				success=False,
				message='You have not provided a valid turtle id!'
			)

		job = data.get('job')
		if job == None or type(job) != int:
			return self.construct_response(
				success=False,
				message='You have not provided a valid job value!'
			)

		if job == SocketJobEnums.DoesTurtleExist.value:
			return await self.does_turtle_exist( tid )
		elif job == SocketJobEnums.Initialize.value:
			return await self.create_turtle( tid, data.get('xyz'), data.get('direction') )
		elif job == SocketJobEnums.GetCurrentJob.value:
			return await self.get_current_turtle_job( tid )
		elif job == SocketJobEnums.SetJobResults.value:
			return await self.set_turtle_job_results( tid, data.get('results') )

		return self.construct_response(
			success=False,
			message = 'The job you have specified does not exist!'
		)

	async def handle_request( self, ws : WebSocketServerProtocol ) -> None:
		'''
		Handle incoming requests.
		'''

		response = None
		try:
			jsdata = json.loads( await ws.recv() )
		except json.JSONDecodeError:
			response = self.construct_response( success=False, message="The json data you have sent could not be decoded." )
		except Exception as exception:
			response = self.construct_response( success=False, message="An internal server error occured.." )
			print("==============")
			print('A websocket connection error has occured.')
			traceback.print_exception(exception)
			print("--------------")

		if response != None:
			print(response)
			await ws.send( self.dump_json2(response) )
			return

		try:
			print( jsdata )
			response = await self.handle_turtle_request( jsdata )
			print( response )
		except Exception as exception:
			print("==============")
			print('A handle-turtle-request error has occured.')
			traceback.print_exception(exception)
			print("--------------")
			response = self.construct_response( success=False, message='An internal server error occured.' )

		await ws.send( self.dump_json2(response) )
