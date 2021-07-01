import sys
import os
# adds the root of the git dir to the import path
sys.path.append(os.getcwd().split("Epidemicon")[0] + "Epidemicon")
import lib.Map.Map as map
import lib.Renderer.Renderer as renderer

OSMfile = "TX-To-TU.osm"

def path_to_root_dir():
    path = os.getcwd().split("Epidemicon")[0]
    return os.path.join(path , "Epidemicon")


def main():
    filePath = os.path.join(path_to_root_dir(), "osmData", OSMfile)
    osmMap = map.readFile(filePath)
    renderer.render(osmMap)

if __name__ == "__main__":
    main()