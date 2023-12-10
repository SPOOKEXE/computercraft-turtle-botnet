
from typing import Any

def array_find( array : list, value : Any ) -> int:
	try: return array.index(value)
	except: return -1
