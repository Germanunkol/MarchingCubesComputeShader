#version 430

out vec4 p3d_FragColor;

in vec2 coord;
in vec3 color;

void main() {
  p3d_FragColor = vec4(color, 1);
}
