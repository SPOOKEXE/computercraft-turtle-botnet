import re

from typing import Any

from behaviortrees import (
	BaseBehaviorTree, BehaviorTreeBuilder,
	BaseSequenceItem, TreeNodeFactory
)

from computercraft import (
	# websocket.py
	BaseWebSocket,
	# ccminecraft.py
	CCWorldAPI,
	# consts.py
	CCTurtle, CCWorld, TurtleActions, Item,
	# ccrecipes.py
	RecipeHelpers, ResourceType, SmartRecipeSystem, DEFAULT_RECIPES,
)

# https://minecraft.fandom.com/wiki/Ore
ORE_LEVEL_CONSTANTS = {
	'minecraft:coal_ore' : 44,
	'minecraft:lapis_ore' : -1,
	'minecraft:iron_ore' : 15,
	'minecraft:redstone_ore' : -59
}

class LuaItemStringPatterns:
	PICKAXE = 'minecraft:(%a+)_pickaxe'
	SHOVEL = 'minecraft:(%a+)_shovel'
	AXE = 'minecraft:(%a+)_axe'
	HOE = 'minecraft:(%a+)_hoe'

class PythonItemStringPatterns:
	PICKAXE = 'minecraft:(.+)_pickaxe'
	SHOVEL = 'minecraft:(.+)_shovel'
	AXE = 'minecraft:(.+)_axe'
	HOE = 'minecraft:(.+)_hoe'

def create_turtle_sequencer( world : CCWorld, turtle : CCTurtle ) -> BaseSequenceItem:
	args = [ world, turtle ]
	return BaseSequenceItem( wrapToRoot = False, conditionAutoParams = args, functionAutoParams = args, data = dict(), )

def array_find( array : list, value : Any ) -> int:
	try: return array.index(value)
	except: return -1

def increment_dictionary( cache : dict, index : str, amount : int ) -> None:
	try:
		cache[index] += amount
	except:
		cache[index] = amount

def find_array_re_match( array_of_patterns : list[str], value : str ) -> int:
	for index, pattern in enumerate(array_of_patterns):
		if len(re.findall(pattern, value)) != 0:
			return index
	return -1

# MAIN BEHAVIOR TREE FUNCTIONS
class BehaviorFunctions:

	# get the turtle info
	@staticmethod
	def GET_TURTLE_INFO( world : CCWorld, turtle : CCTurtle ) -> bool:
		data = CCWorldAPI.yield_turtle_job( world, turtle.uid, TurtleActions.getTurtleInfo )
		print('GET_TURTLE_INFO:', data)
		turtle_info = data[0]
		if type(turtle_info) != dict:
			return False
		# try pull info from the dictionary
		try:
			inventory = turtle_info.get('inventory')
			equipped = turtle_info.get('equipped')
			fuel_level = turtle_info.get('fuel')
		except:
			return False
		# inventory
		turtle.inventory = inventory
		# left/right hands
		if type(equipped) == list:
			left_hand = equipped[0]
			if type(left_hand) == dict:
				turtle.left_hand = Item(
					name=left_hand['name'],
					quantity=left_hand['count']
				)
			right_hand = equipped[1]
			if type(right_hand) == dict:
				turtle.right_hand = Item(
					name=right_hand['name'],
					quantity=right_hand['count']
				)
		# fuel
		turtle.fuel = fuel_level
		# success
		return True

	# set 'turtle_is_new' to false
	@staticmethod
	def SET_IS_TURTLE_NEW_TO_FALSE( turtle : CCTurtle ) -> None:
		turtle.is_new_turtle = False

	# is the turtle a brand new one?
	@staticmethod
	def IS_BRAND_NEW_TURTLE( turtle : CCTurtle ) -> bool:
		return turtle.is_new_turtle == True

	# count the amount of a specific item in the inventory
	@staticmethod
	def COUNT_INVENTORY_ITEMS( turtle : CCTurtle ) -> dict:
		print('COUNT INVENTORY:', turtle.inventory)
		inventory_mapping = {}
		for item in turtle.inventory:
			increment_dictionary( inventory_mapping, item.get('name'), item.get('count') )
		if turtle.left_hand != None:
			increment_dictionary( inventory_mapping, turtle.left_hand.name, turtle.left_hand.quantity )
		if turtle.right_hand != None:
			increment_dictionary( inventory_mapping, turtle.right_hand.name, turtle.right_hand.quantity )
		return inventory_mapping

	@staticmethod
	def HAS_ITEMS_IN_INVENTORY( turtle : CCTurtle, items : list[tuple[str, int]] ) -> bool:
		# map the inventory
		inventory_mapping = BehaviorFunctions.COUNT_INVENTORY_ITEMS( turtle )
		# check requirements
		for (item_id, amount) in items:
			if inventory_mapping.get(item_id) == None or inventory_mapping.get(item_id) < amount:
				return False
		return True # has requirements

	@staticmethod
	def HAS_NEW_TURTLE_REQUIREMENT( turtle : CCTurtle ) -> bool:
		# check for iron pickaxe and crafting table
		if not BehaviorFunctions.HAS_ITEMS_IN_INVENTORY( turtle, [
			('minecraft:iron_pickaxe', 1),
			('minecraft:iron_shovel', 1),
			('minecraft:iron_axe', 1),
			('minecraft:crafting_table', 1),
		] ): return False
		# check for fuel / coal_block
		if turtle.fuel < 800 and not BehaviorFunctions.HAS_ITEMS_IN_INVENTORY( turtle, [('minecraft:coal_block', 1)] ):
			return False
		# has requirements
		return True

	@staticmethod
	def HAS_LOW_FUEL( turtle : CCTurtle ) -> bool:
		y_diff = abs( turtle.position.y - ORE_LEVEL_CONSTANTS['minecraft:coal_ore'] )
		available_fuel = (turtle.fuel - y_diff)
		return available_fuel < 200 # allows 200 blocks to find coal at the COAL_Y_HEIGHT when low again

	@staticmethod
	def FIND_SLOTS_BY_PATTERN( world : CCWorld, turtle : CCTurtle, pattern : str ) -> list[int]:
		return CCWorldAPI.yield_turtle_job(
			world,
			turtle.uid,
			TurtleActions.findItemSlotsByPattern,
			pattern
		)

	@staticmethod
	def REFUEL_USING_PATTERN( world : CCWorld, turtle : CCTurtle, pattern : str ) -> None:
		result = BehaviorFunctions.FIND_SLOTS_BY_PATTERN( world, turtle, pattern )
		if len(result) == 0:
			return
		slots = [ s-1 for s in result[0] ]
		print( 'FUEL ITEMS:', slots )
		for slot in slots:
			BehaviorFunctions.GET_TURTLE_INFO( world, turtle )
			if turtle.fuel > int(turtle.MAX_FUEL * 0.5):
				print("Turtle has plenty of fuel - half of total capacity.")
				break
			CCWorldAPI.yield_turtle_job( world, turtle.uid, TurtleActions.selectSlot, slot + 1 )
			CCWorldAPI.yield_turtle_job( world, turtle.uid, TurtleActions.refuel )

	# set target resource
	def SET_TARGET_ORE( seq : BaseSequenceItem, block : str, amount : int ) -> None:
		seq.data['target_ore'] = (block, amount)

	# get the ore resource information
	def FIND_ORE_RESOURCE_INFO( block_id : str ) -> dict | None:
		return ORE_LEVEL_CONSTANTS.get(block_id)

	# equip item based on pattern
	def EQUIP_ITEM_PATTERN( world : CCWorld, turtle : CCTurtle, pattern : str, equipSlot : int ) -> bool:
		slots = BehaviorFunctions.FIND_SLOTS_BY_PATTERN( world, turtle, pattern )
		print('EQUIP SLOTS:', slots)
		if len(slots) == 0:
			return False
		results = CCWorldAPI.yield_turtle_job( world, turtle.uid, TurtleActions.selectSlot, slots[0][0] )
		equipName = (equipSlot == 0 and TurtleActions.equipLeft or TurtleActions.equipRight)
		results = CCWorldAPI.yield_turtle_job( world, turtle.uid, equipName )
		return results[0] == True

	# get appropriate tool for block below.
	def FIND_APPROPRIATE_TOOL_PATTERN_FOR_BLOCK( block_data : dict, forLua : bool ) -> str | None:
		if block_data == None:
			return None
		tagz : dict[str, bool] = block_data.get('tags')
		if tagz == None:
			return None
		print( list( filter(lambda x : x.find('mineable') != -1, tagz.keys()) ) )
		if tagz.get('minecraft:mineable/pickaxe') != None:
			return forLua and LuaItemStringPatterns.PICKAXE or PythonItemStringPatterns.PICKAXE
		elif tagz.get('minecraft:mineable/axe') != None:
			return forLua and LuaItemStringPatterns.AXE or PythonItemStringPatterns.AXE
		elif tagz.get('minecraft:mineable/shovel') != None:
			return forLua and LuaItemStringPatterns.SHOVEL or PythonItemStringPatterns.SHOVEL
		elif tagz.get('minecraft:mineable/hoe') != None:
			return forLua and LuaItemStringPatterns.HOE or PythonItemStringPatterns.HOE
		print('unsupported block:', block_data.get('name'), list(tagz.keys()))
		return None

	# equip tool for block
	def EQUIP_TOOL_TO_MINE_BLOCK( world : CCWorld, turtle : CCTurtle, block_data : dict | None ) -> bool:
		if block_data == None:
			return True # air block
		patternPy = BehaviorFunctions.FIND_APPROPRIATE_TOOL_PATTERN_FOR_BLOCK( block_data, False )
		if patternPy == None:
			return False # no know tool for it
		# try equip the tool
		print(turtle.left_hand)
		if turtle.left_hand == None or len( re.findall(patternPy, turtle.left_hand.name) ) == 0:
			print('no tool equipped - equipping tool if found.')
			patternLua = BehaviorFunctions.FIND_APPROPRIATE_TOOL_PATTERN_FOR_BLOCK( block_data, True )
			if not BehaviorFunctions.EQUIP_ITEM_PATTERN( world, turtle, patternLua, 0 ):
				print('FAILED TO EQUIP TOOL')
				return False # failed to equip pickaxe
			BehaviorFunctions.GET_TURTLE_INFO( world, turtle )
		print('TOOL IS EQUIPPED')
		return True

	# mine to the Y-level
	def MINE_TO_Y_LEVEL( world : CCWorld, turtle : CCTurtle, y_level : int ) -> bool:
		if y_level == turtle.position.y:
			return True # already here
		direction = (y_level - turtle.position.y) < 0 and -1 or 1
		distance : int = abs( y_level - turtle.position.y )
		if y_level < turtle.position.y:
			DIG_DIR = TurtleActions.digBelow
			MOVE_DIR = TurtleActions.down
		else:
			DIG_DIR = TurtleActions.digAbove
			MOVE_DIR = TurtleActions.up

		for _ in range(distance):
			if turtle.fuel == 0:
				break

			block_exists, block_data = tuple(CCWorldAPI.yield_turtle_job( world, turtle.uid, TurtleActions.inspectBelow ))
			if block_exists == True:
				# equip tool to mine block
				success = BehaviorFunctions.EQUIP_TOOL_TO_MINE_BLOCK( world, turtle, block_data )
				if not success:
					print('Failed to equip tool to dig block.')
					break
				# try mine block
				results = CCWorldAPI.yield_turtle_job( world, turtle.uid, DIG_DIR )
				print('DIG RESULT:', results)
				if results[0] == False:
					print('Failed to dig block')
					break
			# move down/up
			results = CCWorldAPI.yield_turtle_job( world, turtle.uid, MOVE_DIR )
			print('MOVE RESULT: ', results)
			if results[0] == False:
				print('Failed to move to block')
				break
			turtle.position.y += direction
		return (y_level == turtle.position.y)

# MAIN BEHAVIOR TREES
class BehaviorTrees:
	BREAK_ORE_VEIN : BaseBehaviorTree
	DIG_TUNNEL : BaseBehaviorTree
	MINE_ORE_RESOURCE : BaseBehaviorTree

	LOW_FUEL_RESOLVER : BaseBehaviorTree

	# CRAFT_TARGET_RESOURCE : BaseBehaviorTree
	# SMELT_TARGET_RESOURCE : BaseBehaviorTree
	# FARM_TREE_SAPLING : BaseBehaviorTree
	# FARM_SUGAR_CANES : BaseBehaviorTree

	MAIN_LOOP : BaseBehaviorTree
	INITIALIZER : BaseBehaviorTree

def mine_ore_resource_switch( _, seq : BaseSequenceItem, __, ___ ) -> int:
	if type(seq.data.get('target_ore')) != tuple:
		return 0
	oreName = seq.data['target_ore'][0]
	yHeight = ORE_LEVEL_CONSTANTS.get(oreName)
	if yHeight == None:
		return 1
	seq.data['target_height'] = yHeight
	return 2

# BehaviorTrees.DIG_TUNNEL
# def mine_ore_dig_tunnel_mutator( sequencer : BaseSequenceItem ) -> None:
# 	sequencer.data['gathered_amount'] = 0
# 	sequencer.data['blocks_traveled'] = 0

BehaviorTrees.MINE_ORE_RESOURCE = BehaviorTreeBuilder.build_from_nested(
	'MINE_ORE_RESOURCE',

	TreeNodeFactory.condition_switch_node(
		mine_ore_resource_switch,
		[
			# no target ore selected
			TreeNodeFactory.callback_node(
				lambda _, __, ___, turtle : print(f'Turtle of uid {turtle.uid} does not have a ore selected!'),
				None
			),
			# could not find the ore y-level info
			TreeNodeFactory.callback_node(
				lambda _, __, ___, turtle : print(f'Turtle of uid {turtle.uid} has an ore that has no y-level configuration! { turtle.data["target_ore"][0] }'),
				None
			),
			# ore was found, proceed with mining (after going to y-height)
			TreeNodeFactory.condition_truefalse_node(
				lambda _, seq, world, turtle : BehaviorFunctions.MINE_TO_Y_LEVEL( world, turtle, seq.data['target_height'] ),
				# TreeNodeFactory.while_condition_node(
				# 	lambda *args : True,
				# 	lambda _, __, ___, ____ : None,
				# 	None
				# ),
				lambda _, __, ___, turtle : print(f'Turtle of uid {turtle.uid} successfully reached target ore height.'),
				lambda _, __, ___, turtle : print(f'Turtle of uid {turtle.uid} failed to reach target ore height.'),
				None
			)
		],
		None
	)
)

def low_fuel_resolver_switch( _, __, ___, turtle ) -> int:
	inventory_mapping = BehaviorFunctions.COUNT_INVENTORY_ITEMS( turtle )
	if inventory_mapping.get('minecraft:coal') == None:
		return 1 # no coal, go mining
	return 0 # burn coal in inventory, return and check again

BehaviorTrees.LOW_FUEL_RESOLVER = BehaviorTreeBuilder.build_from_nested(
	'LOW_FUEL_RESOLVER',
	TreeNodeFactory.condition_switch_node(
		low_fuel_resolver_switch,
		[
			# burn the coal in the inventory
			TreeNodeFactory.multi_callback_node([
				lambda _, __, world, turtle : BehaviorFunctions.REFUEL_USING_PATTERN(world, turtle, 'minecraft:coal'),
				lambda _, __, world, turtle : BehaviorFunctions.REFUEL_USING_PATTERN(world, turtle, 'minecraft:coal_block'),
			], None),
			# mine for coal
			TreeNodeFactory.multi_callback_node([
				lambda *args : print('Mine for coal then go through the behavior trees again.'),
			], TreeNodeFactory.hook_behavior_tree(
				lambda _, seq : BehaviorFunctions.SET_TARGET_ORE(seq, 'minecraft:coal_ore', 27), # get tons of coal
				BehaviorTrees.MINE_ORE_RESOURCE,
			))
		],
		None
	)
)

# main brain loop
def main_switch_condition( _ , __, ___, turtle : CCTurtle ) -> int:
	print('MAIN SWITCH, GOT TURTLE:', turtle.uid)
	# has low fuel
	if BehaviorFunctions.HAS_LOW_FUEL( turtle ):
		return 0
	# does not have low fuel
	return 1

BehaviorTrees.MAIN_LOOP = BehaviorTreeBuilder.build_from_nested(
	'MAIN_LOOP',
	TreeNodeFactory.condition_switch_node(
		main_switch_condition,
		[
			# has not enough fuel so resolve the issue
			TreeNodeFactory.callback_node(
				lambda _, __, ___, turtle : print(f'{turtle.uid} needs more fuel! Start the LOW_FUEL_RESOLVER tree.'),
				TreeNodeFactory.hook_behavior_tree(None, BehaviorTrees.LOW_FUEL_RESOLVER)
			),
			# has enough fuel so focus on other activities
			TreeNodeFactory.callback_node(
				lambda _, __, ___, turtle : print(f'Turtle {turtle.uid} has minimum coal requirement but nothing else has been implemented!'),
				None
			),
		],
		TreeNodeFactory.callback_node(
			lambda bt, seq, _, __ : bt.pop_sequencer( seq ),
			None
		)
	)
)

def initializer_switch( _, __, ___, turtle : CCTurtle ) -> int:
	print('INITIALIZER SWITCH, GOT TURTLE:', turtle.uid)
	if BehaviorFunctions.IS_BRAND_NEW_TURTLE( turtle ):
		return 0 # already has been initialized
	if not BehaviorFunctions.HAS_NEW_TURTLE_REQUIREMENT( turtle ):
		return 1 # does not have turtle requirements
	if not BehaviorFunctions.GET_TURTLE_INFO(turtle):
		return 2 # get turtle info
	return 3 # has all the requirements

def main_loop_mutator( _, seq ) -> None:
	seq.wrapToRoot = True

BehaviorTrees.INITIALIZER = BehaviorTreeBuilder.build_from_nested(
	'INITIALIZER',
	TreeNodeFactory.condition_switch_node(
		initializer_switch,
		[
			# turtle already has been initialized and will start immediately.
			TreeNodeFactory.multi_callback_node([
				lambda *args : print('Turtle has already been initialized, skipping.'),
				lambda _, __, world, turtle : BehaviorFunctions.GET_TURTLE_INFO(world, turtle),
			], TreeNodeFactory.pass_to_behavior_tree( main_loop_mutator, BehaviorTrees.MAIN_LOOP )),

			# turtle does not have the initial requirements
			TreeNodeFactory.multi_callback_node([
				lambda *args : print('Turtle does not have all the requirements to start.'),
				lambda bt, seq, _, __ : bt.pop_sequencer( seq ) # remove from behavior tree
			], None),

			# could not get the turtle info
			TreeNodeFactory.multi_callback_node([
				lambda *args : print('Could not get the turtle info.'),
				lambda bt, seq, _, __ : bt.pop_sequencer( seq ) # remove from behavior tree
			], None),

			# turtle has all the requirements and now it will start.
			TreeNodeFactory.multi_callback_node([
				lambda *args : print('Turtle has all the requirements to start.'),
				lambda _, __, world, turtle : BehaviorFunctions.GET_TURTLE_INFO(world, turtle),
				lambda _, __, ___, turtle : BehaviorFunctions.SET_IS_TURTLE_NEW_TO_FALSE(turtle),
			], TreeNodeFactory.pass_to_behavior_tree( main_loop_mutator, BehaviorTrees.MAIN_LOOP ))
		],
		None
	)
)
