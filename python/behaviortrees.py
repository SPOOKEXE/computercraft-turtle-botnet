
from __future__ import annotations

import traceback

from copy import deepcopy
from dataclasses import dataclass, field
from random import randint
from threading import Thread
from typing import Any, Callable
from enum import Enum
from uuid import uuid4
from time import sleep

def array_find( array : list, value : Any ) -> int:
	'''
	Try find a value within the array. Returns -1 if not found.
	'''
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
	id : str = field(default_factory=lambda : uuid4().hex)
	type : NodeEnums = None
	parentIDs : list | None = None
	childIDs : list | None = None
	nextNode : BehaviorTreeNode | None = None

	# possible values
	callback : Callable | None = None
	condition : Callable | None = None
	branches : list[BehaviorTreeNode | Callable] | None = None
	if_true_branch : BehaviorTreeNode | Callable | None = None
	if_false_branch : BehaviorTreeNode | Callable | None = None
	action : Callable | None = None
	delay : int | float | None = None
	behavior_tree : BaseBehaviorTree | None = None
	mutator : Callable | None = None

class TreeNodeFactory:
	'''
	Create behavior tree nodes for a behavior tree.
	'''

	def action_node( callback : Callable[ [Any], None ], nextNode : BehaviorTreeNode | None ) -> BehaviorTreeNode:
		'''
		A action node for the behavior tree.
		'''
		return BehaviorTreeNode( type=NodeEnums.Action, action=callback, nextNode=nextNode )

	def multi_action_node( callbacks : list[Callable], nextNode : BehaviorTreeNode | None ) -> BehaviorTreeNode:
		'''
		A action node for the behavior tree.
		'''
		return BehaviorTreeNode( type=NodeEnums.MultiAction, actions=callbacks, nextNode=nextNode )

	def while_condition_node( condition : Callable[ [Any], bool ], callback : Callable[ [Any], None ], nextNode : BehaviorTreeNode | None ) -> BehaviorTreeNode:
		'''
		A while-condition node for the behavior tree.
		'''
		return BehaviorTreeNode( type=NodeEnums.ConditionWhileTrue, condition=condition, callback=callback, nextNode=nextNode )

	def delay_node( delay : int | float, nextNode : BehaviorTreeNode | None ) -> BehaviorTreeNode:
		'''
		A delay node for the behavior tree.
		'''
		return BehaviorTreeNode( type=NodeEnums.Delay, delay=delay, nextNode=nextNode )

	def condition_truefalse_node( condition : Callable[ [Any], bool ], ifTrueBranch : Callable | BehaviorTreeNode | None, ifFalseBranch : Callable | BehaviorTreeNode | None, nextNode : BehaviorTreeNode | None ) -> BehaviorTreeNode:
		'''
		A condition true-false switching node for the behavior tree.
		'''
		return BehaviorTreeNode( type=NodeEnums.ConditionTrueFalse, condition=condition, if_true_branch=ifTrueBranch, if_false_branch=ifFalseBranch, nextNode=nextNode )

	def condition_switch_node( condition : Callable[ [Any], bool ], branches : list[Callable], nextNode : BehaviorTreeNode | None ) -> BehaviorTreeNode:
		'''
		A condition callback switch node for the behavior tree.
		'''
		return BehaviorTreeNode( type=NodeEnums.ConditionSwitch, condition=condition, branches=branches, nextNode=nextNode )

	def random_switch_node( branches : list[Callable], nextNode : BehaviorTreeNode | None ) -> BehaviorTreeNode:
		'''
		A random switch node for the behavior tree.
		'''
		return BehaviorTreeNode( type=NodeEnums.RandomSwitch, branches=branches, nextNode=nextNode )

	def hook_behavior_tree( target_behavior_tree : BaseBehaviorTree, mutator : Callable | None, nextNode : BehaviorTreeNode | None ) -> BehaviorTreeNode:
		'''
		Append to target tree but wait until full completion then continue on here
		'''
		return BehaviorTreeNode( type=NodeEnums.HookBehaviorTree, behavior_tree=target_behavior_tree, mutator=mutator, nextNode=nextNode )

	def pass_to_behavior_tree( target_behavior_tree : BaseBehaviorTree, mutator : Callable | None ) -> BehaviorTreeNode:
		'''
		Append to target tree and remove from current tree
		'''
		return BehaviorTreeNode( type=NodeEnums.PassToBehaviorTree, behavior_tree=target_behavior_tree, mutator=mutator, nextNode=None )

@dataclass
class BaseSequenceItem:
	currentNodeId : str = None
	nextNodeCache : list[str] = field(default_factory=list)
	conditionAutoParams : list[Any] = field(default_factory=list)
	functionAutoParams : list[Any] = field(default_factory=list)
	isUpdating : bool = False
	data : dict | None = None

	wrapToRoot : bool = True
	isCompleted : bool = False

class BaseBehaviorTree:
	nodes : list[BehaviorTreeNode]
	rootNode : BehaviorTreeNode | None = None

	_forwardSparseTree : dict[str, str]
	_idToNode : dict[str, BehaviorTreeNode]
	_sequencersCache : list[BaseSequenceItem]

	autoUpdaterEnabled : bool = False
	data : Any | None = None

	def __init__( self, nodes : list[BehaviorTreeNode] | None = None ) -> BaseBehaviorTree:
		if nodes != None: self.nodes = nodes
		else: self.nodes = []

		self.rootNode = None
		self._forwardSparseTree = {}
		self._idToNode = {}
		self._sequencersCache = []

		self.find_root_node()
		self.update_graph_tree()

	def _internal_update_sequencer_item( self, sequence_item : BaseSequenceItem ) -> None:
		'''
		Internally update the behavior tree sequence item.
		'''

		print(sequence_item.currentNodeId, sequence_item.nextNodeCache)

		currentNodeId : BehaviorTreeNode = None
		try:
			currentNodeId = sequence_item.nextNodeCache.pop()
		except:
			if sequence_item.wrapToRoot:
				currentNodeId = self.rootNode.id # starting off with no node
			else:
				sequence_item.isCompleted = True
				return
		try: currentNode = self._idToNode[currentNodeId]
		except: raise ValueError('Could not find node from id:', currentNodeId) # currentNode = self.rootNode

		sequence_item.currentNodeId = currentNodeId
		condArgs = sequence_item.conditionAutoParams!=None and sequence_item.conditionAutoParams or []
		funcArgs = sequence_item.functionAutoParams!=None and sequence_item.functionAutoParams or []

		if currentNode.nextNode != None:
			sequence_item.nextNodeCache.insert( 0, currentNode.nextNode.id )

		if currentNode.type == NodeEnums.Action:

			currentNode.action( self, sequence_item, *funcArgs )

		elif currentNode.type == NodeEnums.MultiAction:

			for action in currentNode.actions: action( self, sequence_item, *funcArgs )

		elif currentNode.type == NodeEnums.ConditionSwitch:

			index : int = currentNode.condition( self, sequence_item, *condArgs )
			assert type(index) == int, 'ConditionSwitch condition callback did not return a number.'
			assert index > len(currentNode.branches), 'Returned index is out of bounds.'
			value : Callable | str = currentNode.branches[index]

			if callable(value) == True:
				value(self, sequence_item, *funcArgs)
			elif type(value) == str and self._idToNode.get(value) != None:
				sequence_item.nextNodeCache.insert( 0, value )

		elif currentNode.type == NodeEnums.ConditionTrueFalse:

			trueFalse : bool = currentNode.condition( self, sequence_item, *condArgs )
			value : Callable | str = trueFalse==True and currentNode.if_true_branch or currentNode.if_false_branch
			if callable(value) == True:
				value(self, sequence_item, *funcArgs)
			elif type(value) == str and self._idToNode.get(value) != None:
				sequence_item.nextNodeCache.insert( 0, value )

		elif currentNode.type == NodeEnums.ConditionWhileTrue:

			value : bool = currentNode.condition( self, sequence_item, *condArgs )
			while value == True:
				currentNode.callback( self, sequence_item, *funcArgs )
				value = currentNode.condition( self, sequence_item, *condArgs )

		elif currentNode.type == NodeEnums.RandomSwitch:

			randomIndex : int = randint(0, len(currentNode.branches) - 1)
			try: value = currentNode.branches[randomIndex]
			except: value = None

			if callable(value) == True:
				value(self, sequence_item, *funcArgs)
			elif type(value) == str and self._idToNode.get(value) != None:
				sequence_item.nextNodeCache.insert(0, value)

		elif currentNode.type == NodeEnums.HookBehaviorTree:

			previous_wrapRoot = sequence_item.wrapToRoot
			currentNode.behavior_tree.append_sequencer( sequence_item )

			sequence_item.wrapToRoot = False
			currentNode.behavior_tree.await_sequencer_completion( sequence_item )

			sequence_item.wrapToRoot = previous_wrapRoot

		elif currentNode.type == NodeEnums.PassToBehaviorTree:

			# mutate before popping
			if currentNode.mutator != None: currentNode.mutator( self, sequence_item )
			self.pop_sequencer( sequence_item )
			currentNode.behavior_tree.append_sequencer( sequence_item )

		else:
			print("NodeEnum is not implemented: ", currentNode.type.name )

	def update_sequencer_items( self, daemon : bool = False ) -> None:
		'''
		Update all behavior tree sequence items.
		'''
		if len(self._sequencersCache) == 0:
			return

		def update_thread( sequencer ):
			nonlocal self
			try:
				self._internal_update_sequencer_item( sequencer )
			except Exception as exception:
				print('An exception has occured trying to update a sequencer item!')
				print('=================================')
				traceback.print_exception(exception)
				print('=================================')
				print('Sequencer item has been removed.')
				self.pop_sequencer( sequencer )
			sequencer.isUpdating = False

		index : int = 0
		while index < len(self._sequencersCache):
			sequencer : BaseSequenceItem = self._sequencersCache[index]
			if not sequencer.isUpdating:
				sequencer.isUpdating = True
				Thread(target=update_thread, args=(sequencer,), daemon=daemon).start()
			index += 1

	def start_auto_updater( self, delay : float = 1/30, daemon : bool = False ) -> None:
		'''
		Start the behavior tree auto updater.
		'''
		if self.autoUpdaterEnabled: return
		print('Starting behavior tree auto-updater.')
		self.autoUpdaterEnabled = True

		def _thread( ) -> None:
			nonlocal self, delay
			while self.autoUpdaterEnabled:
				self.update_sequencer_items()
				sleep(delay)
		Thread(target=_thread, daemon=daemon).start()

	def stop_auto_updater( self ) -> None:
		'''
		Stop the behavior tree auto updater
		'''
		print('Killing behavior tree auto-updater.')
		self.autoUpdaterEnabled = False

	def create_sequencer_item( self, *args, **kwargs ) -> BaseSequenceItem:
		'''
		Create a new behavior tree sequencer item
		'''
		return BaseSequenceItem(*args, **kwargs)

	def append_sequencer( self, sequencer : BaseSequenceItem ) -> None:
		'''
		Append a sequencer item to the behavior tree resolver.
		'''
		sequencer.nextNodeCache = [self.rootNode.id]
		sequencer.isCompleted = False
		sequencer.isUpdating = False
		self._sequencersCache.append( sequencer )

	def append_bulk_sequencers( self, sequencers : list[BaseSequenceItem] ) -> None:
		'''
		Bulk append sequencer items to the behavior tree resolver.
		'''
		for seq in sequencers:
			seq.currentNodeId = self.rootNode.id
			seq.isCompleted = False
		self._sequencersCache.extend( sequencers )

	def pop_sequencer( self, sequencer : BaseSequenceItem ) -> None:
		'''
		Pop a sequencer item to the behavior tree resolver.
		'''
		sequencer.currentNodeId = None
		sequencer.isCompleted = False
		index : int = array_find( self._sequencersCache, sequencer )
		while index != -1:
			self._sequencersCache.pop( index )
			index : int = array_find( self._sequencersCache, sequencer )

	def await_sequencer_update( self, sequencer : BaseSequenceItem, interval : float | int = 1/60 ) -> None:
		while array_find( self._sequencersCache, sequencer ) != -1 and sequencer.isUpdating:
			sleep(interval)

	def await_sequencer_completion( self, sequencer : BaseSequenceItem, interval : float | int = 1/60 ) -> None:
		'''
		Note: will immediately return if 'wrapToRoot' is equal to True.
		'''
		while array_find( self._sequencersCache, sequencer ) != -1 and (not sequencer.isCompleted) and (not sequencer.wrapToRoot):
			sleep(interval)

	def find_root_node( self ) -> Any:
		'''
		Find the behavior tree root node.
		'''
		for node in self.nodes:
			if node.parentIDs == None or len(node.parentIDs) == 0:
				self.rootNode = node
				return self.rootNode
		self.rootNode = None
		return None

	def update_graph_tree( self ) -> Any:
		'''
		Update the behavior tree connecting graph.
		'''
		self._forwardSparseTree = {}
		self._idToNode = {}
		for node in self.nodes:
			self._idToNode[node.id] = node
			if self._forwardSparseTree.get(node.id) != None:
				continue
			forward : list[str] = []
			if node.type == NodeEnums.ConditionSwitch or node.type == NodeEnums.RandomSwitch:
				forward.extend( list( filter(lambda v : type(v) == str, node.branches) ) )
			elif node.type == NodeEnums.ConditionTrueFalse:
				if type(node.if_true_branch) == str:
					forward.append( node.if_true_branch )
				if type(node.if_false_branch) == str:
					forward.append( node.if_false_branch )
			if type(node.nextNode) == str: forward.append(node.nextNode)
			self._forwardSparseTree[node.id] = forward

class BehaviorTreeBuilder:

	@staticmethod
	def _search_nested_for_ids( node : BehaviorTreeNode, cache : list = [] ) -> list[str]:
		if node == None or callable(node) == True or array_find( cache, node.id ) != -1:
			return cache
		cache.append(node.id)
		if node.type == NodeEnums.ConditionSwitch or node.type == NodeEnums.RandomSwitch:
			for branch in node.branches:
				BehaviorTreeBuilder._search_nested_for_ids( branch, cache=cache )
		elif node.type == NodeEnums.ConditionTrueFalse:
			BehaviorTreeBuilder._search_nested_for_ids( node.if_true_branch, cache=cache )
			BehaviorTreeBuilder._search_nested_for_ids( node.if_false_branch, cache=cache )
		return cache

	@staticmethod
	def _search_nested_fill_links( node : BehaviorTreeNode, parent : BehaviorTreeNode | None = None, cache : list = [] ) -> None:
		'''
		Edit all the nodes within the target tree
		'''
		if node == None or callable(node) == True: return

		# check parent
		if parent != None:
			if parent.childIDs == None: parent.childIDs = []
			if array_find( parent.childIDs, node.id ) == -1:
				parent.childIDs.append(node.id)

		# check if node was already searched
		if array_find( cache, node.id ) != -1: return
		cache.append(node.id)

		if node.childIDs == None:
			node.childIDs = []
		if node.parentIDs == None:
			node.parentIDs = []

		if parent != None and array_find(node.parentIDs, parent.id) == -1:
			node.parentIDs.append( parent.id )

		if node.type == NodeEnums.ConditionSwitch or node.type == NodeEnums.RandomSwitch:
			for branch in node.branches:
				BehaviorTreeBuilder._search_nested_fill_links( branch, parent=node, cache=cache )
		elif node.type == NodeEnums.ConditionTrueFalse:
			BehaviorTreeBuilder._search_nested_fill_links( node.if_true_branch, parent=node, cache=cache )
			BehaviorTreeBuilder._search_nested_fill_links( node.if_false_branch, parent=node, cache=cache )

		nextnode : BehaviorTreeNode = node.nextNode
		if nextnode != None:
			if nextnode.childIDs == None: nextnode.childIDs = []
			if nextnode.parentIDs == None: nextnode.parentIDs = []
			if array_find( nextnode.parentIDs, node.id ) == -1: nextnode.parentIDs.append( node.id )
			if array_find( node.childIDs, nextnode.id ) == -1: node.childIDs.append( nextnode.id )

	@staticmethod
	def _convert_nested_to_array( root : BehaviorTreeNode ) -> list:

		node_array : list[BehaviorTreeNode] = []

		def search( node : BehaviorTreeNode ) -> None:
			nonlocal node_array

			if node == None or callable(node) == True or array_find(node_array, node) != -1:
				return
			node_array.append(node)

			if node.type == NodeEnums.ConditionSwitch or node.type == NodeEnums.RandomSwitch:
				list_of_branches = node.branches[0]
				if type(list_of_branches) == list:
					node.branches = [ branch.id for branch in list_of_branches ]
					for branch in list_of_branches: search(branch)
			elif node.type == NodeEnums.ConditionTrueFalse:
				trueBranch = node.if_true_branch
				falseBranch = node.if_false_branch
				if type(trueBranch) == BehaviorTreeNode:
					node.if_true_branch = trueBranch.id
				if type(falseBranch) == BehaviorTreeNode:
					node.if_false_branch = falseBranch.id
				search( trueBranch )
				search( falseBranch )

			nnode = node.nextNode
			if nnode != None:
				node.nextNode = nnode.id
				search(nnode)

		search(root)
		return node_array

	@staticmethod
	def build_from_nested_dict( root : BehaviorTreeNode ) -> BaseBehaviorTree:
		root = deepcopy(root)
		# deep search for nodes and get all of their ids
		# _ = BehaviorTreeBuilder._search_nested_for_ids( root )
		# deep search nodes and compute child/parent links.
		BehaviorTreeBuilder._search_nested_fill_links( root )
		# create a node array
		nodeArray : list[BehaviorTreeNode] = BehaviorTreeBuilder._convert_nested_to_array( root )
		# return a new behavior tree
		return BaseBehaviorTree(nodes=nodeArray)

# tests
# if __name__ == '__main__':

# 	from time import sleep

# 	def p1(_, __): print('1')
# 	def p2(_, __) : print('2')
# 	def p3(_, __) : print('3')

# 	def print_extra( _, __ ): print('wowzie')

# 	bt : BaseBehaviorTree = BehaviorTreeBuilder.build_from_nested_dict(
# 		TreeNodeFactory.condition_truefalse_node(
# 			lambda _, __ : randint(0, 1) == 0,
# 			TreeNodeFactory.random_switch_node([ p1, p2, p3 ], None),
# 			print_extra,
# 			None
# 		)
# 	)

# 	seq_item = bt.create_sequencer_item()
# 	bt.append_sequencer( seq_item )

# 	print("STEP START")
# 	hasBeenToRoot = False
# 	steps = 1
# 	while seq_item.currentNodeId != bt.rootNode.id or not hasBeenToRoot:
# 		if seq_item.currentNodeId == bt.rootNode.id: hasBeenToRoot = True
# 		bt.update_sequencer_items()
# 		bt.await_sequencer_complete(seq_item)
# 		print(seq_item)
# 		steps += 1
# 	print(f"REACHED ROOT AFTER {steps} steps.")
