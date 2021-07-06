#pragma once

vec3 closestPointOnSegment( vec3 a, vec3 b, vec3 p )
{
    vec3 ap = p-a;
    vec3 ab = b-a;
    float dist = dot(ap,ab)/dot(ab,ab);
    if( dist < 0 )
        return a;
    if( dist > 1 )
        return b;
    vec3 result = a + ab * dist;
    return result;
}

