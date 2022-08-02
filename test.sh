#!/bin/bash
nohup python main_no_render.py -c config1.yml --no_infectious_stop > output1.txt &
nohup python main_no_render.py -c configA.yml --no_infectious_stop > outputA.txt &
wait
