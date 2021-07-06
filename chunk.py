from array import array
import random, math
from panda3d.core import *

profile_textures = TexturePool.load2dTextureArray("Textures/Profile#.png")

class Chunk():

    def __init__( self, voxels_per_side=8, voxel_size=0.15, pos=LVector3f(0,0,0), input_shader_buffer=None ):

        self.num_voxels_per_side = voxels_per_side+1  # padding!
        self.num_voxels = (self.num_voxels_per_side)**3
        self.voxel_size = voxel_size
        self.pos = pos

        scale = 0.6
        self.noise = PerlinNoise3( scale, scale, scale, 
                32,seed = 1 )
        self.textureGround = loader.loadTexture( "Textures/rocks_ground_03_diff_2k.png" )
        self.textureWall = loader.loadTexture( "Textures/rock_wall_02_diff_2k.png" )

        self.input_shader_buffer = input_shader_buffer

        #self.create_input_buffer()
        self.create_geometry_buffer()
        self.create_geometry_node()
        self.create_compute_node()


    #def create_input_buffer( self ):
#
        #data = array('f', field)
        #self.input_shader_buffer = ShaderBuffer('chunk_input', data.tobytes(), GeomEnums.UH_static)

    def create_geometry_buffer( self ):

        vertices = []
        max_points_per_voxel = 15     # Maximum number of verts created per voxel
        for i in range( self.num_voxels*max_points_per_voxel ):
            #vertices += [0,0,0] # position x,y,z
            #vertices += [0,0,0] # normal x,y,z
            #vertices += [random.random(), random.random(), random.random()] # normal x,y,z
            vertices += [0,0,0,0,random.random(),random.random(),random.random(),0]
       
        verts = array('f', vertices)
        self.geom_shader_buffer = ShaderBuffer('chunk_geom', verts.tobytes(), GeomEnums.UH_static)

    def update( self, task ):
        #self.create_input_buffer()
        #self.compute_node_path.set_shader_input("InputField", self.input_shader_buffer)
        #self.compute_node_path.set_shader_input("threshold", math.sin(task.time)*0.2 )
        self.compute_node_path.set_shader_input("threshold", 0 )
        return task.cont

    def create_geometry_node( self ):

        # Create a dummy vertex data object.
        fmt = GeomVertexFormat.get_empty()
        vdata = GeomVertexData('chunk', fmt, GeomEnums.UH_static)

        # This represents a draw call, indicating how many vertices we want to draw.
        tris = GeomTriangles(GeomEnums.UH_static)
        max_points_per_voxel = 15     # Maximum number of verts created per voxel
        tris.add_next_vertices( self.num_voxels * max_points_per_voxel )

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
        self.node_path.set_shader_input( "textureGround", self.textureGround )
        self.node_path.set_shader_input( "textureWall", self.textureWall )

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
        self.compute_node_path.set_shader_input("chunk_position", self.pos )
        self.compute_node_path.set_shader_input("profile_textures", profile_textures )

    def reparent_to( self, parent ):
        self.node_path.reparent_to( parent )


