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

    var ReadFile = Module.findExportByName('kernel32.dll', 'ReadFile');

    // ReadFile API Hook
    Interceptor.attach(ReadFile, {
        onEnter: function(args) {
            this.hFile = args[0];
            this.lpBuffer = args[1];
            this.nNumberOfBytesToRead = args[2];
            this.lpNumberOfBytesRead = args[3];
            this.lpOverlapped = args[4];
        },
        onLeave: function(args) {
            console.log('lpBuffer : ' + this.lpBuffer.readAnsiString());
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