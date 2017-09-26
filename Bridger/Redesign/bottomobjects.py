"""
Move object origins to lowest Z point
Usage:
    - Select objects (only moves mesh object origins from those)
    - Apply rotation and scale (ctrl+a -> rotation & scale)
    - Move object origins to geometry (ctrl+alt+shift+c -> origin to geometry)
    - Run script
"""

import bpy 
import mathutils
from mathutils import Vector

objects = bpy.context.selected_objects

for obj in objects:
    if(obj.type == "MESH"):
                
        vertex_coordinate = ""
        for vertex in obj.data.vertices:
            if((vertex_coordinate == "") or (vertex.co.z < vertex_coordinate.z)):
                vertex_coordinate = vertex.co
        
        vertex_global_coordinate = obj.matrix_world * vertex_coordinate
        offset = (obj.location.x, obj.location.y, vertex_global_coordinate.z)
        new_location = offset
        offset = Vector(offset)
        offset = offset - obj.location
        
        for vertex in obj.data.vertices:
            vertex.co = vertex.co - offset
        
        obj.location = new_location