#version 430

in vec2 coord;
in vec3 color;

in vec3 normal_worldspace;
in vec2 uv_x;
in vec2 uv_y;
in vec2 uv_z;

uniform sampler2D textureGround;
uniform sampler2D textureWall;

out vec4 p3d_FragColor;


vec3 getTriPlanarBlend(vec3 _wNorm){
	// in wNorm is the world-space normal of the fragment
	vec3 blending = abs( _wNorm );
	blending = normalize(max(blending, 0.00001)); // Force weights to sum to 1.0
	float b = (blending.x + blending.y + blending.z);
	blending /= vec3(b, b, b);
	return blending;
}

void main() {

  vec4 wallTexColX = texture(textureWall, uv_x);
  vec4 wallTexColY = texture(textureWall, uv_y);
  vec4 groundTexCol = texture(textureGround, uv_z);


  vec3 blending = getTriPlanarBlend(normal_worldspace);
  vec4 diffuseCol = wallTexColX*blending.x + wallTexColY*blending.y + groundTexCol*blending.z;

  p3d_FragColor = vec4(diffuseCol.rgb*(0.5*color.r+0.5), 1);
}
