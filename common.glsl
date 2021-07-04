#pragma once

struct Vertex {
  vec3 pos;
  float scale;
  vec3 normal;
  float size;
};

layout(std430, binding=1) buffer GeomBuffer {
  Vertex vertices[];
};
