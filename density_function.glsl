#pragma once

#pragma include "utils.glsl"

struct Tunnel {
  vec3 pos1;
  float size1;
  vec3 pos2;
  float size2;
  float profile_index1; 	// Float to make it easier to pack when sending
  float profile_index2; 	// Float to make it easier to pack when sending
  float _1; 	// padding
  float _2; 	// padding
};

layout(std430,binding=3) readonly buffer InputField {
  Tunnel tunnels[];
};

uniform sampler2DArray profile_textures;

float sampleTunnel( vec3 pos, Tunnel tunnel )
{
	vec3 nodePos1 = tunnel.pos1.xyz;
	vec3 nodePos2 = tunnel.pos2.xyz;
	/*if( true )
	{
		float v1 = tunnel.size1 - length( pos - nodePos1 );
		float v2 = tunnel.size2 - length( pos - nodePos2 );
		return max( v1, v2 );
	}*/

	vec3 projection = closestPointOnSegment( nodePos1, nodePos2, pos );

	// TODO move what's not needed yet after the early abort!
	float tunnelLength = length( nodePos1 - nodePos2 );
	float distAlongPath = length( nodePos1 - projection );
	float amountAlongPath = distAlongPath/tunnelLength;
	float size = tunnel.size2*amountAlongPath + tunnel.size1*(1-amountAlongPath);

	/*if( true )
	{
		return size - length( projection - pos );
	}*/

	vec3 offset = projection - pos;
	float offsetDist = length( offset );

	//if( offsetDist > max( tunnel.size1, tunnel.size2 ) )
	if( offsetDist > size )
		return -1;

	vec3 sideVec = normalize( cross( nodePos1 - nodePos2, vec3(0,0,1) ) );

    float side = dot( offset, sideVec );
	float up = offset.z;

	float s = side/size*0.5 + 0.5;
	float u = up/size*0.5 + 0.5;

    float p1 = texture( profile_textures, vec3( s,u, tunnel.profile_index1 ) ).r;
    float p2 = texture( profile_textures, vec3( s,u, tunnel.profile_index2 ) ).r;
	// TODO: Remove maxsize!
    return p1*amountAlongPath + p2*(1-amountAlongPath) - 0.5;
}


float sampleField( vec3 pos )
{
  float maxVal = -1;
  for( int i = 0; i < tunnels.length(); i++ )
  {
  	maxVal = max( maxVal, sampleTunnel( pos, tunnels[i] ) );
  }
  return maxVal;
}

