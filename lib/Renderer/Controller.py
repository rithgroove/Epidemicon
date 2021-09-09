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
        
        self.thread_finished = True
        self.thread_ask_stop = False
        
        # todo merge changes 
        self.view.initial_draw()
    
    ## MAIN METHODS ##
    def main_loop(self):
        self.view.root.mainloop()
        
    def update_view(self):
        self.view.step(self.model.agents, self.model.stepCount)
    
    def on_closing(self):
        self.thread_ask_stop = True
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
        self.thread_ask_stop = False
        self.thread.start()
        
    def cmd_pause(self):
        self.view.btn_start_change_method(text="Play ", method=self.cmd_play)
        self.thread_ask_stop = True
        
                
    def cmd_step(self):
        self.thread = threading.Thread(target=self.run_step, args=())
        self.thread.start()
    
    # 
    def run_auto(self):
        self.thread_finished = False
        while not self.thread_ask_stop:
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
    
    ## STATS ##
    def _on_show_stats(self):
        def __count_jobs(agentlist, jobclasses):
            d = {}
            for job in jobclasses:
                d[job.name] = 0
                
            for agent in agentlist:
                d[agent.mainJob.jobClass.name] +=1
                
            out = "\n".join([f"- {k}: {v}" for k, v in d.items()])
            return out
    
        output = [""]*10
        output[0] = f"====Stats===="
        output[1] = f"Step Count: {self.model.stepCount}"
        output[2] = f"# Agents: {len(self.model.agents)}"
        output[3] = f"Jobs: \n{__count_jobs(agentlist=self.model.agents, jobclasses=self.model.jobClasses)}"
        output[4] = f"Orders Placed: {self.model.online_shopping.n_orders}"
        
        print("\n".join(output))
    