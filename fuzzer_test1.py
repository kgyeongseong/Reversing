import os
import subprocess
import random
import os
import tempfile

#파이썬을 사용한 fuzzer함수 정의 매개변수는 최대 길이, 시작하는 문자, 문자 선택 범위
def fuzzer(max_length = 100, char_start = 32, char_range = 32):
    string_length = random.randrange(0, max_length + 1)
    out = ""
    for i in range(0, string_length):
        out += chr(random.randrange(char_start, char_start + char_range))
    return out

def makeinput(max_length = 100, char_start = 32, char_range = 32):
    basename = "input.txt"
    tempdir = tempfile.mkdtemp()
    FILE = os.path.join(tempdir, basename)
    print("입력을 위한 파일의 경로 :%s", FILE)
    program = "notepad"
    data = fuzzer(max_length, char_start, char_range)
    with open(FILE, "w") as f:
        f.write(data)
    print("생성된 입력값을 확인합니다.\n")
    contents = open(FILE).read()
    print(contents)
    assert(contents == data)
    print("프로그램을 대상으로 퍼징을 수행합니다.")
    result = subprocess.run([program, FILE], stdin = subprocess.DEVNULL, stdout = subprocess.PIPE, 
                            stderr = subprocess.PIPE, universal_newlines = True)
    result.stdout
    print("결과를 출력합니다.:%s", result)

if __name__ == "__main__":
    makeinput()