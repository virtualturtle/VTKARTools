import bpy
import math

#Select armature ending in "_skeleton" and rotate it
bpy.ops.object.select_all(action='DESELECT')

skeleton_armature = None
for obj in bpy.data.objects:
    if obj.type == 'ARMATURE' and obj.name.endswith("_skeleton"):
        skeleton_armature = obj
        break

if skeleton_armature:
    bpy.context.view_layer.objects.active = skeleton_armature
    skeleton_armature.select_set(True)

    # Rotate on X by 90 degrees
    skeleton_armature.rotation_euler[0] += math.radians(90)

    # Apply rotation
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)

    # Delete bones starting with "Joint_"
    bpy.ops.object.mode_set(mode='EDIT')
    edit_bones = skeleton_armature.data.edit_bones
    bones_to_delete = [b for b in edit_bones if b.name.startswith("Joint_")]
    for bone in bones_to_delete:
        edit_bones.remove(bone)
    bpy.ops.object.mode_set(mode='OBJECT')

    # Delete all non-armature objects that DON'T start with "Joint_"
    to_delete = [obj for obj in bpy.data.objects 
                 if obj.type != 'ARMATURE' and not obj.name.startswith("Joint_")]
    for obj in to_delete:
        bpy.data.objects.remove(obj, do_unlink=True)

    # Clear Parent (Keep Transform) for all objects starting with "Joint_"
    joint_objects = [obj for obj in bpy.data.objects if obj.name.startswith("Joint_")]
    for obj in joint_objects:
        obj.select_set(True)
    bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')
    bpy.ops.object.select_all(action='DESELECT')

    # Delete armatures that don't end in "_skeleton"
    other_armatures = [obj for obj in bpy.data.objects 
                       if obj.type == 'ARMATURE' and not obj.name.endswith("_skeleton")]
    for obj in other_armatures:
        bpy.data.objects.remove(obj, do_unlink=True)

    # Parent all mesh objects to "_skeleton" armature (Empty Groups)
    mesh_objects = [obj for obj in bpy.data.objects if obj.type == 'MESH']
    for obj in mesh_objects:
        obj.select_set(True)
    skeleton_armature.select_set(True)
    bpy.context.view_layer.objects.active = skeleton_armature
    bpy.ops.object.parent_set(type='ARMATURE_NAME')  # Armature Deform with Empty Groups
    bpy.ops.object.select_all(action='DESELECT')

    # Move everything into a collection matching armature base name
    base_name = skeleton_armature.name.removesuffix("_skeleton")
    target_collection = bpy.data.collections.get(base_name)
    if not target_collection:
        target_collection = bpy.data.collections.new(base_name)
        bpy.context.scene.collection.children.link(target_collection)

    # Move all remaining objects into the target collection
    for obj in bpy.data.objects:
        for coll in obj.users_collection:
            coll.objects.unlink(obj)
        target_collection.objects.link(obj)

    # Delete default "Collection" if it exists
    default_coll = bpy.data.collections.get("Collection")
    if default_coll:
        bpy.data.collections.remove(default_coll)

    print(f"Script completed successfully. All objects moved into collection '{base_name}'.")
else:
    print("No armature ending with '_skeleton' found.")
