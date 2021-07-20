# stage1
f = open('C:\\Users\\root\\Downloads\\section_encrypt\\oh_sad_copy.exe', 'rb') # 바이너리 읽기 모드
data = f.read()
print(len(data))
for i in range(0x400, 0x1BFF+1):
    print("%X" % data[i], end=' ')
tmp = data
f.close()

print("\nstage2\n")
print(type(tmp))

bTmp = bytearray(tmp)

# stage2
for i in range(0x400, 0x1BFF+1):
    print(bTmp[i] ^ 0x20, end=' ')
    bTmp[i] = (int(hex(tmp[i]), 16) ^ 0x20)

print("\nstage3\n")

# stage3
f = open('C:\\Users\\root\\Downloads\\section_encrypt\\oh_sad_test.exe', 'wb') # 바이너리 쓰기 모드
f.write(bTmp)
f.close()