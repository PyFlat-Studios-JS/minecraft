from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import json
import hashlib
import time
app = Ursina()
textures = ['mc/bedrock', 'mc/planks', 'mc/wood', 'mc/dirt', 'mc/stone', 'mc/grass', 'mc/diamond']
selected_tex = textures[1]
Sky()
size = (0.5, 0.5, 0.5)
#size = (1, 1, 1)
i = 0
mode = 'Block.obj'
# Define a Voxel class.
# By setting the parent to scene and the model to 'cube' it becomes a 3d button.
iventory = Entity(
            parent = camera.ui,
            model = 'quad',
            scale = (.9, .1),
            origin = (-.5, .5),
            position = (-.4,-.3),
            texture = 'white_cube',
            texture_scale = (9,1),
            color = color.dark_gray
            )
class Chunk():
    global selected_tex, textures
    def __init__(self, x, z):
        self.cx = x
        self.cz = z
        self.block = []
        self.voxels = []
        self.textures = []
        self.loaded = False
        dd = "[" + str(x) + "|" + str(z) + "]"
        self.name = hashlib.md5(dd.encode()).hexdigest()
        for i in range (0,8):
            m = []
            t = []
            for j in range (0,8):
                sx = i + x * 8
                sy = j + z * 8
                position = (sx, 0, sy)
                m.append(position)
                t.append(textures[0])
            self.textures.append(t)
                #voxel = Voxel(position=position)
                
            self.block.append(m)
        print("Initialized Chunk " + self.name)
    def load(self):
        selected_tex = textures[0]
        for i in range (0,8):
            m = i
            for j in range (0,8):
                selected_tex  = self.textures[m][j]
                voxel = Voxel(position=self.block[m][j])
                self.voxels.append(voxel)
        self.loaded=True
        print("Loaded Chunk " + self.name)
        selected_tex = 1
    def unload(self):
        indexer = 0
        for i in range (0, 8):
            for j in range (0, 8):
                self.textures[i][j] = self.voxels[indexer].stexture
                indexer = indexer + 1
        for i in range (0,len(self.voxels)):
            destroy(self.voxels[i])
        self.voxels = []
        print("Unloaded Chunk" + self.name)
        self.loaded = False
class Voxel(Button):
    global selected_tex
    def __init__(self, position=(0,0,0)):
        self.stexture = selected_tex
        super().__init__(
            parent = scene,
            position = position,
            model = mode,
            origin_y = .5,
            texture = selected_tex,
            scale = size,
            color = color.color(0, 0, random.uniform(.9, 1.0)),
            #highlight_color = color.limegreen,
        )
    def input(self, key):
        global textures, selected_tex, i, le
        if self.hovered:
            #print(t)
            if key == 'right mouse down':
                voxel = Voxel(position=self.position + mouse.normal)
            if key == 'left mouse down':
                if str(self.texture) == 'bedrock.png':
                    return
                else:
                    destroy(self)
            if key == 'escape':
                mouse.visible = True
                mouse.position = position
            if key == '1':
                i = 1
                selected_tex = textures[1]
            if key == '2':
                i = 2
                selected_tex = textures[2]
            if key == '3':
                i = 3
                selected_tex = textures[3]
            if key == '4':
                i = 4
                selected_tex = textures[4]
            if key == '5':
                i = 5
                selected_tex = textures[5]
            if key == '6':
                i = 6
                selected_tex = textures[6]  
            if key == 'scroll up':
                if i <= 5:  
                    i += 1
                selected_tex = textures[i]
            if key == 'scroll down':
                if i >= 2:  
                    i -= 1
                selected_tex = textures[i]
def input(key):
    if key == 'r':
        m[0].unload()
    if key == 'm':
        m[0].load()
m = []
z_chunks = 80
x_chunks = 80
for z in range(-1*int(z_chunks / 2), int((z_chunks / 2)+1)):
    for x in range(-1* int(x_chunks / 2), int((x_chunks / 2)+1)):
        a = Chunk(z,x)
        if (z == 0 and x == 0):
            a.load()
        m.append(a)

def update():
    global m
    p = player.position
    x, y, z = p 
    a = str(x/8)
    b = str(z/8)
    ccx = 0
    ccz = 0
    if (float(a) < 0):
        ccx = int(a.split(".")[0]) - 1
    else:
        cx = int(a.split(".")[0])
    if (float(b) < 0):
        ccz = int(b.split(".")[0]) - 1
    else:
        ccz = int(b.split(".")[0])
    #print (str(cx) + str(cz))
    ul = []
    l = []
    for x in range (-2 , 3):
        for z in range (-2, 3):
            for i in range (0, len(m)):
                if (m[i].cx == ccx + x and m[i].cz == ccz + z):
                    if ((x < 2 and x > -2) and (z<2 and z > -2)):
                        l.append(m[i])
                    else:
                        ul.append(m[i])

    for i in range (0, len(l)):
        if (l[i].loaded ==  False):
            l[i].load()
    for i in range (0, len(ul)):
        if (ul[i].loaded == True):
            ul[i].unload()
player = FirstPersonController()
app.run()