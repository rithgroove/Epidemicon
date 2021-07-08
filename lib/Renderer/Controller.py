from .View import View
import platform

#todo: there are stuff from View that should be moved here

class Controller():
    def __init__(self, osmMap, simulation=None, path=None):
        self.window = View(mymap=osmMap, simulation=simulation, path=path)
        
        ### platform specific methods and stuff ###
        self.OS = platform.system()
        
        # scroll
        self.onMouseScroll = self.scroll_windows_mac
        if self.OS == "Linux":
            self.onMouseScroll = self.scroll_linux
            
        
        self.window.setController(self)
    
    def mainloop(self):
        self.window.root.mainloop()
    
    def onMouseScroll(self, event):
        pass

    def scroll_linux(self, event):
        if event.num == 4:
            self.zoom_in()
        elif event.num == 5:
            self.zoom_out()
        
    def scroll_windows_mac(self, event):
        value = -1*(event.delta)
        if (value>0):
            self.zoom_in()
        elif (value<0):
            self.zoom_out()
    
    def zoom_in(self):
        self.window.canvas.scale('all', 0, 0, 1.1, 1.1)
        self.window.scale *=  1.1
        
    def zoom_out(self):
        self.window.canvas.scale('all', 0, 0, 10.0/11.0, 10.0/11.0)
        self.window.scale *= (10.0/11.0)
        
    def test(self):
        print("test")
    
    
    def onMouseDoubleClick(self, event):
        self.window.animating = not self.window.animating
        
    def onMouseRelease(self, event):
        self.window.prevPosition = None
        
    def onMouseHold(self, event):
        if self.window.prevPosition is not None:
            translation = (self.window.prevPosition[0]-event.x, self.window.prevPosition[1]-event.y)
            self.window.viewPort = (self.window.viewPort[0]-translation[0], self.window.viewPort[1]- translation[1])
            #print(translation)
            if(self.window.viewPort[0] > 0):
                self.window.viewPort = (0, self.window.viewPort[1])
            elif(self.window.viewPort[0] < -1* self.window.scale *self.window.canvasSize[0] + self.window.windowSize[0]):
                #print("too far x")
                self.window.viewPort = (int( -1* self.window.scale *self.window.canvasSize[0] + self.window.windowSize[0]), self.window.viewPort[1])
            if(self.window.viewPort[1] > 0):
                self.window.viewPort = (self.window.viewPort[0], 0)
            elif(self.window.viewPort[1] < -1* self.window.scale *self.window.canvasSize[1] + self.window.windowSize[1]):
                #print("too far y")
                self.window.viewPort = (self.window.viewPort[0], int( -1* self.window.scale *self.window.canvasSize[1] + self.window.windowSize[1]))
            
        self.window.prevPosition = (event.x,event.y)
        self.window.canvas.scan_dragto(self.window.viewPort[0], self.window.viewPort[1], gain=1)