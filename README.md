# Epidemicon
Disease spread simulation
This repository contains the simulator used for the paper: Mitsuteru Abe, Fabio Tanaka, Jair Pereira Junior, Anna Bogdanova, Tetsuya Sakurai, and Claus Aranha. 2022. **Using Agent-Based Simulator to Assess Interventions Against COVID-19 in a Small Community Generated from Map Data.** In Proceedings of the 21st International Conference on Autonomous Agents and Multiagent Systems (AAMAS '22). International Foundation for Autonomous Agents and Multiagent Systems, Richland, SC, 1–8.

## How to reproduce the results:
- Download the .osm file for the tsukuba area and place it on: osm_files/Tx-To-TU.osm
    - To download the file go to: https://www.openstreetmap.org/export and set the following coordinates:
        - minlat="36.0777000" 
        - minlon="140.0921000" 
        - maxlat="36.1217000"
        - maxlon="140.1201000"
- change the configurations on 
- to execute without a config file run: $ python main_no_render.py -c config_file --no_infectious_stop