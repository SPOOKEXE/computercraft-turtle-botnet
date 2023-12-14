
from __future__ import annotations

from traceback import print_exception
from enum import Enum
from dataclasses import dataclass, field
from uuid import uuid4
from typing import Callable, Any
from time import sleep
from threading import Thread
from random import randint

def array_find( array : list, value : Any ) -> int:
	try: return array.index(value)
	except: return -1

class NodeEnums(Enum):
	Action = 0
	MultiAction = 1
	ConditionTrueFalse = 2
	ConditionSwitch = 3
	ConditionWhileTrue = 4
	RandomSwitch = 5
	Delay = 6
	HookBehaviorTree = 7
	PassToBehaviorTree = 8

@dataclass
class BehaviorTreeNode:
	# base node data
	id : str = field(default_factory=lambda : uuid4().hex)
	parentIDs : list | None = None
	childIDs : list | None = None
	# actual node data
	type : NodeEnums = None
	arguments : list  | None = None
	nextNode : BehaviorTreeNode | None = None

class TreeNodeFactory:
	@staticmethod
	def callback_node( callback : Callable, nextNode : BehaviorTreeNode | None ) -> BehaviorTreeNode:
		'''
		A function callback node for the behavior tree.
		'''
		assert callable( callback ) == True, 'Passed callback is NOT a callable item!'
		return BehaviorTreeNode(
			type=NodeEnums.Action,
			arguments=[callback],
			nextNode=nextNode
		)

	@staticmethod
	def multi_callback_node( callbacks : list[Callable], nextNode : BehaviorTreeNode | None ) -> BehaviorTreeNode:
		'''
		A multi-function-callback node for the behavior tree.
		'''
		for index, callback in enumerate(callbacks):
			assert callable( callback ) == True, f'Callback at index {index} is not a callable item!'
		return BehaviorTreeNode(
			type=NodeEnums.MultiAction,
			arguments=callbacks,
			nextNode=nextNode
		)

	@staticmethod
	def delay_node( delay : int | float, nextNode : BehaviorTreeNode | None ) -> BehaviorTreeNode:
		'''
		A delay node for the behavior tree.
		'''
		return BehaviorTreeNode(
			type=NodeEnums.Delay,
			arguments=[delay],
			nextNode=nextNode
		)

	@staticmethod
	def while_condition_node( condition : Callable[ [Any], bool ], callback : Callable[ [Any], None ], nextNode : BehaviorTreeNode | None ) -> BehaviorTreeNode:
		'''
		A while-condition node for the behavior tree.
		'''
		assert callable(condition) == True, 'The condition function is not callable!'
		assert callable(callback) == True, 'The callback function is not callable!'
		return BehaviorTreeNode(
			type=NodeEnums.ConditionWhileTrue,
			arguments=[condition, callback],
			nextNode=nextNode
		)

	@staticmethod
	def condition_truefalse_node( condition : Callable[ [Any], bool ], ifTrueBranch : Callable | BehaviorTreeNode | None, ifFalseBranch : Callable | BehaviorTreeNode | None, nextNode : BehaviorTreeNode | None ) -> BehaviorTreeNode:
		'''
		A condition true-false switching node for the behavior tree.
		'''
		assert callable(condition) == True, 'The condition function is not callable!'
		INVALID_BRANCH_VALUE = 'The {} branch is not a callable value, is not a behavior tree node, or is not None.'
		assert callable(ifTrueBranch) == True or type(ifTrueBranch) == BehaviorTreeNode or ifTrueBranch == None, INVALID_BRANCH_VALUE.format('IF_TRUE')
		assert callable(ifFalseBranch) == True or type(ifFalseBranch) == BehaviorTreeNode or ifFalseBranch == None, INVALID_BRANCH_VALUE.format('IF_FALSE')
		return BehaviorTreeNode(
			type=NodeEnums.ConditionTrueFalse,
			arguments=[condition, ifTrueBranch, ifFalseBranch],
			nextNode=nextNode
		)

	@staticmethod
	def condition_switch_node( condition : Callable[ [Any], int ], branches : list[Callable, BehaviorTreeNode], nextNode : BehaviorTreeNode | None ) -> BehaviorTreeNode:
		'''
		A condition callback switch node for the behavior tree.
		'''
		assert callable(condition) == True, 'Condition is not a callable!'
		for index, branch in enumerate(branches):
			assert callable(branch) or type(branch) == BehaviorTreeNode, f'Branch at index {index} is not a callable or is not a behavior tree node.'
		return BehaviorTreeNode(
			type=NodeEnums.ConditionSwitch,
			arguments=[condition, branches],
			nextNode=nextNode
		)

	@staticmethod
	def random_switch_node( branches : list[Callable | BehaviorTreeNode], nextNode : BehaviorTreeNode | None ) -> BehaviorTreeNode:
		'''
		A random switch node for the behavior tree.
		'''
		for index, branch in enumerate(branches):
			assert callable(branch) or type(branch) == BehaviorTreeNode, f'Branch at index {index} is not a callable or is not a behavior tree node.'
		return BehaviorTreeNode(
			type=NodeEnums.RandomSwitch,
			arguments=branches,
			nextNode=nextNode
		)

	@staticmethod
	def hook_behavior_tree( mutator : Callable | None, target_bt : BaseBehaviorTree ) -> BehaviorTreeNode:
		'''
		Append to target tree but wait until full completion then continue on here
		'''
		assert isinstance(target_bt, BaseBehaviorTree), 'Target behavior tree is not a behavior tree!'
		assert callable(mutator) == True or mutator == None, 'Mutator is not a callable value or is not None!'
		return BehaviorTreeNode(
			type=NodeEnums.HookBehaviorTree,
			arguments=[ mutator, target_bt ]
		)

	@staticmethod
	def pass_to_behavior_tree( mutator : Callable | None, target_bt : BaseBehaviorTree ) -> BehaviorTreeNode:
		'''
		Append to target tree and remove from current tree
		'''
		return BehaviorTreeNode(
			type=NodeEnums.PassToBehaviorTree,
			arguments=[ mutator, target_bt ]
		)

@dataclass
class BaseSequenceItem:
	uid : str = field(default_factory=lambda : uuid4().hex)
	currentNodeId : str = None
	nextNodeCache : list[str] = field(default_factory=list)
	conditionAutoParams : list[Any] = field(default_factory=list)
	functionAutoParams : list[Any] = field(default_factory=list)
	isUpdating : bool = False
	data : dict = field(default_factory=dict)

	wrapToRoot : bool = False
	isCompleted : bool = False

def parse_node( tree : BaseBehaviorTree, sequencer : BaseSequenceItem, currentNode : BehaviorTreeNode ) -> None:

	# print( sequencer.uid, currentNode.type )

	def parse_multi_type( value : str | Callable | BehaviorTreeNode | Any ) -> None:
		nonlocal tree, sequencer
		# print(type(value), value)
		if isinstance(value, BehaviorTreeNode):
			parse_node( tree, sequencer, value )
			if value.nextNode != None:
				parse_node( tree, sequencer, value.nextNode )
		elif callable( value ) == True:
			value( tree, sequencer, *sequencer.functionAutoParams )
		elif type(value) == str:
			next_node = tree._idToNode.get(value)
			if next_node == None:
				raise ValueError('Could not find node given the id: ' + str(value))
			parse_node( value )
		else:
			raise ValueError('Unsupported node value: ' + str(value))

	if currentNode.type ==  NodeEnums.Action:

		action : Callable = currentNode.arguments[0]
		action( tree, sequencer, *sequencer.functionAutoParams )

	elif currentNode.type == NodeEnums.MultiAction:

		actions : list[Callable] = currentNode.arguments
		for action in actions:
			action( tree, sequencer, *sequencer.functionAutoParams )

	elif currentNode.type == NodeEnums.Delay:

		sleep( currentNode.arguments[0] )

	elif currentNode.type == NodeEnums.RandomSwitch:

		index = randint( 0, len(currentNode.arguments) - 1 )
		value = currentNode.arguments[index]

		parse_multi_type( value )

	elif currentNode.type == NodeEnums.ConditionSwitch:

		values : list = currentNode.arguments.copy()
		condition = values.pop(0)
		branches = values.pop(0)

		index = condition( tree, sequencer, *sequencer.conditionAutoParams )
		assert type(index) == int, 'The index returned from the condition is not valid! You must return a integer.'

		error_message = 'The index is out of bounds, index is {} whilst the min/max is 0 and {}'.format(index, len(branches)-1)
		assert index >= 0 and index <= len(branches) - 1, error_message

		parse_multi_type( branches[index] )

	elif currentNode.type == NodeEnums.ConditionTrueFalse:

		values : list = currentNode.arguments.copy()
		condition = values.pop(0)

		result = condition( tree, sequencer, *sequencer.conditionAutoParams )
		assert type(result) == bool, 'The result of the ConditionTrueFalse is not a boolean!'

		parse_multi_type( result == True and values[0] or values[1] )

	elif currentNode.type == NodeEnums.ConditionWhileTrue:

		values : list = currentNode.arguments.copy()
		condition, callback = tuple(values)
		while condition( tree, sequencer, *sequencer.conditionAutoParams ):
			callback( tree, sequencer, *sequencer.functionAutoParams )

	elif currentNode.type == NodeEnums.PassToBehaviorTree:

		mutator : Callable = currentNode.arguments[0]
		target_bt : BaseBehaviorTree = currentNode.arguments[1]
		if mutator != None:
			mutator( tree, sequencer )
		tree.pop_sequencer( sequencer )
		target_bt.append_sequencer( sequencer )

	elif currentNode.type == NodeEnums.HookBehaviorTree:

		previous_wrapRoot : bool = sequencer.wrapToRoot
		nextNodeCache : list = sequencer.nextNodeCache

		mutator : Callable = currentNode.arguments[0]
		target_bt : BaseBehaviorTree = currentNode.arguments[1]
		if mutator != None:
			mutator( tree, sequencer )

		tree.pop_sequencer( sequencer )

		sequencer.wrapToRoot = False

		target_bt.append_sequencer( sequencer )
		target_bt.await_sequencer_completion( sequencer )

		sequencer.nextNodeCache = nextNodeCache
		sequencer.wrapToRoot = previous_wrapRoot

		tree.append_sequencer( sequencer )

def tree_update_thread( self : BaseBehaviorTree, sequencer : BaseSequenceItem ) -> None:
	try:

		# get the current node + id
		try: currentNode = sequencer.nextNodeCache.pop(0)
		except: currentNode = None

		if sequencer.wrapToRoot == True and currentNode == None:
			currentNode = self.root_node
		sequencer.currentNodeId = (currentNode != None and currentNode.id or None)

		if currentNode == None:
			print('No next node detected, popping sequencer and returning!')
			sequencer.isCompleted = True
			self.pop_sequencer( sequencer )
			return

		# check for next node
		if currentNode.nextNode != None:
			sequencer.nextNodeCache.insert(0, currentNode.nextNode)

		# parse the current node by node-enum.
		parse_node( self, sequencer, currentNode )

	except Exception as exception:
		print('An exception has occured trying to update a sequencer item!')
		print('=================================')
		print_exception(exception)
		print('=================================')
		print('Sequencer item has been removed.')
		self.pop_sequencer( sequencer )
	sequencer.isUpdating = False

class BaseBehaviorTree:
	uid : str
	tree_nodes : list[BehaviorTreeNode]
	root_node : BehaviorTreeNode | None

	_sparseTree : dict[str, str]
	_idToNode : dict[str, BehaviorTreeNode]
	_sequencersCache : list[BaseSequenceItem]
	_updaterEnabled : bool

	# data : Any | None = None

	def __init__( self, uid : str = uuid4().hex, nodes : list = [] ) -> BaseBehaviorTree:
		self.uid = uid
		self.tree_nodes = nodes
		self.root_node = None

		self._sparseTree = dict()
		self._idToNode = dict()
		self._sequencersCache = list()
		self._updaterEnabled = False

		self.update_sparse_graph()
		self.find_root_node()

	def append_sequencer( self : BaseBehaviorTree, sequencer : BaseSequenceItem ) -> None:
		print(f'Appended sequencer to behavior tree of uid {self.uid}')
		sequencer.currentNodeId = None
		sequencer.nextNodeCache = [ self.root_node ]
		sequencer.isCompleted = False
		sequencer.isUpdating = False
		self._sequencersCache.append( sequencer )

	def extend_sequencers( self : BaseBehaviorTree, sequencers : list[BaseSequenceItem] ) -> None:
		print(f'Extend { len(sequencers) } sequencers to behavior tree of uid {self.uid}')
		for sequencer in sequencers:
			sequencer.currentNodeId = None
			sequencer.nextNodeCache = [ self.root_node ]
			sequencer.isCompleted = False
			sequencer.isUpdating = False
		self._sequencersCache.extend( sequencers )

	def pop_sequencer( self : BaseBehaviorTree, sequencer : BaseSequenceItem ) -> None:
		sequencer.currentNodeId = None
		sequencer.nextNodeCache = list()
		sequencer.isCompleted = True
		sequencer.isUpdating = False
		while True:
			try:
				self._sequencersCache.remove( sequencer )
			except:
				break

	def await_sequencer_completion( self : BaseBehaviorTree, sequencer : BaseSequenceItem ) -> None:
		while sequencer.isUpdating:
			sleep(0.1)

	def update_sequencers( self : BaseBehaviorTree, daemon : bool = False ) -> None:
		if len(self._sequencersCache) == 0:
			return
		index : int = 0
		while index < len(self._sequencersCache):
			try:
				sequencer : BaseSequenceItem = self._sequencersCache[index]
			except:
				break
			if sequencer.isUpdating or sequencer.isCompleted:
				continue
			sequencer.isUpdating = True
			Thread(target=tree_update_thread, args=(self,sequencer,), daemon=daemon).start()
			index += 1

	def start_auto_updater( self : BaseBehaviorTree, delay : float = 1/30, daemon : bool = False ) -> None:
		if self._updaterEnabled:
			return
		print(f'Behavior tree of uid {self.uid} is now auto-updating.')
		self._updaterEnabled = True

		def _thread( ) -> None:
			nonlocal self, delay
			while self._updaterEnabled:
				self.update_sequencers()
				sleep(delay)
		Thread(target=_thread, daemon=daemon).start()

	def stop_auto_updater( self : BaseBehaviorTree ) -> None:
		print(f'Behavior tree of uid {self.uid} auto-updating has been stopped.')
		self._updaterEnabled = False

	def update_sparse_graph( self : BaseBehaviorTree ) -> None:
		self._sparseTree = dict()
		self._idToNode = dict()
		for node in self.tree_nodes:
			self._idToNode[node.id] = node
		for node in self.tree_nodes:
			if self._sparseTree.get( node.id ) != None:
				continue
			forward : list[str] = []
			for arg in node.arguments:
				if isinstance(arg, BehaviorTreeNode):
					forward.append( arg.id )
				elif type(arg) == str:
					forward.append( arg )
			if isinstance(node.nextNode, BehaviorTreeNode):
				forward.append( node.nextNode.id )
			elif type(arg) == str:
				forward.append( node.nextNode )
			self._idToNode[node.id] = forward

	def find_root_node( self : BaseBehaviorTree ) -> BehaviorTreeNode | None:
		value = None
		for node in self.tree_nodes:
			if node.parentIDs == None or len(node.parentIDs) == 0:
				value = node
				break
		self.root_node = value
		return value

class BehaviorTreeBuilder:

	@staticmethod
	def fill_node_links( node : BehaviorTreeNode, parent : BehaviorTreeNode | None, cache : list = [] ) -> list[BehaviorTreeNode]:
		if node == None or callable(node) == True:
			return

		if parent != None:
			if parent.childIDs == None:
				parent.childIDs = []
			if array_find( parent.childIDs, node.id ) == -1:
				parent.childIDs.append(node.id)

		# skip repeats (cyclic avoidance)
		if array_find( cache, node.id ) != -1:
			return
		cache.append(node.id)

		if node.childIDs == None:
			node.childIDs = []
		if node.parentIDs == None:
			node.parentIDs = []

		if parent != None and array_find(node.parentIDs, parent.id) == -1:
			node.parentIDs.append( parent.id )

		if node.arguments != None and len(node.arguments) > 0:
			for value in node.arguments:
				if not isinstance( value, BehaviorTreeNode ):
					continue
				BehaviorTreeBuilder.fill_node_links( value, node, cache=cache )

		# next nodes
		nextNode : BehaviorTreeNode | None = node.nextNode
		if nextNode == None:
			return

		if nextNode.childIDs == None:
			nextNode.childIDs = []
		if nextNode.parentIDs == None:
			nextNode.parentIDs = []

		if array_find( nextNode.parentIDs, node.id ) == -1:
			nextNode.parentIDs.append( node.id )
		if array_find( node.childIDs, nextNode.id ) == -1:
			node.childIDs.append( nextNode.id )

	@staticmethod
	def convert_nested_to_array( root : BehaviorTreeNode ) -> list[BehaviorTreeNode]:
		node_array : list[BehaviorTreeNode] = list()
		passed_array : list[str] = list()

		def search( node : BehaviorTreeNode ) -> None:
			nonlocal node_array
			# print(node)
			if array_find(passed_array, node.id) != -1:
				return
			passed_array.append(node.id)
			node_array.append(node)
			if node.arguments and len(node.arguments) > 0:
				for index, arg in enumerate(node.arguments):
					# print(index, arg)
					if isinstance( arg, BehaviorTreeNode ):
						node_array.append(arg)
						search( arg )
						# node.arguments[index] = arg.id
			if node.nextNode != None and isinstance(node.nextNode, BehaviorTreeNode):
				node_array.append(node)
				search( node.nextNode )
				# node.nextNode = node.nextNode.id

		# print( node_array )
		search( root )
		return node_array

	@staticmethod
	def build_from_nested( uuid : str, root : BehaviorTreeNode ) -> BaseBehaviorTree:
		BehaviorTreeBuilder.fill_node_links( root, None, cache=[] )
		node_array = BehaviorTreeBuilder.convert_nested_to_array( root )
		return BaseBehaviorTree(uid=uuid, nodes=node_array)

# tests
# if __name__ == '__main__':

# 	from time import sleep

# 	def p1(_, __):
# 		print('1')
# 	def p2(_, __) :
# 		print('2')
# 	def p3(_, __) :
# 		print('3')

# 	def print_extra( _, __ ):
# 		print('wowzie')

# 	bt : BaseBehaviorTree = BehaviorTreeBuilder.build_from_nested(
# 		'TEST_TREE',
# 		TreeNodeFactory.condition_truefalse_node(
# 			lambda _, __ : randint(0, 1) == 0,
# 			TreeNodeFactory.random_switch_node([ p1, p2, p3 ], None),
# 			print_extra,
# 			None
# 		)
# 	)

# 	seq_item = BaseSequenceItem()
# 	bt.append_sequencer( seq_item )

# 	print("STEP START")
# 	hasBeenToRoot = False
# 	steps = 1
# 	while seq_item.currentNodeId != bt.root_node.id or not hasBeenToRoot:
# 		if seq_item.currentNodeId == bt.root_node.id:
# 			hasBeenToRoot = True
# 		bt.update_sequencers()
# 		#bt.await_sequencer_completion(seq_item)
# 		while seq_item.isUpdating:
# 			sleep(0.1)
# 		# print(seq_item)
# 		if seq_item.isCompleted == True:
# 			break
# 		steps += 1
# 	print(f"REACHED FINISH AFTER {steps} steps.")
