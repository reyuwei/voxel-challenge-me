from scene import Scene
import taichi as ti
from taichi.math import *

scene = Scene(exposure=1, voxel_edges=0.0)
scene.set_floor(0, (1.0, 1.0, 1.0))

@ti.func
def create_block(pos, size, color, color_noise, btype=1):
    for I in ti.grouped(
            ti.ndrange((pos[0], pos[0] + size[0]),
                       (pos[1], pos[1] + size[1]),
                       (pos[2], pos[2] + size[2]))):
        scene.set_voxel(I, btype, color + color_noise * ti.random())


@ti.func
def create_light_saber(pos, length, radius, light_color):
    base = ti.cast(length * 0.3, ti.int16)
    base = base + ti.raw_mod(base, 3)
    light_len = ti.cast(length * 0.7, ti.int16)
    pos_light = ivec3(pos[0], pos[1] + base, pos[2])

    base_color_gray = vec3(0.5, 0.5, 0.5)
    base_color_black = vec3(0, 0, 0)

    create_block(pos=ivec3(pos[0], pos[1], pos[2]), size=ivec3(radius, 1, radius), color=base_color_gray, color_noise=vec3(0.1), btype=1)
    create_block(pos=ivec3(pos[0], pos[1]+1, pos[2]), size=ivec3(radius, base/3, radius), color=base_color_black, color_noise=vec3(0), btype=1)
    create_block(pos=ivec3(pos[0], pos[1]+1+base/3, pos[2]), size=ivec3(radius, 1, radius), color=base_color_gray, color_noise=vec3(0.1), btype=1)
    create_block(pos=ivec3(pos[0], pos[1]+2+base/3, pos[2]), size=ivec3(radius, base/3, radius), color=base_color_black, color_noise=vec3(0), btype=1)
    create_block(pos=ivec3(pos[0], pos[1]+1+2*base/3, pos[2]), size=ivec3(radius, base/3, radius), color=base_color_gray, color_noise=vec3(0), btype=1)
    create_block(pos=pos_light, size=ivec3(radius, light_len, radius), color=light_color, color_noise=vec3(0), btype=2)

@ti.func
def rgb(r, g, b):
    return vec3(r/255.0, g/255.0, b/255.0)

@ti.kernel
def initialize_voxels():
    lcolor_1 = vec3(59, 129, 150)
    lcolor_2 = vec3(215, 32, 39)
    lcolor_3 = vec3(211, 91, 27)
    lcolor_4 = vec3(59, 78, 155)
    lcolor_5 = vec3(182, 159, 54)
    lcolor_6 = vec3(192, 58, 255)
    lcolor_7 = vec3(33, 188, 30)
    lcolor_8 = vec3(74, 131, 163)

    # Your code here! :-)
    for i in range(100):
        x = ti.random() * 124 - 62
        z = ti.random() * 124 - 62
        
        randradius = ti.cast(max(ti.random() * 3, 1), ti.int16)
        randheight = max(ti.random() * 63, 10)

        light_id = ti.cast(ti.random() * 8, ti.int16)
        randcolor = rgb(lcolor_8[0], lcolor_8[1], lcolor_8[2])                
        if light_id == 0:     randcolor = rgb(lcolor_1[0], lcolor_1[1], lcolor_1[2])
        elif light_id == 1:   randcolor = rgb(lcolor_2[0], lcolor_2[1], lcolor_2[2])
        elif light_id == 2:   randcolor = rgb(lcolor_3[0], lcolor_3[1], lcolor_3[2])
        elif light_id == 3:   randcolor = rgb(lcolor_4[0], lcolor_4[1], lcolor_4[2])            
        elif light_id == 4:   randcolor = rgb(lcolor_5[0], lcolor_5[1], lcolor_5[2])
        elif light_id == 5:   randcolor = rgb(lcolor_6[0], lcolor_6[1], lcolor_6[2])
        elif light_id == 6:   randcolor = rgb(lcolor_7[0], lcolor_7[1], lcolor_7[2])
        elif light_id == 7:   randcolor = rgb(lcolor_8[0], lcolor_8[1], lcolor_8[2])                            

        create_light_saber(vec3(x, 0, z), randheight, randradius, randcolor)


initialize_voxels()
scene.finish()
