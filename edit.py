import os
from time import sleep

os.system('VBoxManage startvm boan_sol_win --type gui')
#VBoxManage startvm boan_sol --type gui   #(gui | headless | sdi | separate)

sleep(90) # vbox on time...wait
os.system('VBoxManage debugvm "boan_sol_win" dumpvmcore --filename ./bosol/test_sleep.vmem')
