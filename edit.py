import os
from time import sleep

'''해당 부분은 VBOX 조정'''

#os.system('VBoxManage startvm boan_sol_win --type gui')
#VBoxManage startvm boan_sol --type gui   #(gui | headless | sdi | separate)

os.system('VBoxManage guestcontrol boan_sol_win copyto --target-directory C:\\test\ C:\\Users\\LINKER\\Desktop\\PythonWorkspace\\test_sleep.vmem --username test --password 1234 --verbose')

#os.system('VBoxManage debugvm "boan_sol_win" dumpvmcore --filename ./bosol/test_sleep.vmem') 

'''이 부분부터는 와이어샤크 조종'''