
from typing import Any

def array_find( array : list, value : Any ) -> int:
	try:
		return array.index(value)
	except:
		return -1

def cache_increment_index( cache : dict, index : str, amount : int ) -> None:
	try:
		cache[index] += amount
	except:
		cache[index] = amount

def cache_push_increment( to_cache : dict, from_cache : dict ) -> None:
	for index, amount in from_cache.items():
		cache_increment_index( to_cache, index, amount )
