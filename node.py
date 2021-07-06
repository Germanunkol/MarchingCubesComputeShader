
class Node():

    def __init__( self, index, pos, size, profile_index=0 ):
        self.pos = pos
        self.size = size
        self.profile_index = profile_index
        self.index = index
        self.neighbors = []

    def addNeighbor( self, other ):

        if not other in self.neighbors:
            self.neighbors.append( other )
            self.addNeighbor.addNeighbor( self )

    def serialized( self ):
        l = [ self.pos.x, self.pos.y, self.pos.z, 0.0]    # zero pad because we need to use vec4!
        l += [ self.size, float(self.profile_index), 0.0, 0.0 ]
        return l
