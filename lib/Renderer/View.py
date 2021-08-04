import tkinter as tk
import time

class View():
    def __init__(self, mymap, simulation=None, path=None):
        #todo: there are part of functions that should go to controller
        self.animating = False
        
        self.path = path
        
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
        self.root = tk.Tk()
        self.root.title("Epidemicon")
        self.root.resizable(False, False)
        
        ## frames
        self.frame_btn    = tk.Frame(self.root)
        self.frame_canvas = tk.Frame(self.root)
        
        for i in range(11):
            self.frame_btn.columnconfigure(i, weight=10)
    
        ## canvas
        self.canvas = tk.Canvas(self.frame_canvas)
    
        ## button bar
        # zoom
        self.root.btn_zoom_in  = tk.Button(self.frame_btn, text="+")
        self.root.btn_zoom_out = tk.Button(self.frame_btn, text="-")
        
        #play pause step
        self.root.btn_start   = tk.Button(self.frame_btn, text="Init")
        self.root.btn_step  = tk.Button(self.frame_btn, text="Forward")
        self.root.btn_step["state"] = tk.DISABLED #disabled until we click on INIT
        
        #number of steps
        self.root.label_step = tk.Label(self.frame_btn, text="Step: 0")
        self.root.step_scale = tk.Scale(self.frame_btn, label="Step Size", from_=1, to=100, orient=tk.HORIZONTAL)
        
        #add to grid
        self.root.btn_start.grid(row=0,    column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.root.label_step.grid(row=0,   column=1, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.root.step_scale.grid(row=0,   column=2, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.root.btn_step.grid(row=0,     column=3, sticky=(tk.N, tk.S, tk.E, tk.W))
        
        self.root.btn_zoom_out.grid(row=0, column=9, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.root.btn_zoom_in.grid(row=0,  column=10, sticky=(tk.N, tk.S, tk.E, tk.W))
        
        
        ## canvas pack and size
        self.canvas.pack()
        self.canvas.config(width=self.windowSize[0], height=self.windowSize[1])
        
        ## frames pack
        self.frame_btn.pack(side="top", fill=tk.X, expand=True)   
        self.frame_canvas.pack(side="bottom")
    
    def set_events(self, controller): #todo: need more thoughts on decoupling
        ## bindings
        # buttons
        self.root.btn_zoom_in["command"]  = controller.on_zoom_in
        self.root.btn_zoom_out["command"] = controller.on_zoom_out
        self.root.btn_step["command"]     = controller.cmd_step
        self.root.btn_start["command"]    = controller.cmd_start
        
        # canvas
        self.canvas.bind("<MouseWheel>"     , controller.on_mouse_scroll)
        self.canvas.bind("<B1-Motion>"      , controller.on_mouse_hold)
        self.canvas.bind("<ButtonRelease-1>", controller.on_mouse_release)
        
        self.root.protocol("WM_DELETE_WINDOW", controller.on_closing)
    
    def initial_draw(self):
        self.draw()
        if self.path is not None:
            self.drawPath(path)
        if self.sim is not None:
            self.drawAgent()
    
    ## commands ##
    def zoom(self, scale):
        self.scale *=  scale
        self.canvas.scale('all', 0, 0, scale, scale)

    def mouse_release(self):
        self.prevPosition = None
    
    def mouse_hold(self, x, y): #todo: decouple
        if self.prevPosition is not None:
            translation = (self.prevPosition[0]-x, self.prevPosition[1]-y)
            self.viewPort = (self.viewPort[0]-translation[0], self.viewPort[1]- translation[1])
            #print(translation)
            if(self.viewPort[0] > 0):
                self.viewPort = (0, self.viewPort[1])
            elif(self.viewPort[0] < -1* self.scale *self.canvasSize[0] + self.windowSize[0]):
                #print("too far x")
                self.viewPort = (int( -1* self.scale *self.canvasSize[0] + self.windowSize[0]), self.viewPort[1])
            if(self.viewPort[1] > 0):
                self.viewPort = (self.viewPort[0], 0)
            elif(self.viewPort[1] < -1* self.scale *self.canvasSize[1] + self.windowSize[1]):
                #print("too far y")
                self.viewPort = (self.viewPort[0], int( -1* self.scale *self.canvasSize[1] + self.windowSize[1]))
            
        self.prevPosition = (x, y)
        self.canvas.scan_dragto(self.viewPort[0], self.viewPort[1], gain=1)

    def close(self):
        self.root.destroy()

    def step(self, agents, stepcount=""):
        for a in agents:
            self.moveAgent(a)
        self.root.label_step["text"] = f"Step: {stepcount}"
    
    def btn_start_change_method(self, text, method):
        self.root.btn_start["text"]    = text
        self.root.btn_start["command"] = method
        
        
        self.root.btn_step["state"] = tk.NORMAL
        if text == "Pause": # auto-running
            self.root.btn_step["state"] = tk.DISABLED
        
        
    ## setters and getters ##
    @property
    def steps_to_advance(self):
        return self.root.step_scale.get()


    ##refactoring
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
            lat += self.osmMap.gridCellHeight 
        lon = self.osmMap.origin.lon
        for j in range(0, self.osmMap.gridSize[0]):
            self.drawLine(lon, self.osmMap.origin.lat, lon, self.osmMap.end.lat, "#AA0000")  
            lon += self.osmMap.gridCellWidth 

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
    
