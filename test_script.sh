time python3 main_no_render.py -c config.yml -s 100 --no_infectious_stop | tee reportNoLockdown/output.txt
time python3 main_no_render.py -c configTimeLockdown.yml -s 100 --no_infectious_stop | tee reportTimeLockdown/output.txt
time python3 main_no_render.py -c configTotalLockdown.yml -s 100 --no_infectious_stop | tee reportTotalLockdown/output.txt