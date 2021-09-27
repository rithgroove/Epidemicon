#!/bin/bash
python main_no_render.py -c config.yml --no_infectious_stop > output1.txt &
python main_no_render.py -c config2.yml --no_infectious_stop > output2.txt &
python main_no_render.py -c config3.yml --no_infectious_stop > output3.txt &
wait