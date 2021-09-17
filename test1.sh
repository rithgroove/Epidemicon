python3 main_no_render.py -s 10 -c 20road.yml --no_infectious_stop | tee 20road.txt
python3 main_no_render.py -s 10 -c initialInf.yml --no_infectious_stop | tee initialInf.txt
python3 main_no_render.py -s 10 -c infectionRate.yml --no_infectious_stop | tee infectionRate.txt