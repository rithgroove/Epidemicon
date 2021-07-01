import tkinter 
import platform
import time
import threading

osmMap = None
sim = None
windowSize = (1024,768)
viewPort = (0,0)
canvasOrigin = None
canvasMax = None
canvasSize = None
scale = None 
prevPosition = None
canvas = None
OS = platform.system()
animating = False

def motion(event):
    global prevPosition
    global viewPort
    global canvas
    global canvasSize
    global windowSize
    if prevPosition is not None:
        translation = (prevPosition[0]-event.x, prevPosition[1]-event.y)
        viewPort = (viewPort[0]-translation[0], viewPort[1]- translation[1])
        #print(translation)
        if (viewPort[0] > 0):
            viewPort = (0, viewPort[1])
        elif (viewPort[0] < -1* scale *canvasSize[0] + windowSize[0]):
            #print("too far x")
            viewPort = (int( -1* scale *canvasSize[0] + windowSize[0]),viewPort[1])
        if (viewPort[1] > 0):
            viewPort = (viewPort[0], 0)
        elif (viewPort[1] < -1* scale *canvasSize[1] + windowSize[1]):
            #print("too far y")
            viewPort = (viewPort[0], int( -1* scale *canvasSize[1] + windowSize[1]))
        
    prevPosition = (event.x,event.y)
    canvas.scan_dragto(viewPort[0], viewPort[1], gain=1)
    #draw()
    #print("Mouse position: (%s %s)" % (event.x, event.y))
    #print("Root position: (%s %s)" % (event.x_root, event.y_root))
    return

def clickRelease(event):
    global prevPosition
    prevPosition = None

def doubleClick(event):
    global animating
    print("double click")
    animating = not animating
    
def start():
    global animating
    while(1):
        if (animating):
            sim.step()
            print("finish stepping")
        time.sleep(10)
        
def step():
    global lastStep 
    if lastStep != sim.stepCount:
        for x in sim.agents:
            moveAgent(x)
        lastStep = sim.stepCount
    canvas.after(1000,step)
        
def scroll(event):
    global canvas
    global viewPort
    global scale
    value = -1*(event.delta)
    #print(f"Scrolling {value}")
    if OS == 'Linux':
        if event.num == 4:
            canvas.scale('all', 0, 0, 1.1, 1.1)
            scale *=  1.1
        elif event.num == 5:
            canvas.scale('all', 0, 0, 10.0/11.0, 10.0/11.0)
            scale *= (10.0/11.0)
    else:          
        if (value > 0):
            canvas.scale('all', 0, 0,1.1, 1.1)
            scale *=  1.1
        elif (value <0):
            canvas.scale('all', 0, 0, 10.0/11.0, 10.0/11.0)
            scale *= (10.0/11.0)

#def resize(event):
    #global canvas
    #region = canvas.bbox(tkinter.ALL)
    #print(region)
    #windowsSize = (,)
    #canvas.configure(scrollregion=region)      
            
def draw():
    for temp in osmMap.amenities:
        path = []
        for node in temp.nodes:
            x = (node.coordinate.lon - canvasOrigin[0]) * scale +viewPort[0]
            y = (canvasSize[1]-( node.coordinate.lat - canvasOrigin[1])) * scale + viewPort[1]
            path.append(x)
            path.append(y)
        if (path.__len__() > 6):
            outline = '#CCCCCC'
            fill = '#DDDDDD'
            
            if (temp.tags['amenity'] == 'school'):
                outline = '#515464'
                fill = '#CCCCCC'
            elif (temp.tags['amenity'] == 'police'):
                outline = '#515464'
                fill = '#CCCCCC'
            elif (temp.tags['amenity'] == 'karaoke_box'):
                outline = '#515464'
                fill = '#CCCCCC'
            elif (temp.tags['amenity'] == 'university'):
                outline = '#619e44'
                fill = '#9edd80'
            elif (temp.tags['amenity'] == 'library'):
                outline = '#515464'
                fill = '#CCCCCC'
            elif (temp.tags['amenity'] == 'driving_school'):
                outline = '#515464'
                fill = '#CCCCCC'
            elif (temp.tags['amenity'] == 'bus_station'):
                outline = '#515464'
                fill = '#CCCCCC'
            elif (temp.tags['amenity'] == 'kindergarten'):
                outline = '#515464'
                fill = '#CCCCCC'
            elif (temp.tags['amenity'] == 'post_office'):
                outline = '#515464'
                fill = '#CCCCCC'
            elif (temp.tags['amenity'] == 'community_centre'):
                outline = '#515464'
                fill = '#CCCCCC'
            elif (temp.tags['amenity'] == 'toilets'):
                outline = '#515464'
                fill = '#CCCCCC'
            elif (temp.tags['amenity'] == 'bank'):
                outline = '#515464'
                fill = '#CCCCCC'
            elif (temp.tags['amenity'] == 'parking'):
                outline = '#515464'
                fill = '#676768'
            elif (temp.tags['amenity'] == 'bicycle_parking'):
                outline = '#515464'
                fill = '#676768'
            elif (temp.tags['amenity'] == 'parking_space'):
                outline = '#515464'
                fill = '#676768'
                
            canvas.create_polygon(path, outline=outline,
            fill=fill, width=1)
    for temp in osmMap.leisures:
        path = []
        for node in temp.nodes:
            x = (node.coordinate.lon - canvasOrigin[0]) * scale +viewPort[0]
            y = (canvasSize[1]-( node.coordinate.lat - canvasOrigin[1])) * scale + viewPort[1]
            path.append(x)
            path.append(y)
        if (path.__len__() > 6):
            outline = '#CCCCCC'
            fill = '#DDDDDD'
            if (temp.tags['leisure'] == 'park'):
                outline = '#619e44'
                fill = '#9edd80'
            elif (temp.tags['leisure'] == 'garden'):
                outline = '#85a22f'
                fill = '#b7da52'
            elif (temp.tags['leisure'] == 'track'):
                outline = '#7a651d'
                fill = '#c4a646'
            elif (temp.tags['leisure'] == 'pitch'):
                outline = '#7a651d'
                fill = '#c4a646'
                
            canvas.create_polygon(path, outline=outline,
            fill=fill, width=1)
            
    for temp in osmMap.naturals:
        path = []
        water = []
        for node in temp.nodes:
            x = (node.coordinate.lon - canvasOrigin[0]) * scale +viewPort[0]
            y = (canvasSize[1]-( node.coordinate.lat - canvasOrigin[1])) * scale + viewPort[1]
            path.append(x)
            path.append(y)
        if (path.__len__() > 6):
            outline = '#CCCCCC'
            fill = '#DDDDDD'
            if (temp.tags['natural'] == 'grassland'):
                outline = '#619e44'
                fill = '#9edd80'
            elif (temp.tags['natural'] == 'water'):
                outline = '#515464'
                fill = '#8895e4'
            elif (temp.tags['natural'] == 'wood'):
                outline = '#2c7509'
                fill = '#42b00d'
            elif (temp.tags['natural'] == 'scrub'):
                outline = '#85a22f'
                fill = '#b7da52'
            elif (temp.tags['natural'] == 'heath'):
                outline = '#7a651d'
                fill = '#c4a646'
                
            temp2 = canvas.create_polygon(path, outline=outline,
            fill=fill, width=1)
            if (temp.tags['natural'] == 'water'):
                water.append(temp2)
        for x in water:
            canvas.tag_raise(x)
    
    for temp in osmMap.buildings:
        path = []     
        for node in temp.way.nodes:
            x = (node.coordinate.lon - canvasOrigin[0]) * scale +viewPort[0]
            y = (canvasSize[1]-( node.coordinate.lat - canvasOrigin[1])) * scale + viewPort[1]
            path.append(x)
            path.append(y)
        if (path.__len__() > 6): #at least a triangle if not don't render
            canvas.create_polygon(path, outline='#515464',fill='#CCCCCC', width=2)           
            drawCircle(temp.coordinate.lon,temp.coordinate.lat,2, "#DDDDDD")   
        if (temp.entryPoint is not None):
            #print("rendering entry Point")
            drawLine(temp.entryPoint.lon,temp.entryPoint.lat, temp.coordinate.lon, temp.coordinate.lat, '#000000')
            
    for temp in osmMap.roads:
        data = temp.getPathForRendering()
        
#         x =  (data[0] - canvasOrigin[0]) * scale +viewPort[0]
#         y = (canvasSize[1]-(data[1] - canvasOrigin[1])) * scale + viewPort[1]
#         #drawCircle(temp.lon,temp.lat,1, "#476042")
#         x1 = (data[2] - canvasOrigin[0]) * scale +viewPort[0]
#         y1 = (canvasSize[1]-(data[3] - canvasOrigin[1])) * scale + viewPort[1]
#         canvas.create_line(x,y,x1,y1)
        
        drawLine(data[0],data[1], data[2], data[3], temp.color , width = temp.width)
        
    for temp in osmMap.roadNodes:
        drawCircle(temp.coordinate.lon,temp.coordinate.lat,1, "#476042")  
        
    lat = osmMap.origin.lat    
    for i in range(0,osmMap.gridSize[1]):
        drawLine(osmMap.origin.lon, lat, osmMap.end.lon,lat, "#AA0000")  
        lat += osmMap.distanceLat 
    lon = osmMap.origin.lon
    for j in range(0,osmMap.gridSize[0]):
        drawLine(lon, osmMap.origin.lat, lon,osmMap.end.lat, "#AA0000")  
        lon += osmMap.distanceLon 
        
        
def drawPath(path):
    prev = None
    for temp in path:
        if (prev is not None):            
            x =  (temp.lon - canvasOrigin[0]) * scale +viewPort[0]
            y = (canvasSize[1]-( temp.lat - canvasOrigin[1])) * scale + viewPort[1]
            x1 = (prev.lon - canvasOrigin[0]) * scale +viewPort[0]
            y1 = (canvasSize[1]-( prev.lat - canvasOrigin[1])) * scale + viewPort[1]
            canvas.create_line(x, y, x1, y1,fill="#0000FF")
        prev = temp
    for temp in path:
        drawCircle(temp.lon, temp.lat, 3,"#0000FF")
        

def drawAgent():   
    for agent in sim.agents:
        agent.oval = drawCircle(agent.currentLocation.lon, agent.currentLocation.lat, 5,"#3333CC", agent.name) 


def moveAgent(agent):
    x1,y1,x2,y2 = canvas.coords(agent.oval)
    xmid = x1 + ((x2-x1)/2) + viewPort[0]
    ymid = y1 + ((y2-y1)/2) + viewPort[1]
    x = ((agent.currentLocation.lon - canvasOrigin[0]) * scale +viewPort[0])- xmid 
    y = ((canvasSize[1]-( agent.currentLocation.lat - canvasOrigin[1])) * scale + viewPort[1]) -ymid 

    #print((x,y,agent.oval))
    if (agent.infectionStatus == "Exposed"):
        canvas.itemconfig(agent.oval,fill="#CCCC33")
    elif (agent.infectionStatus == "Infectious"):
        canvas.itemconfig(agent.oval,fill="#CC3333")
    elif (agent.infectionStatus == "Susceptible"):
        canvas.itemconfig(agent.oval,fill="#3333CC")
    else:
        canvas.itemconfig(agent.oval,fill="#33CC33")        
    canvas.move(agent.oval,x,y)

def drawCircle(lon,lat,radius, color, name = None):
    x = (lon - canvasOrigin[0]) * scale +viewPort[0]
    y = (canvasSize[1]-( lat - canvasOrigin[1])) * scale + viewPort[1]
    circle = None
    if (name is None):
        circle = canvas.create_oval(x-radius, y-radius, x+radius, y+radius, fill= color)
    else:
        circle = canvas.create_oval(x-radius, y-radius, x+radius, y+radius, fill=color,tag = name)
    return circle

def drawLine(originLon,originLat, destinationLon, destinationLat, color, width = 1.0, name = None):
    x =  (originLon - canvasOrigin[0]) * scale +viewPort[0]
    y = (canvasSize[1]-(originLat- canvasOrigin[1])) * scale + viewPort[1]
    #drawCircle(temp.lon,temp.lat,1, "#476042")
    x1 = (destinationLon- canvasOrigin[0]) * scale +viewPort[0]
    y1 = (canvasSize[1]-(destinationLat- canvasOrigin[1])) * scale + viewPort[1]
    line = canvas.create_line(x,y,x1,y1,width = width,fill=color)    
    return line

def render(map,simulation = None, path = None):
    global osmMap
    global canvasOrigin
    global canvasMax
    global canvasSize
    global canvas
    global scale
    global windowSize
    global viewPort
    global sim
    global lastStep 
    lastStep =0
    sim = simulation
    osmMap = map
    canvasOrigin = osmMap.origin.getLonLat()
    canvasMax = osmMap.end.getLonLat()
    canvasSize = osmMap.end.getVectorDistance(osmMap.origin).getLonLat()
    scale = 100000
    windowSize = (1024,768)
    viewPort = (0,0)
    prevPosition = None
    root = tkinter.Tk()
    root.resizable(False,False)
    canvas = tkinter.Canvas(root)
    ## bind button
    canvas.bind("<B1-Motion>", motion)
    canvas.bind("<ButtonRelease-1>",clickRelease)
    canvas.bind("<Double-Button-1>",doubleClick)
    canvas.bind("<MouseWheel>", scroll)
    #canvas.bind("<Configure>", resize)
    if OS == "Linux":
        root.bind_all('<4>', scroll, add='+')
        root.bind_all('<5>', scroll, add='+')
    else:
        # Windows and MacOS
        root.bind_all("<MouseWheel>", scroll, add='+')
    canvas.pack()
    canvas.config(width=windowSize[0], height=windowSize[1])
        
    draw()
    if (path is not None):
        drawPath(path)
    if (sim is not None):
        drawAgent()
        x = threading.Thread(target=start, args=())
        x.start()
        canvas.after(1000,step)
    root.mainloop()