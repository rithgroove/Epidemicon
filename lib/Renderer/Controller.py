from .View import View
import platform
import time
import threading

#todo: there are stuff from View that should be moved here

class Controller():
    def __init__(self, model, view, path=None):
        self.model = model
        self.view  = view
        
        # for convinience 
        self.mymap = self.model.osmMap
        
        ### platform specific methods and stuff ###
        self.OS = platform.system()
        # scroll
        self.on_mouse_scroll = self.__scroll_windows_mac
        if self.OS == "Linux":
            self.on_mouse_scroll = self.__scroll_linux
            
        ## set key events
        self.view.set_events(self)
        
        ## some attributes related to the view ##
        self.zoom_in_param = 1.1
        self.zoom_out_param = (10.0/11.0)
        
        self.thread_finished = False
        
        # todo merge changes 
        self.view.initial_draw()
    
    ## MAIN METHODS ##
    def main_loop(self):
        self.view.root.mainloop()
        
    def update_view(self):
        self.view.step(self.model.agents, self.model.stepCount)
    
    def on_closing(self):
        self.view.thread_run = False
        while not self.thread_finished:
            time.sleep(1)
        self.view.close()
    
    ## ZOOM ##
    def on_mouse_scroll(self, event):
        pass

    def __scroll_linux(self, event):
        if event.num == 4:
            self.on_zoom_in()
        elif event.num == 5:
            self.on_zoom_out()
        
    def __scroll_windows_mac(self, event):
        value = -1*(event.delta)
        if (value>0):
            self.on_zoom_in()
        elif (value<0):
            self.on_zoom_out()
    
    def on_zoom_in(self):
        self.view.zoom(self.zoom_in_param)
        
    def on_zoom_out(self):
        self.view.zoom(self.zoom_out_param)
    
    ## MOVING THE MAP ##
    def on_mouse_release(self, event):
        self.view.mouse_release() 
        
    def on_mouse_hold(self, event):
        self.view.mouse_hold(event.x, event.y)
    
    ## RUN ##
    #cmd = buttons
    def cmd_start(self):
        self.view.btn_start_change_method(text="Play ", method=self.cmd_play)
        
        self.thread = threading.Thread(target=self.run_step, args=())
        self.thread.start()
        
    def cmd_play(self):
        self.view.btn_start_change_method(text="Pause", method=self.cmd_pause)
        self.thread = threading.Thread(target=self.run_auto, args=())
        self.view.thread_run = True
        self.thread.start()
        
    def cmd_pause(self):
        self.view.btn_start_change_method(text="Play ", method=self.cmd_play)
        self.view.thread_run = False
                
    def cmd_step(self):
        self.thread = threading.Thread(target=self.run_step, args=())
        self.thread.start()
    
    # 
    def run_auto(self):
        self.thread_finished = False
        while self.view.thread_run:
            print("Processing... ", end="", flush=True)
            self.model.step(steps=self.view.steps_to_advance)
            self.update_view()
            print("Done!", flush=True)
            time.sleep(1)
        self.thread_finished = True
        
    def run_step(self):
        self.thread_finished = False
        print("Processing... ", end="", flush=True)
        self.model.step(steps=self.view.steps_to_advance)
        self.update_view()
        print("Done!", flush=True)
        self.thread_finished = True
    
    ## DRAWING ##
    