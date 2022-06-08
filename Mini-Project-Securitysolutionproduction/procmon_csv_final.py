import os
from time import sleep
import pandas as pd
import datetime
from datetime import datetime
import csv
import numpy as np
import re
import glob

vmemfile = 'C:\\Users\\LINKER\\Desktop\\PythonWorkspace\\bosol\\test.vmem'
configfile = 'C:\\Users\\LINKER\\Desktop\\PythonWorkspace\\bosol\\config.json'
volatility = 'C:\\Users\\LINKER\\Desktop\\PythonWorkspace\\bosol\\volatility3-develop\\vol.py'
volatility2 = 'C:\\Users\\LINKER\\Desktop\\PythonWorkspace\\bosol\\volatility2\\vol.py'

'''[note] 
boan_sol_win -> windows 10 pro 64bit
boan_sol_win7 -> windows 7 ultimate 64 bit
'''

# 1번 
def vm_start():
    os.system('VBoxManage startvm boan_sol_win7 --type gui')
    print('VM이 실행되었습니다.')
    return

# 2번
def vm_snapshot():
    file_check = glob.glob("D:\\snapshot\\**") # 해당 폴더 내의 모든 파일 출력 - VBox에서 스냅샷 경로 설정 안했음 기본 폴더 확인
    if len(file_check):
        print("스냅샷 파일이 있습니다.\n",file_check,"\n")
      
    else :
        os.system('VBoxManage snapshot boan_sol_win7 take win-test') # 스냅샷 찍기
        print("\n win-test 스냅샷이 생성되었습니다.\n")
    return

# 3번
def file_search():

    total_score = 0

    print("\n해당 작업은 파일을 받고 프로세스모니터 -> 와이어샤크 -> netscan순으로\n작업 후 종료됩니다.\n")
    file_name = input("분석할 파일이름을 입력하세요. -> ")
    add_func = input("테스트용 명령어 인자를 추가해주세요. 없으면 Enter Ex) /all -> ")

    os.system('VBoxManage guestcontrol boan_sol_win7 copyto --target-directory C:\\test C:\\Users\\LINKER\\Desktop\\PythonWorkspace\\bosol\\%s --username test --password 1234 --verbose' % file_name)
    sleep(2)

    # 프로세스 모니터 조종
    os.system('start /b VBoxManage guestcontrol boan_sol_win7 run --exe "C:\Windows\SysWOW64\cmd.exe" --username test --password 1234 /c Procmon /BackingFile C:\\test\\monitor.pml')
  
    sleep(2)
    os.system('start /b VBoxManage guestcontrol boan_sol_win7 run --exe "C:\Windows\SysWOW64\cmd.exe" --username test --password 1234 /c C:\\test\\%s /c %s' % (file_name, add_func))
    sleep(30)
    os.system('start /b VBoxManage guestcontrol boan_sol_win7 run --exe "C:\Windows\SysWOW64\cmd.exe" --username test --password 1234 /c Procmon /Terminate')
    sleep(6)
    os.system('start /b VBoxManage guestcontrol boan_sol_win7 run --exe "C:\Windows\SysWOW64\cmd.exe" --username test --password 1234 /c Procmon /OpenLog C:\\test\\monitor.pml /SaveAs C:\\test\\monitor.csv')
    sleep(10)

    os.system('VBoxManage guestcontrol boan_sol_win7 copyfrom --target-directory C:\\Users\\LINKER\\Desktop\\PythonWorkspace\\bosol\\ C:\\test\\monitor.csv --username test --password 1234 --verbose')

    
    sleep(1) # 종료 직전 메모리 추출 단계 필요!

    print("dump vmem\n")
    os.system('VBoxManage debugvm "boan_sol_win7" dumpvmcore --filename ' + vmemfile)
    sleep(6)
    print("\n"+vmemfile+"파일이 생성되었습니다.\n")
    #check config.json file
    if os.path.isfile(configfile):
        print("Yes. it is a file")
    else :
        print("Nothing")
        os.system('python C:\\Users\\LINKER\\Desktop\\PythonWorkspace\\bosol\\volatility3-develop\\vol.py --write-config -f ' + vmemfile + ' windows.info')
    

    #####################################
    #### procmon을 통한 행위 추출 #######
    df = pd.read_csv("C:/Users/LINKER/Desktop/PythonWorkspace/bosol/monitor.csv", error_bad_lines=False)
    process = df['Process Name'] == file_name ############### 수정해야함
    df_unique = df[process]
    operation = df_unique['Operation'] == 'CreateFile'
    df1 = df_unique[operation]
    df1 = df1[['Path']]
    df1['name'] = df1['Path'].str.extract(r'([^\\/\n]+$)')

    df1 = df1.dropna(axis=0)
    filename = df1['name'].reset_index()
    filename.drop(['index'], axis=1, inplace=True)
    input_name = file_name ##################### 수정해야함. 검사하려는 파일 이름 추가
    filename.loc[0] = [input_name]
    filename.insert(0, 'total', 1)
    file = filename.groupby('total')['name'].unique().loc[1]
    print("생성한 파일: ", file)

    df_final = df[df['Process Name'].isin(file)]
    df1 = df_final.reset_index(drop=True)
    df2 = df1[['Operation', 'Path']]
    df2
    cols = ['Operation',]
    df2.insert(1, 'total', 1)
    df3 = df2.groupby(cols)['total'].sum().reset_index()
    df3 = df3.sort_values(by = 'total')
    df3 = df3.reset_index(drop=True)
    print(df3)

    procmon_score = df3['total'].sum()
    print("procmon 행위 개수 : ", procmon_score)

    # 행위 개수를 통한 스코어링
    if( procmon_score > 6000):
        total_score += 1000
    else:
        total_score += (procmon_score/6000)*1000


    ### Volatility 사용 시작 ###
    print("\n netscan 플러그인 실행")

    def replace_in_file(file_path, old_str, new_str):

        fr = open(file_path, 'r')
        lines = fr.readlines()
        fr.close()

        fw = open(file_path, 'w')
        for line in lines:
            fw.write(line.replace(old_str, new_str))
        fw.close()

    def replace_in_file_cp949(file_path, old_str, new_str):

        fr = open(file_path, 'rt', encoding='cp949')
        lines = fr.readlines()
        fr.close()

        fw = open(file_path, 'w')
        for line in lines:
            fw.write(line.replace(old_str, new_str))
        fw.close()

    #####################
    ### netscan 사용 ###
    os.system('python %s -f %s windows.netscan.NetScan > C:\\Users\\LINKER\\Desktop\\PythonWorkspace\\bosol\\netscan.txt' % (volatility, vmemfile))
    print("\nnetscan 추출 완료.\n")

    replace_in_file('C:\\Users\\LINKER\\Desktop\\PythonWorkspace\\bosol\\netscan.txt',"Volatility 3 Framework 1.2.0", " ")
    ns = pd.read_csv('C:\\Users\\LINKER\\Desktop\\PythonWorkspace\\bosol\\netscan.txt', delimiter = '\t')
    ns.to_csv('C:\\Users\\LINKER\\Desktop\\PythonWorkspace\\bosol\\netscan.csv')
    ns1 = pd.read_csv('C:\\Users\\LINKER\\Desktop\\PythonWorkspace\\bosol\\netscan.csv', sep=",")
    ns1

    try :
        ns1.drop(['Unnamed: 0'], axis = 1, inplace = True)
    except :
        pass

    ns_file = ns1['Owner'] == file_name
    ns2 = ns1[ns_file]

    ns3 = ns2[['ForeignAddr', 'ForeignPort', 'State']]
    ns3 = ns3[ns3.ForeignPort != 0]
    ns3 = ns3.reset_index()
    print("네트워크 연결과정: \n", ns3)
    print("네트워크 연결 횟수: \n", len(ns3)) ### 스코어링 필요
    if(len(ns3) > 2):
        total_score += 1000

    ###################
    ### pslist 사용 ###
    os.system('python %s -f %s windows.pslist.PsList > C:\\Users\\LINKER\\Desktop\\PythonWorkspace\\bosol\\pslist.txt' % (volatility, vmemfile))

    replace_in_file('C:/Users/LINKER/Desktop/PythonWorkspace/bosol/pslist.txt',"Volatility 3 Framework 1.2.0", " ")

    pslist = pd.read_csv('C:/Users/LINKER/Desktop/PythonWorkspace/bosol/pslist.txt', delimiter = '\t')

    scan = pslist['ImageFileName'] == file_name
    pslist = pslist[scan]
    pslist = pslist.reset_index(drop=True)

    ### 실행한 프로세스의 PID
    try:
        ps_pid_num = pslist['PID'][0]
    except:
        ps_pid_num = 0
        print("PID를 불러올 수 없습니다.")

    createtime = pslist['CreateTime'].apply(lambda x: datetime.strptime(x, "%Y-%m-%d %H:%M:%S.%f "))
    try:
        exittime = pslist['ExitTime'].apply(lambda y: datetime.strptime(y, "%Y-%m-%d %H:%M:%S.%f "))
        def get_seconds(time_delta):
            return time_delta.seconds

        date_diff = exittime - createtime
        print(date_diff)

        try:
            if (date_diff.apply(get_seconds)[0] < 10): # 10초 이내로 프로세스 종료 되었을 경우
                total_score += 2000;
        except:
            print("\n검사하려는 파일이 종료되지 않았습니다.\n")
    except:
        print("\n검사하려는 파일이 종료되지 않았습니다.\n")


    ####################
    ### envars 사용 ####
    os.system('python %s -f %s windows.envars.Envars > C:\\Users\\LINKER\\Desktop\\PythonWorkspace\\bosol\\envars.txt' % (volatility, vmemfile))
  
    replace_in_file('C:/Users/LINKER/Desktop/PythonWorkspace/bosol/envars.txt',"Volatility 3 Framework 1.2.0", " ")
    envars = pd.read_csv('C:/Users/LINKER/Desktop/PythonWorkspace/bosol/envars.txt', delimiter = '\t')

    scan = envars['Process'] == file_name
    envars = envars[scan]
    sysroot = envars['Variable'] == 'SystemRoot'
    sysroot_num = len(envars[sysroot].index)
    print("systemroot 접근 횟수: ", sysroot_num) # 접근 횟수 별 스코어링 필요

    windir = envars['Variable'] == 'windir'
    windir_num = len(envars[windir].index)
    print("windir 접근 횟수: ", windir_num) # 접근 횟수 별 스코어링 필요
    if(sysroot_num >= 1 or windir_num >= 1  ):
        total_score += 2000

    ##############################################
    ### malfind 사용, 파이썬 2 버전 사용해야 함.###
    if(ps_pid_num != 0):
        os.system('python2 %s -f %s --profile Win7SP1x64 -p %d malfind > C:\\Users\\LINKER\\Desktop\\PythonWorkspace\\bosol\\malfind.txt' % (volatility2, vmemfile, ps_pid_num))
        print("\nnetscan 추출 완료.\n")

        def findTextCountInText(fname, word):
            cOunt = 0
            with open(fname, 'r') as f:
                for line in f:
                    if word in line:
                        cOunt = cOunt + 1
            return cOunt
        print("\nVadS Protection 개수 : ", findTextCountInText('C:\\Users\\LINKER\\Desktop\\PythonWorkspace\\bosol\\malfind.txt', 'VadS Protection'))  ## 스코어링 필요 
        print("\nPAGE_EXECUTE_READWRITE 개수 : ", findTextCountInText('C:\\Users\\LINKER\\Desktop\\PythonWorkspace\\bosol\\malfind.txt', 'PAGE_EXECUTE_READWRITE'))

        VadS_count = findTextCountInText('C:\\Users\\LINKER\\Desktop\\PythonWorkspace\\bosol\\malfind.txt', 'VadS Protection')
        PageRW_count = findTextCountInText('C:\\Users\\LINKER\\Desktop\\PythonWorkspace\\bosol\\malfind.txt', 'PAGE_EXECUTE_READWRITE')
        if(VadS_count > 1 or PageRW_count > 1):
            total_score += 4000
    else:
        print("\nVadS Protection가 없습니다. ") 
        print("\nPAGE_EXECUTE_READWRITE가 없습니다.")

    if(total_score >= 6000):
        print("\n=====================")
        print("\n악성 파일 입니다.\n")
        print("=====================\n")
    else:
        print("\n=====================")
        print("\n정상 파일 입니다.\n")
        print("=====================\n")

    os.system('VBoxManage controlvm boan_sol_win7 poweroff')
    print('VM이 종료되었습니다.\n')
    sleep(1)
    os.system('VBoxManage snapshot boan_sol_win7 restore win-test') #스냅샷 시점으로 복원
    os.system('VBoxManage startvm boan_sol_win7 --type gui')
    print("프로그램 실행 전 상태로 복원되었습니다.\n")

    return

# 4번
def vm_snapdelete():
    print("x")
    