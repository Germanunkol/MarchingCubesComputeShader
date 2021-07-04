from panda3d.core import *
from direct.showbase.ShowBase import ShowBase
from chunk import Chunk

base = ShowBase()

voxel_size = 0.15
voxels_per_chunk = 8
chunk_size = voxels_per_chunk*voxel_size

for x in range(-1,2):
    for y in range(-1,2):
        for z in range(-1,2):
            pos = LVector3f( chunk_size*x, chunk_size*y, chunk_size*z )
            chunk = Chunk( voxels_per_side=voxels_per_chunk, voxel_size=voxel_size, pos=pos )
            chunk.reparent_to( base.render )
            #chunk.compute_node_path.reparent_to( base.render )
            base.taskMgr.add( chunk.update, "update" )

base.set_background_color(0, 0, 0)
base.setFrameRateMeter(True)

base.cam.set_x(0.5)
base.cam.set_y(-2)
base.cam.set_z(0.5)

base.run()
