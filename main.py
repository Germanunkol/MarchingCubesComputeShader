from panda3d.core import *
from direct.showbase.ShowBase import ShowBase
from chunk import Chunk
from node import Node
import random, math
from array import array

base = ShowBase()

voxel_size = 0.5
voxels_per_chunk = 8
chunk_size = voxels_per_chunk*voxel_size

map_size = 24 # in meters
half_map_size = map_size*0.5 # in meters

nodes = []
for i in range(10):
    profile = int(random.random()*3)
    pos = LVector3f( random.random()*map_size-half_map_size,
            random.random()*map_size-half_map_size,
            random.random()*map_size-half_map_size )
    nodes.append( Node( index=0, pos=pos, size=random.random()*2+0.5, profile_index=profile ) )

tunnels = []

for i in range(20):
    n1 = nodes[i % len(nodes)]
    n2 = random.choice( nodes )
    tunnels.append( (n1, n2) )
#tunnels.append( (nodes[2], nodes[1]) )

tunnels_serialized = []
for t in tunnels:
    node1 = t[0]
    node2 = t[1]
    t_s = []
    t_s += [node1.pos.x, node1.pos.y, node1.pos.z, node1.size]
    t_s += [node2.pos.x, node2.pos.y, node2.pos.z, node2.size]
    t_s += [float(node1.profile_index), float(node2.profile_index)]
    t_s += [0,0]    # padding
    # Pad each array element to 16 bytes:
    #padding = 16 - len(t_s) % 16
    #if padding != 0:
        #t_s += [0.0]*padding

    tunnels_serialized += t_s

input_shader_buffer = ShaderBuffer("chunk_input",
                array('f', tunnels_serialized ).tobytes(),
                GeomEnums.UH_static )

chunks = []

for x in range(-3,4):
    for y in range(-3,4):
        for z in range(-3,4):
            pos = LVector3f( chunk_size*x, chunk_size*y, chunk_size*z )
            chunk = Chunk( voxels_per_side=voxels_per_chunk, voxel_size=voxel_size, pos=pos, input_shader_buffer=input_shader_buffer )
            chunk.reparent_to( base.render )
            #chunk.compute_node_path.reparent_to( base.render )
            base.taskMgr.add( chunk.update, "update" )
            chunks.append(chunk)

base.graphicsEngine.render_frame()
base.graphicsEngine.render_frame()
for c in chunks:
    c.compute_node_path.detachNode()

def update( task ):

    nodes = []
    nodes.append( Node( index=0, pos=LVector3f(0.5,0,-2.5), size=1.5, profile_index=0 ) )
    nodes.append( Node( index=1, pos=LVector3f(0,0,0), size=0.8, profile_index=1 ) )
    nodes.append( Node( index=2, pos=LVector3f(math.cos(task.time)*4,math.sin(task.time)*4.0, math.sin(task.time*0.5)*0.7), size=1.2, profile_index=2 ) )
    nodes.append( Node( index=3, pos=LVector3f(5,4,0), size=0.8, profile_index=1 ) )
    nodes.append( Node( index=4, pos=LVector3f(-5,-4,2), size=1.0, profile_index=2 ) )

    tunnels = []
    tunnels.append( (nodes[0], nodes[1]) )
    tunnels.append( (nodes[1], nodes[2]) )
    tunnels.append( (nodes[1], nodes[3]) )
    tunnels.append( (nodes[1], nodes[4]) )
    tunnels.append( (nodes[2], nodes[4]) )
    #tunnels.append( (nodes[2], nodes[1]) )

    tunnels_serialized = []
    for t in tunnels:
        node1 = t[0]
        node2 = t[1]
        t_s = []
        t_s += [node1.pos.x, node1.pos.y, node1.pos.z, node1.size]
        t_s += [node2.pos.x, node2.pos.y, node2.pos.z, node2.size]
        t_s += [float(node1.profile_index), float(node2.profile_index)]
        t_s += [0,0]    # padding
        # Pad each array element to 16 bytes:
        #padding = 16 - len(t_s) % 16
        #if padding != 0:
            #t_s += [0.0]*padding

        tunnels_serialized += t_s

    input_shader_buffer = ShaderBuffer("chunk_input",
            array('f', tunnels_serialized ).tobytes(),
            GeomEnums.UH_static )
    for c in chunks:
        #c.input_shader_buffer = input_shader_buffer
        c.compute_node_path.set_shader_input("InputField", input_shader_buffer)
    return task.cont

#base.taskMgr.add( update, "update" )
base.set_background_color(0, 0, 0)
base.setFrameRateMeter(True)

base.cam.set_x(0.5)
base.cam.set_y(-2)
base.cam.set_z(0.5)

base.run()
