import bpy
import math
import mathutils

# Get the active object
obj = bpy.context.active_object
if not obj or obj.type != 'MESH':
    raise TypeError("Please select a mesh object.")

# Switch to object mode just in case
bpy.ops.object.mode_set(mode='OBJECT')

# Add Solidify modifier
solidify_mod = obj.modifiers.new(name="Solidify", type='SOLIDIFY')
#solidify_mod.solidify_mode = 'SIMPLE'
solidify_mod.thickness = 1.75

# Add Triangulate modifier
tri_mod = obj.modifiers.new(name="Triangulate", type='TRIANGULATE')

# Apply both modifiers
bpy.context.view_layer.objects.active = obj
bpy.ops.object.modifier_apply(modifier=solidify_mod.name)
bpy.ops.object.modifier_apply(modifier=tri_mod.name)

mesh = obj.data

# Ensure the mesh has custom split normals
if not mesh.has_custom_normals:
    mesh.create_normals_split()

# Define the target normal direction (world +X)
target_normal = mathutils.Vector((1.0, 0.0, 0.0))

# Create the normal array for every loop
custom_normals = [target_normal] * len(mesh.loops)

# Assign custom split normals
mesh.normals_split_custom_set(custom_normals)

# Update mesh and viewport
mesh.update()
bpy.context.view_layer.update()


# Rotate the object on X axis by -90 degrees

obj.rotation_euler.rotate_axis('X', math.radians(-90))
