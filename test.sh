#!/bin/bash
nohup python main_no_render.py -c config2.yml --no_infectious_stop > output2.txt &
wait
