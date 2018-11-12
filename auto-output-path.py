bl_info = {
    "name": "Auto Output Path",
    "author": "Jahnertz",
    "version": (1.0),
    "location": "Properties > Render Tab",
    "description": "A simple control panel for quickly creating a meaningful output paths for blender renders.",
    "warning": "",
    "category": "Render"
    }

import bpy
import os

class OutputFilenamePropertyGroup(bpy.types.PropertyGroup):
    num_digits = bpy.props.IntProperty(name = "Digits", subtype = 'UNSIGNED')
    prefix = bpy.props.StringProperty(name = "Prefix")
    suffix = bpy.props.StringProperty(name = "Suffix")
    annotation = bpy.props.StringProperty(name = "Annotation")
    destination = bpy.props.StringProperty(name = "Destination Folder", subtype = 'DIR_PATH')
    subfolder = bpy.props.BoolProperty(name = "Place in Subfolder")

bpy.utils.register_class(OutputFilenamePropertyGroup)

bpy.types.Scene.output_filename_props = bpy.props.PointerProperty(type=OutputFilenamePropertyGroup)
bpy.context.scene.output_filename_props.num_digits = 3
# bpy.context.scene.output_filename_props.prefix = ""
# bpy.context.scene.output_filename_props.destination = ""

def setOutputFilename( context ):
    prop_grp = context.scene.output_filename_props
    projectname = bpy.path.basename(context.blend_data.filepath)
    projectname = os.path.splitext(projectname)[0]
    filename = prop_grp.destination
    if (prop_grp.subfolder == True):
        filename = '/' + filename + \
        str(projectname) + '_' + \
        str(context.scene.name) + '/'
    filename = filename + str(prop_grp.prefix) + str(projectname) + '_' + str(context.scene.name) + str(prop_grp.suffix) + '_' + ('#' * prop_grp.num_digits) + str(prop_grp.annotation)
    context.scene.render.filepath = filename

class SetThisSceneOutputFilenameOperator(bpy.types.Operator):
    bl_idname = "wm.set_scene_output_filename"
    bl_label = "Set Output Filenames"
    def execute(self, context):
        # Set the output filename for current scene:
        setOutputFilename(bpy.context)
        return {'FINISHED'}

bpy.utils.register_class(SetThisSceneOutputFilenameOperator)

class SetAllScenesOutputFilenamesOperator(bpy.types.Operator):
    bl_idname = "wm.set_all_scenes_output_filenames"
    bl_label = "Set Output Filenames"
    def execute(self, context):
        # Set the output filename for all scenes
        for scene in bpy.data.scenes:
            bpy.context.screen.scene = scene
            setOutputFilename(bpy.context)
        return {'FINISHED'}

bpy.utils.register_class(SetAllScenesOutputFilenamesOperator)

class AutoOutputNamePanel(bpy.types.Panel):
    """Creates a Panel in the Render properties window"""
    bl_label = "Auto Output Name"
    bl_idname = "OBJECT_PT_Auto_Output_Name"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "render"

    def draw(self, context):
        prop_grp = bpy.context.scene.output_filename_props
        layout = self.layout
        col = layout.column(align=True)
        row = layout.row(align=True)
        row.prop(prop_grp, "destination")
        row.prop(prop_grp, "subfolder")
        row = layout.row(align=True)
        row.prop(prop_grp, "prefix")
        row.prop(prop_grp, "suffix")
        row = layout.row(align=True)
        row.prop(prop_grp, "num_digits")
        row.prop(prop_grp, "annotation")
        row = layout.row(align=True)
        row.label(text="Set Output Filename:")
        row.operator("wm.set_scene_output_filename", text="This Scene")
        # row.operator("wm.set_all_scenes_output_filenames", text="All Scenes", icon="ERROR") TODO: This button should use the same settings and apply it to all scenes.

def register():
    bpy.utils.register_class(AutoOutputNamePanel)

def unregister():
    bpy.utils.unregister_class(AutoOutputName)

if __name__ == "__main__":
    register()
