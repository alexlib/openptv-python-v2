"""MatchedCoords class for OpenPTV."""

import numpy as np
from .epi import Coord2d_dtype

class MatchedCoords:
    """A class for matched coordinates."""
    
    def __init__(self, num_points: int = 0):
        """Initialize a MatchedCoords object."""
        self.arr = np.recarray(num_points, dtype=Coord2d_dtype)
        
    def __getitem__(self, index):
        """Get an item from the array."""
        return self.arr[index]
        
    def __len__(self):
        """Get the length of the array."""
        return len(self.arr)
        
    def __iter__(self):
        """Iterate over the array."""
        for i in range(len(self.arr)):
            yield self.arr[i]
