import sys
import os
# adds the root of the git dir to the import path
# FIXME: Directory shenanigans
root_dir = os.getcwd()
sys.path.append(root_dir)
import lib.Map.Map as map
from lib.Renderer.Controller import Controller

import time

OSMfile = "TX-To-TU.osm"
def main():
    filePath = os.path.join(root_dir, "osmData", OSMfile)
    
    t1 = time.time()
    osmMap = map.readFile(filePath)
    t2 = time.time()
    print(f"Time to load the data: {t2-t1}")
    
    app = Controller(osmMap)
    app.mainloop()

if __name__ == "__main__":
    main()
    