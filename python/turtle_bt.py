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
	CCTurtle, CCWorld, TurtleActions,
	# ccrecipes.py
	RecipeHelpers, ResourceType, SmartRecipeSystem, DEFAULT_RECIPES,
)

def create_turtle_sequencer( world : CCWorld, turtle : CCTurtle ) -> BaseSequenceItem:
	args = [ turtle, world ]
	return BaseSequenceItem( wrapToRoot = False, conditionAutoParams = args, functionAutoParams = args, data = dict(), )

# MAIN BEHAVIOR TREE FUNCTIONS
class BehaviorTreeFunctions:
	pass

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

	MAIN_LOOP : BaseBehaviorTree
	INITIALIZER : BaseBehaviorTree
