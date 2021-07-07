#pragma once

struct Vertex {
  vec3 pos;
  float _1;
  vec3 normal;
  float _2;
};

layout(std430, binding=1) buffer GeomBuffer {
  Vertex vertices[];
};
