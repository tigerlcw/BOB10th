import os
from time import sleep
import pandas as pd
import datetime
from datetime import datetime
import csv
import numpy as np
import re

# 1번 
def vm_start():
    os.system('VBoxManage startvm boan_sol_win --type gui')
    print('VM이 실행되었습니다.')
    return

# 2번
def vm_snapshot():
    os.system('VBoxManage snapshot boan_sol_win take win-test') # 스냅샷 찍기
    print("\n win-test 스냅샷이 생성되었습니다.\n")
    return

# 3번
def file_search():
    print("\n해당 작업은 파일을 받고 프로세스모니터 -> 와이어샤크 -> netscan순으로\n작업 후 종료됩니다.\n")
    file_name = input("분석할 파일이름을 입력하세요. -> ")
    add_func = input("테스트용 명령어 인자를 추가해주세요. 없으면 Enter Ex) /all -> ")

    os.system('VBoxManage guestcontrol boan_sol_win copyto --target-directory C:\\test C:\\Users\\LINKER\\Desktop\\PythonWorkspace\\bosol\\%s --username test --password 1234 --verbose' % file_name)
    sleep(2)

    '''이 부분부터는 프로세스모니터 조종'''

    os.system('start /b VBoxManage guestcontrol boan_sol_win run --exe "C:\Windows\SysWOW64\cmd.exe" --username test --password 1234 /c Procmon /BackingFile C:\\test\\monitor.pml')
    sleep(4)
    os.system('start /b VBoxManage guestcontrol boan_sol_win run --exe "C:\Windows\SysWOW64\cmd.exe" --username test --password 1234 /c C:\\test\\%s /c %s' % (file_name, add_func))
    sleep(5)
    os.system('start /b VBoxManage guestcontrol boan_sol_win run --exe "C:\Windows\SysWOW64\cmd.exe" --username test --password 1234 /c Procmon /Terminate')
    sleep(6)
    os.system('start /b VBoxManage guestcontrol boan_sol_win run --exe "C:\Windows\SysWOW64\cmd.exe" --username test --password 1234 /c Procmon /OpenLog C:\\test\\monitor.pml /SaveAs C:\\test\\monitor.csv')
    sleep(2)

    os.system('VBoxManage guestcontrol boan_sol_win copyfrom --target-directory C:\\Users\\LINKER\\Desktop\\PythonWorkspace\\bosol\\ C:\\test\\monitor.csv --username test --password 1234 --verbose')
    
    '''이 부분부터는 와이어샤크 조종'''
  
    os.system('VBoxManage guestcontrol boan_sol_win run --exe "C:\Windows\SysWOW64\cmd.exe" --username test --password 1234 --wait-stdout -- cmd.exe /c tshark -i 이더넷 -T fields -E separator=, -E quote=d -e _ws.col.No. -e _ws.col.Time -e _ws.col.Source -e _ws.col.Destination -e _ws.col.Protocol -e _ws.col.Length -e _ws.col.Info -c 3' + ' > C:\\Users\\LINKER\\Desktop\\PythonWorkspace\\bosol\\shark.csv')
    print("성공")
    sleep(1)

    df = pd.read_csv("C:/Users/LINKER/Desktop/PythonWorkspace/bosol/monitor.csv", error_bad_lines=False)
    sleep(1) # 종료 직전 메모리 추출 단계 필요!

    os.system('VBoxManage controlvm boan_sol_win poweroff')
    print('VM이 종료되었습니다.\n')
    # 검사하고 싶은 프로그램( ex)'wmiprvse.exe' )에서 CreateFile API를 사용해 생성된 파일 이름을 file이라는 변수에 저장
    process = df['Process Name'] == file_name 
    df_unique = df[process]
    operation = df_unique['Operation'] == 'CreateFile'
    df1 = df_unique[operation]
    df1 = df1[['Path']]
    df1['name'] = df1['Path'].str.extract(r'([^\/\n]+$)')

    df1 = df1.dropna(axis=0)
    filename = df1['name'].reset_index()
    filename.drop(['index'], axis=1, inplace=True)
    input_name = file_name 

    filename.loc[0] = [input_name]
    filename.insert(0, 'total', 1)
    file = filename.groupby('total')['name'].unique().loc[1]
    print("생성한 파일: ", file)


    ## file이라는 변수에 저장된 프로그램이 사용한 API 함수 불러오기
    df_final = df[df['Process Name'].isin(file)]
    df1 = df_final.reset_index(drop=True)
    df2 = df1[['Operation', 'Path']]
    df2

    cols = ['Operation',]
    df2.insert(1, 'total', 1)
    df3 = df2.groupby(cols)['total'].sum().reset_index()
    df3 = df3.sort_values(by = 'total')
    df3 = df3.reset_index(drop=True)
    print(df3,"\n")

    sleep(1)
    os.system('VBoxManage snapshot boan_sol_win restore win-test') #스냅샷 시점으로 복원
    print("프로그램 실행 전 상태로 복원되었습니다.\n")
    return

# 4번
def dump_vmem():
    vmem_name = input("입력한 파일명으로 .vmem로 생성됩니다. -> ")
    os.system('VBoxManage debugvm "boan_sol_win" dumpvmcore --filename ./bosol/'+vmem_name+'.vmem')
    print("\n"+vmem_name+".vmem파일이 생성되었습니다.\n")
    return

# 5번
def vm_snapdelete():
    os.system('VBoxManage snapshot boan_sol_win delete win-test')
    print("\n스냅샷 파일이 삭제되었습니다.\n")
    return