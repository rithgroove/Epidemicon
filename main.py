import sys
import os
# adds the root of the git dir to the import path
# FIXME: Directory shenanigans
root_dir = os.getcwd()
sys.path.append(root_dir)
import lib.Map.Map as map
import lib.Renderer.Renderer as renderer

OSMfile = "TX-To-TU.osm"
def main():
    filePath = os.path.join(root_dir, "osmData", OSMfile)
    osmMap = map.readFile(filePath)
    renderer.render(osmMap)

if __name__ == "__main__":
    main()
    