#version 430

#pragma include "common.glsl"

uniform mat4 p3d_ModelViewMatrix;
uniform mat4 p3d_ProjectionMatrix;

out vec2 coord;
out vec3 color;

void main() {
  //int triID = gl_VertexID / 3;

  vec4 pos = p3d_ModelViewMatrix * vec4(vertices[gl_VertexID].pos, 1);

  /*int vtxID = gl_VertexID % 3;
  if( vtxID == 0 )
	  color = vec3(1, 1, 1);
  else if( vtxID == 1 )
	  color = vec3(1, 1, 0.5);
  else
	  color = vec3(1, 0.5, 1);*/

  color = vertices[gl_VertexID].pos;
  //color = vec3(1, 0.5, 1);

  gl_Position = p3d_ProjectionMatrix * pos;
}
