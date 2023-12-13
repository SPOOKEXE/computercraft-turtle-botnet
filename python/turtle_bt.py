import traceback
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

def create_turtle_sequencer( world : CCWorld, turtle : CCTurtle ) -> BaseSequenceItem:
	args = [ world, turtle ]
	return BaseSequenceItem( wrapToRoot = False, conditionAutoParams = args, functionAutoParams = args, data = dict(), )

def increment_dictionary( cache : dict, index : str, amount : int ) -> None:
	try:
		cache[index] += amount
	except:
		cache[index] = amount

# MAIN BEHAVIOR TREE FUNCTIONS
class BehaviorFunctions:

	# get the turtle info
	@staticmethod
	def GET_TURTLE_INFO( world : CCWorld, turtle : CCTurtle ) -> bool:
		result = CCWorldAPI.yield_turtle_job( world, turtle.uid, TurtleActions.getTurtleInfo )
		if type(result) != dict:
			return False
		# try pull info from the dictionary
		try:
			inventory = result['inventory']
			equipped = result['equipped']
			fuel_level = result['fuel']
		except:
			return False
		# inventory
		turtle.inventory = inventory
		# left/right hands
		left_hand = equipped[0]
		if type(left_hand) == dict:
			turtle.left_hand = Item( name=left_hand['name'], quantity=left_hand['count'] )
		right_hand = equipped[0]
		if type(right_hand) == dict:
			turtle.right_hand = Item( name=right_hand['name'], quantity=right_hand['count'] )
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
		inventory_mapping = {}
		for (item_id, amount) in turtle.inventory:
			increment_dictionary( inventory_mapping, item_id, amount )
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

# MAIN BEHAVIOR TREES
class BehaviorTrees:
	BREAK_ORE_VEIN : BaseBehaviorTree
	DIG_TUNNEL : BaseBehaviorTree
	MINE_ORE_RESOURCE : BaseBehaviorTree

	LOW_FUEL_RESOLVER : BaseBehaviorTree

	# FIND_SURFACE_RESOURCE : BaseBehaviorTree
	# FIND_UNDERGROUND_RESOURCE : BaseBehaviorTree
	# FIND_TARGET_RESOURCE : BaseBehaviorTree

	# CRAFT_TARGET_RESOURCE : BaseBehaviorTree
	# SMELT_TARGET_RESOURCE : BaseBehaviorTree
	# FARM_TREE_SAPLING : BaseBehaviorTree
	# FARM_SUGAR_CANES : BaseBehaviorTree

	MAIN_LOOP : BaseBehaviorTree
	INITIALIZER : BaseBehaviorTree

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
				lambda _, __, ___, turtle : print(f'{turtle.uid} needs more fuel! Start the LOW_FUEL_RESOLVER tree'),
				None
			), # BehaviorTrees.LOW_FUEL_RESOLVER,
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

BehaviorTrees.INITIALIZER = BehaviorTreeBuilder.build_from_nested(
	'INITIALIZER',
	TreeNodeFactory.condition_switch_node(
		initializer_switch,
		[
			# turtle already has been initialized and will start immediately.
			TreeNodeFactory.multi_callback_node([
				lambda *args : print('Turtle has already been initialized, skipping.')
			], TreeNodeFactory.pass_to_behavior_tree( BehaviorTrees.MAIN_LOOP, None )),

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
				lambda _, __, ___, turtle : BehaviorFunctions.SET_IS_TURTLE_NEW_TO_FALSE(turtle),
			], TreeNodeFactory.pass_to_behavior_tree( BehaviorTrees.MAIN_LOOP, None ))
		],
		None
	)
)
