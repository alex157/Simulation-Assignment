import math

node = hou.pwd()
geo = node.geometry()

# Add code to modify contents of geo.
# Use drop down menu to select examples.

freq = node.evalParm("frequency")
phase = node.evalParm("phase")
amp = node.evalParm("amplitude")

#access the parameter of ramp color
ramp = node.parm("color").evalAsRamp()

#next we store all the points
points = geo.points()
cd = geo.addAttrib(hou.attribType.Point, "Cd", (1.0,1.0,1.0)) #add the attribute of color, 1 1 1 default value of vector

#first create a list with only the white values
ypos = [p.position()[1] for p in points]
miny = min(ypos) #set the lowest point on y before deformation
maxy = max(ypos)

#height variable
height = maxy - miny
v = 1.0/height #store the value to multiply the position wave. 

#set the sin wave
for p in points: #p is a single point
    pos = p.position() #getting the position of that point
    x = pos[0] #0 will give us x, pos is a list with three values x,y and z
    z = pos[2] #wave will be moving along z
    y = pos[1] + math.sin(z*phase + (hou.frame()*freq))*amp #grab the curve position that I already have and add on top of that the sin wave
    #if we delete pos[1] we lose the original deformation. so we keep it and add the sin function on top of it
    p.setPosition([x,y,z])
    
    #get the look of the value
    lv = (pos[1] - miny)*v #retrn a value between zero and one
    color = ramp.lookup(lv) #get color based on that value
    p.setAttribValue(cd, color)    #set the color attribute
