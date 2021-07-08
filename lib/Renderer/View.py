import tkinter 
import time
import threading

class View():
    def __init__(self, mymap, simulation=None, path=None):
        #todo: there are part of functions that should go to controller
        self.animating = False
        
        self.lastStep = 0
        self.sim      = simulation
        self.osmMap   = mymap
        
        self.canvasOrigin = self.osmMap.origin.getLonLat()
        self.canvasMax    = self.osmMap.end.getLonLat()
        self.canvasSize   = self.osmMap.end.getVectorDistance(self.osmMap.origin).getLonLat()

        self.scale        = 100000
        self.windowSize   = (1024,768)
        self.viewPort     = (0,0)
        self.prevPosition = None
        
        ## root
        self.root = tkinter.Tk()
        self.root.resizable(True, True)
        
        ## frames
        self.frame_btn    = tkinter.Frame(self.root)
        self.frame_canvas = tkinter.Frame(self.root)
    
        ## canvas
        self.canvas = tkinter.Canvas(self.frame_canvas)
    
        ## buttons
        self.root.btn_zoom_in  = tkinter.Button(self.frame_btn, text="Zoom in (+)")#, command=lambda:zoom_in(canvas, scale))
        self.root.btn_zoom_out = tkinter.Button(self.frame_btn, text="Zoom out (-)")#, command=lambda:zoom_out(canvas, scale))
        self.root.btn_zoom_in.pack(side="left")
        self.root.btn_zoom_out.pack(side="left")
        
        # ## bind button
        #todo: ask abe whats this for
        # if OS == "Linux": #todo: platform.system()
            # self.root.bind_all('<4>', scroll, add='+')
            # self.root.bind_all('<5>', scroll, add='+')
        # else: #Windows and MacOS
            # self.root.bind_all("<MouseWheel>", scroll, add='+')
        
        self.canvas.pack()
        self.canvas.config(width=self.windowSize[0], height=self.windowSize[1])
            
        self.draw()
        if path is not None:
            self.drawPath(path)
        if self.sim is not None:
            self.drawAgent()
            x = threading.Thread(target=self.start, args=())
            x.start()
            self.canvas.after(1000, self.step)
            
        ## frames pack
        self.frame_btn.pack(side="top")   
        self.frame_canvas.pack(side="bottom")

    def setController(self, controller):
        self.controller = controller
        
        # bindings
        ## buttons
        self.root.btn_zoom_in["command"]  = controller.zoom_in
        self.root.btn_zoom_out["command"] = controller.zoom_out
        ## canvas
        self.canvas.bind("<MouseWheel>"     , controller.onMouseScroll)
        self.canvas.bind("<Double-Button-1>", controller.onMouseDoubleClick)
        self.canvas.bind("<B1-Motion>"      , controller.onMouseHold)
        self.canvas.bind("<ButtonRelease-1>", controller.onMouseRelease)

    def draw(self): #todo: break this into smaller functions
        for temp in self.osmMap.amenities:
            path = []
            for node in temp.nodes:
                x = (node.coordinate.lon - self.canvasOrigin[0]) * self.scale + self.viewPort[0]
                y = (self.canvasSize[1]-( node.coordinate.lat - self.canvasOrigin[1])) * self.scale + self.viewPort[1]
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
                    
                self.canvas.create_polygon(path, outline=outline, fill=fill, width=1)
                
        for temp in self.osmMap.leisures:
            path = []
            for node in temp.nodes:
                x = (node.coordinate.lon - self.canvasOrigin[0]) * self.scale + self.viewPort[0]
                y = (self.canvasSize[1]-(node.coordinate.lat - self.canvasOrigin[1])) * self.scale + self.viewPort[1]
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
                    
                self.canvas.create_polygon(path, outline=outline, fill=fill, width=1)
                
        for temp in self.osmMap.naturals:
            path = []
            water = []
            for node in temp.nodes:
                x = (node.coordinate.lon - self.canvasOrigin[0]) * self.scale + self.viewPort[0]
                y = (self.canvasSize[1]-( node.coordinate.lat - self.canvasOrigin[1])) * self.scale + self.viewPort[1]
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
                    
                temp2 = self.canvas.create_polygon(path, outline=outline, fill=fill, width=1)
                if (temp.tags['natural'] == 'water'):
                    water.append(temp2)
            for x in water:
                self.canvas.tag_raise(x)
        
        for temp in self.osmMap.buildings:
            path = []     
            for node in temp.way.nodes:
                x = (node.coordinate.lon - self.canvasOrigin[0]) * self.scale + self.viewPort[0]
                y = (self.canvasSize[1]-(node.coordinate.lat - self.canvasOrigin[1])) * self.scale + self.viewPort[1]
                path.append(x)
                path.append(y)
            if (path.__len__() > 6): #at least a triangle if not don't render
                self.canvas.create_polygon(path, outline='#515464',fill='#CCCCCC', width=2)           
                self.drawCircle(temp.coordinate.lon,temp.coordinate.lat,2, "#DDDDDD")   
            if (temp.entryPoint is not None):
                #print("rendering entry Point")
                self.drawLine(temp.entryPoint.lon,temp.entryPoint.lat, temp.coordinate.lon, temp.coordinate.lat, '#000000')
                
        for temp in self.osmMap.roads:
            data = temp.getPathForRendering()
            
    #         x =  (data[0] - canvasOrigin[0]) * scale +viewPort[0]
    #         y = (canvasSize[1]-(data[1] - canvasOrigin[1])) * scale + viewPort[1]
    #         #drawCircle(temp.lon,temp.lat,1, "#476042")
    #         x1 = (data[2] - canvasOrigin[0]) * scale +viewPort[0]
    #         y1 = (canvasSize[1]-(data[3] - canvasOrigin[1])) * scale + viewPort[1]
    #         canvas.create_line(x,y,x1,y1)
            
            self.drawLine(data[0],data[1], data[2], data[3], temp.color , width = temp.width)
            
        for temp in self.osmMap.roadNodes:
            self.drawCircle(temp.coordinate.lon,temp.coordinate.lat,1, "#476042")  
            
        lat = self.osmMap.origin.lat    
        for i in range(0, self.osmMap.gridSize[1]):
            self.drawLine(self.osmMap.origin.lon, lat, self.osmMap.end.lon,lat, "#AA0000")  
            lat += self.osmMap.distanceLat 
        lon = self.osmMap.origin.lon
        for j in range(0, self.osmMap.gridSize[0]):
            self.drawLine(lon, self.osmMap.origin.lat, lon, self.osmMap.end.lat, "#AA0000")  
            lon += self.osmMap.distanceLon 

    def drawCircle(self, lon, lat, radius, color, name=None):
        x = (lon - self.canvasOrigin[0]) * self.scale + self.viewPort[0]
        y = (self.canvasSize[1]-( lat - self.canvasOrigin[1])) * self.scale + self.viewPort[1]
        circle = None
        if (name is None):
            circle = self.canvas.create_oval(x-radius, y-radius, x+radius, y+radius, fill= color)
        else:
            circle = self.canvas.create_oval(x-radius, y-radius, x+radius, y+radius, fill=color,tag = name)
        return circle
        
    def drawLine(self, originLon, originLat, destinationLon, destinationLat, color, width=1.0, name=None):
        x =  (originLon - self.canvasOrigin[0]) * self.scale + self.viewPort[0]
        y = (self.canvasSize[1]-(originLat- self.canvasOrigin[1])) * self.scale + self.viewPort[1]
        #drawCircle(temp.lon,temp.lat,1, "#476042")
        x1 = (destinationLon- self.canvasOrigin[0]) * self.scale + self.viewPort[0]
        y1 = (self.canvasSize[1]-(destinationLat- self.canvasOrigin[1])) * self.scale + self.viewPort[1]
        line = self.canvas.create_line(x,y,x1,y1,width=width,fill=color)    
        return line
    
    def drawPath(self, path):
        prev = None
        for temp in path:
            if prev is not None:
                x =  (temp.lon - self.canvasOrigin[0]) * self.scale + self.viewPort[0]
                y = (self.canvasSize[1]-(temp.lat - self.canvasOrigin[1])) * self.scale + self.viewPort[1]
                x1 = (prev.lon - self.canvasOrigin[0]) * self.scale + self.viewPort[0]
                y1 = (self.canvasSize[1]-(prev.lat - self.canvasOrigin[1])) * self.scale + self.viewPort[1]
                self.canvas.create_line(x, y, x1, y1,fill="#0000FF")
            prev = temp
        for temp in path:
            self.drawCircle(temp.lon, temp.lat, 3,"#0000FF")

    def drawAgent(self):
        for agent in self.sim.agents:
            agent.oval = self.drawCircle(agent.currentLocation.lon, agent.currentLocation.lat, 5,"#3333CC", agent.name) 
        
    def moveAgent(self, agent):
        x1,y1,x2,y2 = self.canvas.coords(agent.oval)
        xmid = x1 + ((x2-x1)/2) + self.viewPort[0]
        ymid = y1 + ((y2-y1)/2) + self.viewPort[1]
        x = ((agent.currentLocation.lon - self.canvasOrigin[0]) * self.scale + self.viewPort[0])- xmid 
        y = ((self.canvasSize[1]-( agent.currentLocation.lat - self.canvasOrigin[1])) * self.scale + self.viewPort[1]) -ymid 

        #print((x,y,agent.oval))
        if (agent.infectionStatus == "Exposed"):
            self.canvas.itemconfig(agent.oval,fill="#CCCC33")
        elif (agent.infectionStatus == "Infectious"):
            self.canvas.itemconfig(agent.oval,fill="#CC3333")
        elif (agent.infectionStatus == "Susceptible"):
            self.canvas.itemconfig(agent.oval,fill="#3333CC")
        else:
            self.canvas.itemconfig(agent.oval,fill="#33CC33")        
        self.canvas.move(agent.oval,x,y)
    
    def start(self):
        while True:
            if self.animating:
                self.sim.step()
                print("finish stepping")
            time.sleep(10)
            
    def step(self):
        if self.lastStep != self.sim.stepCount:
            for x in self.sim.agents:
                self.moveAgent(x)
            self.lastStep = self.sim.stepCount
        self.canvas.after(1000, self.step)
            
            
            
            
            
            
            
            
            
            
            
