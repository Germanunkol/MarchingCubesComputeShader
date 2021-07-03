#pragma once

struct Vertex {
  vec3 pos;
};

layout(std430, binding=1) buffer GeomBuffer {
  Vertex vertices[];
};
