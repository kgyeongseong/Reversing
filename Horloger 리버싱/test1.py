# -*- coding: utf-8 -*-

from pydbg import *
from pydbg.defines import *

import threading
import utils
import shutil
import time
import random

class file_fuzzer:
    def __init__(self):
        self.running = False
        self.pid = None
        self.iteration = 0
        self.dbg = None
        self.in_accessv_handler = False
        self.crash = None
        self.test_cases = [ "%s%n%s%n%s%n", "\xff", "\x00", "A"]
    
    def fuzz(self):
        while 1:
            if not self.running:
                # 먼저 변형을 가할 파일을 선택한다.
                self.mutate_file()

                # 디버거 스레드를 실행시킨다.
                pydbg_thread = threading.Thread(target = self.start_debugger)
                pydbg_thread.setDaemon(0)
                pydbg_thread.start()

                while self.pid == None:
                    time.sleep(1)
                
                #모니터링 스레드를 실행시킨다.
                monitor_thread = threading.Thread(target = self.monitor_debugger)
                monitor_thread.setDaemon(0)
                monitor_thread.start()

                self.iteration += 1
            else:
                time.sleep(1)

    #대상 어플리케이션을 실행시키는 디버거 스레드
    def start_debugger(self):
        print "[*] Start debugger for iteration: %d" % self.iteration
        self.running = True
        self.dbg = pydbg()
        self.dbg.set_callback(EXCEPTION_ACCESS_VIOLATION, self.check_accessv)
        pid = self.dbg.load("C:\\Program Files\\Amine Dries\\Horloger\\Horloger.exe")
        self.pid = self.dbg.pid
        self.dbg.run()

    #에러를 추적하고 그것의 정보를 저장하기 위한 접근 위반 핸들러
    def check_accessv(self, dbg):
        if dbg.dbg.u.Exception.dwFirstChance:
            return DBG_CONTINUE
        
        print "[*]Woot! Handling an access violation!"
        self.in_accessv_handler = True
        crash_bin = utils.crash_binning.crach_binning()
        crash_bin.record_crash(dbg)
        self.crash = crash_bin.crash_synopsis()

        #에러 정보를 작성한다.
        crash_fd = open("crashes\\crash-$d" % self.iteration, "w")
        crash_fd.write(self.crash)

        #파일을 백업한다.
        shutil.copy("C:\\Program Files\\Amine Dries\\Horloger\\Lang\\English.ini",
                    "crashes\\%d.English.ini" % self.iteration)
        self.dbg.terminate_process()
        self.in_accessv_handler = False
        self.running = False

        return DBG_EXCEPTION_NOT_HANDLED

    #애플리케이션 몇 초 동안 실행되게 한 다음 그것을 종료시키는 모니터링 스레드
    def monitor_debugger(self):
        counter = 0
        print "[*] Monitor thread for pid: %d waiting." % self.pid

        while counter < 3:
            time.sleep(1)
            print counter
            counter += 1
            if counter == 3:
                print "\n"
        
        if self.in_accessv_handler != True:
            time.sleep(1)
            self.dbg.terminate_process()
            self.pid = None
            self.running = False
        else:
            print "[*]the access violation handler is doing its business. Waiting."

            while self.running:
                time.sleep(1)
    
    def mutate_file(self):
        # 파일의 내용을 버퍼로 읽어 들인다.
        fd = open("C:\\Program Files\\Amine Dries\\Horloger\\Lang\\English.ini", "rb")
        stream = fd.read()
        fd.close()

        #퍼징의 가장 핵심적인 부분이다.
        #임의의 test_case를 선택해 파일 내부의 임의의 위치에 적용한다.
        test_case = self.test_cases[random.randint(0, len(self.test_cases)-1)]
        stream_length = len(stream)
        rand_offset = random.randint(0, stream_length-1)
        rand_len = random.randint(1, 1000)

        #선택한 test_case를 반복시킨다.
        fuzz_file = stream[0:rand_offset]
        fuzz_file += str(test_case)
        fuzz_file += stream[rand_offset:]

        #버퍼의 내용을 파일에 써 넣는다.
        fd = open("C:\\Program Files\\Amine Dries\\Horloger\\Lang\\English.ini", "wb")
        fd.write(fuzz_file)
        fd.close()

if __name__ == "__main__":
    print "[*]Generic File Fuzzer"

    fuzzer = file_fuzzer()
    fuzzer.fuzz()