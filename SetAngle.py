import bpy
import bmesh
from bmesh.types import BMVert
import math
from math import radians
from math import degrees
from math import pi
import mathutils
from mathutils import geometry
from mathutils import Vector, Matrix, Quaternion, Euler


# from pynput.keyboard import Key, Controller

# keyboard = Controller()


def check(self):
    obj = bpy.context.object

    # Check scale
    if obj.scale != Vector((1.0, 1.0, 1.0)) or obj.delta_scale != Vector((1.0, 1.0, 1.0)):
        bpy.ops.object.dialog_warning_operator('INVOKE_DEFAULT') 
    
        
def check3(self):
    obj = bpy.context.object
    text = "You need to select 3 vertices"
    war = "ERROR"
    self.report({war}, text)


class SetAngle(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "mesh.change_angle"
    bl_label = "Set Angle"
    bl_description = "Set Angle \n You can also assign shortcut \n How to do it: > right-click on this button > Assign Shortcut"
    bl_options = {'REGISTER', 'UNDO'}

    
    @classmethod
    def poll(cls, context):
        return context.active_object is not None    

    def execute(self, context):
                
        check(self)

        # bpy.context.object.update_from_editmode()

        # Get values
        height = bpy.context.window_manager.setprecisemesh.angle
        bool = bpy.context.window_manager.setprecisemesh.anglebool
        bool2 = bpy.context.window_manager.setprecisemesh.angleinput

        
        obj = bpy.context.edit_object
        me = obj.data
        bm = bmesh.from_edit_mesh(me)

        bpy.context.object.update_from_editmode()
        bmesh.update_edit_mesh(me, True, True)
        
        #Create lists
        vec = []
        ind = []

        #Append to lists
        for g in bm.select_history:
            # if len(vec)<3:
                vec.append(bm.verts[g.index].co)
                ind.append(g.index)


        # Check number
        # if len(vec)<3:
            # check3(self)
            # return{"FINISHED"}


        prog = context.window_manager.setprecisemesh.projection_type
        bpy.context.object.update_from_editmode()
        bmesh.update_edit_mesh(me, True, True)

        boolcheck = 0
        lenvec = 0


        # Check list of selected vertices
        if len(vec) == 4:
            length_selcted_vert = 1
            v0=vec[0] # 1 selected
            v1=vec[1] # 2 selected
            v2=vec[2] # 3 selected
            v3=vec[3] # 4 selected
            oldv3=vec[3] # 4 selected

        elif len(vec)==2:
            length_selcted_vert = 0
            boolcheck = 0
            lenvec = 1

            v2=vec[0] # 2 selected
            v3=vec[1] #  3 selected
            oldv3=vec[1] # 3 selected

            # Differrent cases for progection
            prog = context.window_manager.setprecisemesh.projection_type


            if prog == "global_matrix":

                bpy.context.object.update_from_editmode()
                bmesh.update_edit_mesh(me, True, True)

                v2_prg = bpy.context.active_object.matrix_world  @ v2
                v1 = bpy.context.active_object.matrix_world  @ v3

                wm = bpy.context.active_object.matrix_world.copy()
                wm = wm.inverted()
                              
                v1 = mathutils.Vector((v1[0], v1[1] , v2_prg[2])) # 1 selected simulate
                
                v3_prg = bpy.context.active_object.matrix_world  @ v3
                if v3_prg == v1 :
                    print("global matrix 1")
                    boolcheck = 1
                    v3 = mathutils.Vector((  v3_prg[0] , v3_prg[1] , (v2_prg[2] + 1.0)  ))
                    v3 = wm @ v3
                    oldv3 = v3
                # oldv3 = v3
                v1 = wm @ v1  
                
                ind.append(ind[1])
                print("global matrix")

                bpy.context.object.update_from_editmode()
                bmesh.update_edit_mesh(me, True, True)

            elif prog == "local_matrix":

                v2_prg = v2
                v1 = v3
                v1 = mathutils.Vector((v1[0], v1[1] , v2_prg[2])) # 1 selected simulate

                v3_prg = v3
                if v3_prg == v1 :
                    boolcheck = 1
                    v3 = mathutils.Vector((  v3_prg[0] , v3_prg[1] , (v2_prg[2] + 10.0)  ))
                    # v3 = wm @ v3
                    oldv3 = v3

                ind.append(ind[1])

            elif prog == "cursor_location":
                wm = bpy.context.active_object.matrix_world.copy()
                wm = wm.inverted()

                v3_prg = bpy.context.active_object.matrix_world  @ v3
                v2_prg =  bpy.context.active_object.matrix_world @ v2

                v1 = bpy.context.scene.cursor.location

                v1 = wm @ v1

                v1ch=v1-v2
                v3ch=v3-v2
                angle = v3ch.angle(v1ch, 0.0)
                print(angle, "angle1111111111111")
                # if length_intersect != 0:

                if angle == 0.0 :
                    print("Warning you need tp make it")
                
                ind.append(ind[1])                  

            elif prog == "cursor_matrix":

                wm = bpy.context.active_object.matrix_world.copy()
                wm_c = bpy.context.scene.cursor.matrix.copy()
                mat_cur = wm @ wm_c

                # wm = wm.inverted()
                # wm_c = wm_c.inverted()

                # v2_prg = bpy.context.active_object.matrix_world  @ v2
                v2_prg =  v2
                v2_prg = mat_cur  @ v2_prg

                # v1 = bpy.context.active_object.matrix_world  @ v3
                v1 =  v3
                v1 = mat_cur @ v1
                
                v1 = mathutils.Vector((v1[0], v1[1] , v2_prg[2])) # 1 selected simulate
                
                # v3_prg = bpy.context.active_object.matrix_world  @ v3
                v3_prg =  v3
                v3_prg = mat_cur @ v3_prg

                print(v3_prg)
                print(v1)

                wm = wm.inverted()
                wm_c = wm_c.inverted()
                mat_cur = mat_cur.inverted()

                if v3_prg == v1:
                    print("Enter")
                    boolcheck = 1
                    v3 = mathutils.Vector((  v3_prg[0] , v3_prg[1] , (v2_prg[2] + 10.0)  ))
                    # v3 = bpy.context.scene.cursor.matrix @ v3
                    v3 = mat_cur @ v3
                    oldv3 = v3
                    print("Out ")

                # v1 = bpy.context.scene.cursor.matrix @ v1
                v1 = mat_cur @ v1
                ind.append(ind[1])

            elif prog == "custom_object_location": 

                obj_name = bpy.data.scenes[bpy.context.scene.name_full].my_property.name_full

                obj_marx = bpy.data.objects[obj_name].matrix_world
                obj_loc = bpy.data.objects[obj_name].location

                wm = bpy.context.active_object.matrix_world.copy()
                wm = wm.inverted()

                v1 = obj_loc
                v1 = wm @ v1  

                ind.append(ind[1])

            elif prog == "custom_object_matrix":

                obj_name = bpy.data.scenes[bpy.context.scene.name_full].my_property.name_full

                wm = bpy.context.active_object.matrix_world.copy()
                obj_marx = bpy.data.objects[obj_name].matrix_world
                wm_c = obj_marx.copy()

                # mat = wm @ wm_c
                mat = wm_c


                # v2_prg = bpy.context.active_object.matrix_world  @ v2
                v2_prg =  v2
                v2_prg =  mat @ v2_prg

                v1 = v3
                v1 = mat @ v1
                
                v1 = mathutils.Vector((v1[0], v1[1] , v2_prg[2])) # 1 selected simulate
                
                v3_prg =  v3
                v3_prg = mat @ v3_prg

                wm = wm.inverted()
                wm_c = wm_c.inverted()
                mat = mat.inverted()

                # v3_prg = bpy.context.active_object.matrix_world  @ v3
                if v3_prg == v1 :
                    boolcheck = 1
                    v3 = mathutils.Vector((  v3_prg[0] , v3_prg[1] , (v2_prg[2] + 10.0)  ))
                    v3 = mat @ v3
                    oldv3 = v3
                    print("WWWWWWWWOOOOOOOOOORRRRRRRKKKKKKKSSSSSSS")


                v1 = mat @ v1
                # v1 = wm @ v1

                ind.append(ind[1])
        else:
            length_selcted_vert = 0
            v1=vec[0] # 1 selected
            v2=vec[1] # 2 selected
            v3=vec[2] #  3 selected
            oldv3=vec[2] # 3 selected

        bpy.context.object.update_from_editmode()
        bmesh.update_edit_mesh(me, True, True)
        # If projection of angle = angle
        # wm = bpy.context.active_object.matrix_world.copy()
        # wm = wm.inverted()
        # v1_prg = bpy.context.active_object.matrix_world  @ v1

        
            # v1 = wm @ v1_prg
    
        # Angle between verteses
        v1ch=v1-v2
        v3ch=v3-v2

        if boolcheck == 1:
            angle = 0.0
        else:
            angle = v3ch.angle(v1ch, 0.0)

        # v3_prg = bpy.context.active_object.matrix_world  @ v3
        # if v3 == v1 :
            # v3 = mathutils.Vector((  v3_prg[0] , v3_prg[1] , (v2_prg[2] + 0.1)  ))
        
        # print(angle, 111111111111)
        # else:
            # angle = v3ch.angle(v1ch, 0.0)
            # print(angle)


        bmesh.update_edit_mesh(me, True, True)
        # Select cases for number of selected vertices
        if length_selcted_vert == 1:
            # Select vertices
            bm.verts[ind[0]].select = 0
            bm.verts[ind[1]].select = 0
            bm.verts[ind[2]].select = 0
            bm.verts[ind[3]].select = 1

        else:
            # Select vertices
            bm.verts[ind[0]].select = 0
            bm.verts[ind[1]].select = 0
            bm.verts[ind[2]].select = 1



        context = bpy.context
        scene = context.scene
        ob = context.edit_object

        #pp = Cursor location
        if prog != "cursor_location" and prog != "cursor_matrix":
            bpy.context.scene.cursor.location = bpy.context.active_object.matrix_world  @ v2
        

        # Create global coordinates
        vec1 = bpy.context.active_object.matrix_world  @ v1
        vec2 = bpy.context.active_object.matrix_world  @ v2
        vec3 = bpy.context.active_object.matrix_world  @ v3
         

        # Calculate global normal
        normallistgl = [vec1,vec2,vec3]
        normalgl = mathutils.geometry.normal(normallistgl)


        # Calculate local normal
        normallist = [v1,v2,v3]
        normal = mathutils.geometry.normal(normallist)

         
        # Set cursor direction
        if prog != "cursor_location" and prog != "cursor_matrix":
            obj_camera = bpy.data.scenes[bpy.context.scene.name_full].cursor
            loc_camera = bpy.data.scenes[bpy.context.scene.name_full].cursor.matrix.to_translation()         
            direction = normalgl
            # point the cameras '-Z' and use its 'Y' as up
            rot_quat = direction.to_track_quat('-Z', 'Y')
            obj_camera.rotation_euler = rot_quat.to_euler()
        

        # Create Matrix
        mat_loc =  mathutils.Matrix.Translation(( 0.0 ,  0.0 ,  0.0 ))        
        mat_sca =  mathutils.Matrix.Scale( 1.0 ,  4 ,  ( 0.0 ,  0.0 ,  1.0 ))
        mat_rot =  mathutils.Matrix.Rotation(0 ,  4 , "Z" )

        mat_out =  mat_loc @  mat_rot @  mat_sca


        S = mat_out
        pp = v2
        S.translation -= pp      
        
        
        if bool2 == 1:              
            R = Matrix.Rotation(angle, 4, (normal))
            
            bmesh.ops.rotate(bm, 
                    matrix=R,        
                    verts=[v for v in bm.verts if v.select],
                    space=S,
                    )
            bpy.context.scene.tool_settings.transform_pivot_point = 'CURSOR'

                        
            bpy.context.object.update_from_editmode()
            bmesh.update_edit_mesh(me, True, True)


            bpy.ops.transform.rotate("INVOKE_DEFAULT")
            # bpy.context.active_operator.options.use_cursor_region = True
        

            bpy.context.object.update_from_editmode()
            bmesh.update_edit_mesh(me, True, True)
            
            
        else:
            
            
            R = Matrix.Rotation(angle-height, 4, (normal))
            
            bmesh.ops.rotate(bm, 
                    matrix=R,        
                    verts=[v for v in bm.verts if v.select],
                    space=S,
            )    
        
        
        if bool == 1:
            
            obj = context.active_object
            bpy.context.object.update_from_editmode()
            bmesh.update_edit_mesh(me, True, True)

            if length_selcted_vert == 1:

                bmesh.update_edit_mesh(me, True, True)

                newv3 = obj.data.vertices[ind[3]].co

                #New position
                iv1=v2
                # iv2=newv3
                iv2=oldv3

                #Old position
                iv3=v0
                # iv4=oldv3
                iv4=newv3

                
                

                iv = geometry.intersect_line_line(iv1, iv2, iv3, iv4)
                if iv:
                    iv = (iv[0] + iv[1]) / 2

                    bm.verts[ind[3]].co = iv
                    
                    bpy.context.object.update_from_editmode()
                    bmesh.update_edit_mesh(me, True, True)

            else:     
                bpy.context.object.update_from_editmode()
                bmesh.update_edit_mesh(me, True, True)

                if  lenvec == 1:
                    newv3 = obj.data.vertices[ind[1]].co
                else:
                    newv3 = obj.data.vertices[ind[2]].co
                
                # iv1=v1
                # iv2=newv3
                # iv3=v2
                # iv4=oldv3

                iv1=v1
                iv2=oldv3
                iv3=v2
                iv4=newv3

                print(iv1, iv2, iv3, iv4, "qqqqqqqqqqqqqqq")
                
                iv = geometry.intersect_line_line(iv1, iv2, iv3, iv4)
                if iv:
                    iv = (iv[0] + iv[1]) / 2

                    bm.verts[ind[2]].co = iv
                    
                    
                    bpy.context.object.update_from_editmode()
                    bmesh.update_edit_mesh(me, True, True)
            

        
        bpy.context.object.update_from_editmode()
        bmesh.update_edit_mesh(me, True, True)

        
         
        return {'FINISHED'}
if __name__ == "__main__":
    register()
