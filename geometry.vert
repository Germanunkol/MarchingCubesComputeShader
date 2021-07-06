#version 430

#pragma include "common.glsl"

uniform mat4 p3d_ModelViewMatrix;
uniform mat4 p3d_ProjectionMatrix;

//in vec3 p3d_Normal;

out vec2 coord;
out vec3 color;

out vec3 normal_worldspace;

out vec2 uv_x;
out vec2 uv_y;
out vec2 uv_z;

void main() {
  //int triID = gl_VertexID / 3;

  vec3 local_pos = vertices[gl_VertexID].pos;

  vec4 pos = p3d_ModelViewMatrix * vec4(local_pos,1);

  float brightness = dot( vertices[gl_VertexID].normal, vec3(0,0,1) );
  color = vec3( brightness, brightness, brightness );
  normal_worldspace = vertices[gl_VertexID].normal;

  uv_x = local_pos.yz;
  uv_y = local_pos.xz;
  uv_z = local_pos.xy;

  gl_Position = p3d_ProjectionMatrix * pos;
}
