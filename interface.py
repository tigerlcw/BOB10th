import sys
import os
from time import sleep
import pandas as pd
import datetime
from datetime import datetime
import csv
import numpy as np
import re
import procmon_csv_final

def print_menu():
    print('0 = 프로그램 종료') 
    # vm 종료 및 파이썬코드 종료
    print('1 = VM 시작')
    # VM 시작 코드
    print('2 = VM 스냅샷 찍기')
    # VM 스냅샷 찍기
    print('3 = 악성 프로그램 판단')
    # 프로세스모니터 와이어샤크 // 볼라티비티 + 현종이형 코드 + 황병우형 코드 + 스코어링
    print('4 = 공사중')
    return

def main():
    option = -1

    while option != 0:
        print_menu()
        print("=============================================")
        try:
            option = int(input('\n실행하실 메뉴 숫자를 등록해주세요! -> '))
            if option == 0:
                print('프로그램과 VM을 종료합니다.\n')
                os.system('VBoxManage controlvm boan_sol_win poweroff')
            elif option == 1:
                procmon_csv_final.vm_start()
            elif option == 2:
                procmon_csv_final.vm_snapshot()
            elif option == 3:
                procmon_csv_final.file_search()
            elif option == 4:
                procmon_csv_final.vm_snapdelete()
                
            else:
                print('\nERROR: 다시 입력하세요!!!')
        except ValueError:
            print('\nERROR: 다시 입력하세요!!!')
    return
print("=============================================")


# main func()
if __name__ == '__main__':
    main()