from __future__ import print_function
import frida
import sys

def on_message(message, data):
    print("[%s] => %s" % (message, data))

def main(target_process):
    session = frida.attach(target_process)

    script = session.create_script("""
    console.log('script start');

    // Find base address of current imported kernel32.dll by main process SeiService.exe
    var baseAddr = Module.findBaseAddress('kernel32.dll');
    console.log('kernel32.dll baseAddr: ' + baseAddr);
    var WriteFile = Module.findExportByName('kernel32.dll', 'WriteFile');
    var CreateFileA = Module.findExportByName('kernel32.dll', 'CreateFileA');

    // CreateFileA API Hook
    Interceptor.attach(CreateFileA, {
        onEnter: function(args) {
            this.lpFileName = args[0];
            this.dwDesiredAccess = 0x80000000 | 0x40000000;
            this.dwShareMode = 0x00000001;
            this.lpSecurityAttributes = 0;
            this.dwCreationDisposition = 3;
            this.dwFlagsAndAttributes = 0x00000080 | 0x02000000;
            this.hTemplateFile = args[6];
        },
        onLeave: function(args) {
            console.log('lpFileName : ' + this.lpFileName.readAnsiString());
            console.log('dwDesiredAccess : ' + this.dwDesiredAccess);
            console.log('dwShareMode : ' + this.dwShareMode);
            console.log('lpSecurityAttributes : ' + this.lpSecurityAttributes);
            console.log('dwCreationDisposition : ' + this.dwCreationDisposition);
            console.log('dwFlagsAndAttributes : ' + this.dwFlagsAndAttributes);
            console.log('hTemplateFile : ' + this.hTemplateFile);
        }
    })

    // WrtieFile API Hook
    Interceptor.attach(WriteFile, {
        onEnter: function(args) {
            //send('[+] WriteFile API hooked!');
            // Save the following arguments for onLeave
            this.hFile = args[0];
            this.lpBuffer = args[1];
            this.nNumberOfBytesToWrite = args[2];
            this.lpNumberOfBytesWritten = args[3];
            this.lpOverlapped = args[4];
        },
        onLeave: function(args) {
            //send('[+] Retrieving argument values..');
            //send('================================');
            //send('hFile : ' + this.hFile);
            console.log('lpBuffer : ' + this.lpBuffer.readAnsiString());
            //send('nNumberOfBytesToWrite : ' + this.nNumberOfBytesToWrite.readUtf8String());
            //send('lpNumberOfBytesWritten : ' + this.lpNumberOfBytesWritten.readUtf8String());
            //send('lpOverlapped : ' + this.lpOverlapped.readUtf16String());
        }
    })

    
    """);

    script.on('message', on_message)
    script.load()
    print("[!] Ctrl+D on UNIX, Ctrl+Z on Windows/cmd.exe to detach from instrumented program.\n\n")
    sys.stdin.read()
    session.detach()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: %s <process name or PID>" % __file__)
        sys.exit(1)

    try:
        target_process = int(sys.argv[1])
    except ValueError:
        target_process = sys.argv[1]
    main(target_process)