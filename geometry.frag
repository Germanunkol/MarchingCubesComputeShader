#version 430

in vec2 coord;
in vec3 color;
//in vec3 normal_worldspace;

out vec4 p3d_FragColor;

void main() {
  p3d_FragColor = vec4(color, 1);
}
