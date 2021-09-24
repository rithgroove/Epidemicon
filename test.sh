#!/bin/bash
nohup python main_no_render.py -c config4.yml --no_infectious_stop > output4.txt &
nohup python main_no_render.py -c config6.yml --no_infectious_stop > output6.txt &
