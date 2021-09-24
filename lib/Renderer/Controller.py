from .View import View
from . import debug
import platform
import time
import threading
from tkinter import messagebox

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
        self.set_events()
        
        ## some attributes related to the view ##
        self.zoom_in_param = 1.1
        self.zoom_out_param = (10.0/11.0)
        
        self.thread_finished = True
        self.thread_ask_stop = False
        
        # todo merge changes 
        self.view.root.after(1000, self.disable_buttons)
        self.view.initial_draw()
    
    def disable_buttons(self):
        if self.model.calculating:
            self.view.button["play"]["state"] = "disabled"
            self.view.button["step"]["state"] = "disabled"
        else:
            # self.view.button["play"]["state"] = "normal"
            self.view.button["step"]["state"] = "normal"
        self.view.root.after(1000, self.disable_buttons)


    ## MAIN METHODS ##
    def main_loop(self):
        # add here methods to excute before entering the mainloop
        # ...
        try:
            self.view.root.mainloop()
        except:
            self.model.killStepThreads()
        # add here methods to excute after exiting the mainloop
        # ...
        
    def update_view(self):
        self.view.step(self.model.agents, self.model.timeStamp.stepCount)
    
    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.thread_ask_stop = True
            self.model.killStepThreads()
            #if (self.thread is not None):
            #    self.thread.terminate()
            #while not self.thread_finished:
            #    time.sleep(1)
            self.view.close()
            
    def set_events(self):
        view = self.view
        
        # window
        view.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # tab 1 buttons
        view.button["zoom_in"]["command"]  = self.on_zoom_in
        view.button["zoom_out"]["command"] = self.on_zoom_out
        view.button["play"]["command"]     = self.cmd_start
        view.button["step"]["command"]     = self.cmd_step

        # tab 1 canvas
        view.canvas.bind("<MouseWheel>"     , self.on_mouse_scroll)
        view.canvas.bind("<B1-Motion>"      , self.on_mouse_hold)
        view.canvas.bind("<ButtonRelease-1>", self.on_mouse_release)
        
        # tab 2 stats
        view.button["jobs"]["command"]   = lambda: debug._on_show_jobs(self)
        view.button["orders"]["command"] = lambda: debug._on_show_orders(self)
        view.button["agent_position"]["command"] = lambda: debug._on_agents_position(self)

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
        self.thread_ask_stop = False
        self.thread.start()
        
    def cmd_pause(self):
        self.view.btn_start_change_method(text="Play ", method=self.cmd_play)
        self.thread_ask_stop = True
        
                
    def cmd_step(self):
        self.thread = threading.Thread(target=self.run_step, args=())
        self.thread.start()
    
    def run_auto(self):
        self.thread_finished = False
        while not self.thread_ask_stop:
            print("Processing... ", end="", flush=True)
            self.model.step(stepSize=self.view.steps_to_advance)
            self.update_view()
            print("Done!", flush=True)
            time.sleep(1)
        self.thread_finished = True
        
    def run_step(self):
        self.thread_finished = False
        print("Processing... ", end="", flush=True)
        self.model.step(stepSize=self.view.steps_to_advance)
        self.update_view()
        print("Done!", flush=True)
        self.thread_finished = True
