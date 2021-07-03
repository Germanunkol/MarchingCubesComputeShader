from array import array
import random, math
from panda3d.core import *

class Chunk():

    def __init__( self, num_voxels=8, voxel_size=0.15, pos=LVector3f(0,0,0) ):

        self.num_voxels = num_voxels+1  # padding!
        self.voxel_size = voxel_size
        self.pos = pos

        scale = 0.6
        self.noise = PerlinNoise3( scale, scale, scale, 
                32,seed = 1 )

        self.create_input_buffer()
        self.create_geometry_buffer()
        self.create_geometry_node()
        self.create_compute_node()


    def create_input_buffer( self ):

        field = [-1.0]*(self.num_voxels**3)
        i = 0
        for z in range( self.num_voxels ):
            for y in range( self.num_voxels ):
                for x in range( self.num_voxels ):
                    #field[i] = int(100*(x-4+y*0.5*globalClock.getRealTime()*0.1))
                    #field[i] = int(100*(x-4))
                    #field[i] = ( x % 3 - 1 )
                    px = self.pos.x + x*self.voxel_size
                    py = self.pos.y + y*self.voxel_size
                    pz = self.pos.z + z*self.voxel_size
                    py += globalClock.getRealTime()*0.2
                    field[i] = self.noise( px, py, pz )
                    i += 1
        data = array('f', field)
        self.input_shader_buffer = ShaderBuffer('chunk_input', data.tobytes(), GeomEnums.UH_static)

    def create_geometry_buffer( self ):

        vertices = []
        max_tris_per_voxel = 15     # Maximum number of verts created per voxel
        full_num_voxels = (self.num_voxels+1)**3
        for i in range( full_num_voxels*max_tris_per_voxel ):
            vertices += [0,0,0] # x,y,z
       
        verts = array('f', vertices)
        self.geom_shader_buffer = ShaderBuffer('chunk_geom', verts.tobytes(), GeomEnums.UH_static)

    def update( self, task ):
        self.create_input_buffer()
        self.compute_node_path.set_shader_input("InputField", self.input_shader_buffer)
        return task.cont

    def create_geometry_node( self ):

        # Create a dummy vertex data object.
        fmt = GeomVertexFormat.get_empty()
        vdata = GeomVertexData('chunk', fmt, GeomEnums.UH_static)

        # This represents a draw call, indicating how many vertices we want to draw.
        tris = GeomTriangles(GeomEnums.UH_static)
        tris.add_next_vertices( (self.num_voxels**3) * 15)

        # The geom which will be rendered. The empty list of verts will be filled from the
        # ShaderBuffer later on.
        geom = Geom(vdata)
        geom.add_primitive(tris)
        # We need to set a bounding volume so that Panda doesn't try to cull it.
        geom.set_bounds(BoundingBox((0, 0, 0), (1, 1, 1)))

        geom_node = GeomNode("node")
        geom_node.add_geom(geom)

        # Put our node in the scene graph and apply the SSBO.
        shader = Shader.load(Shader.SL_GLSL, "geometry.vert", "geometry.frag")
        self.node_path = NodePath( geom_node )
        self.node_path.set_shader(shader)
        self.node_path.set_shader_input("GeomBuffer", self.geom_shader_buffer)
        self.node_path.set_two_sided(True)
        self.node_path.set_pos( self.pos )
        #self.node_path.set_attrib(ColorBlendAttrib.make(ColorBlendAttrib.M_add, ColorBlendAttrib.O_incoming_alpha, ColorBlendAttrib.O_one))
        self.node_path.node().set_bounds_type(BoundingVolume.BT_box)

    def create_compute_node( self ):

        compute_node = ComputeNode("simulate")
        compute_node.add_dispatch( 1, 1, 1 )

        # Add compute node to the scene graph:
        self.compute_node_path = self.node_path.attach_new_node( compute_node )

        shader = Shader.load_compute(Shader.SL_GLSL, "geometry.comp")
        self.compute_node_path.set_shader( shader )
        self.compute_node_path.set_shader_input("InputField", self.input_shader_buffer)
        self.compute_node_path.set_shader_input("GeomBuffer", self.geom_shader_buffer)
        self.compute_node_path.set_shader_input("voxel_size", self.voxel_size)
        self.compute_node_path.set_shader_input("threshold", 0 )

    def reparent_to( self, parent ):
        self.node_path.reparent_to( parent )


