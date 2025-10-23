import bpy

# Target and Source Armature names
SOURCE_RIG_NAME = "SOURCERIG"
TARGET_RIG_NAME = "TARGETRIG"

# Get armature objects
source_rig = bpy.data.objects.get(SOURCE_RIG_NAME)
target_rig = bpy.data.objects.get(TARGET_RIG_NAME)

if not source_rig or not target_rig:
    raise ValueError("Could not find one or both armatures: check the names.")

# Make sure we’re in Object mode
bpy.ops.object.mode_set(mode='OBJECT')

# Enter Pose Mode for the target rig
bpy.context.view_layer.objects.active = target_rig
bpy.ops.object.mode_set(mode='POSE')

# Loop through each bone in the target rig
for bone_name, pbone in target_rig.pose.bones.items():
    # Check if the same bone exists in the source rig
    if bone_name in source_rig.pose.bones:
        # Create a new Copy Transforms constraint
        constraint = pbone.constraints.new(type='COPY_TRANSFORMS')
        constraint.name = "Copy Transforms from SOURCERIG"
        constraint.target = source_rig
        constraint.subtarget = bone_name
        print(f"Added Copy Transforms constraint for bone: {bone_name}")
    else:
        print(f"Bone '{bone_name}' not found in {SOURCE_RIG_NAME}, skipping.")

# Return to Object Mode
bpy.ops.object.mode_set(mode='OBJECT')

print("✅ All matching bones now have Copy Transforms constraints.")
