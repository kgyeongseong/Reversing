#include <ntifs.h>
#include <ntddk.h>

PCHAR PsGetProcessImageFileName(PEPROCESS Process);
VOID CreateThreadNotify(HANDLE ProcessId, HANDLE ThreadId, BOOLEAN Create);
void HookTest1DriverUnload(PDRIVER_OBJECT DriverObject);
void InstallHook();

extern "C" NTSTATUS DriverEntry(PDRIVER_OBJECT DriverObject, PUNICODE_STRING)
{
    UNREFERENCED_PARAMETER(DriverObject);
    
    InstallHook();

    DriverObject->DriverUnload = HookTest1DriverUnload;

    return STATUS_SUCCESS;
}

void InstallHook()
{
    NTSTATUS status;

    status = PsSetCreateThreadNotifyRoutine(CreateThreadNotify);

    if (NT_SUCCESS(status)) KdPrint(("PsSetCreateThreadNotifyRoutine CreateThreadNotify=%p\r\n", CreateThreadNotify));
    else KdPrint(("PsSetCreateThreadNotifyRoutine status=%d\r\n", status));
}

VOID CreateThreadNotify(HANDLE ProcessId, HANDLE ThreadId, BOOLEAN Create)
{
    PEPROCESS Process = NULL;
    PETHREAD Thread = NULL;
    NTSTATUS status;
    UCHAR* pWin32Address = NULL;

    if (Create) {
        // 1. Obtain EPROCESS by process ID
// 1. 프로세스 ID로 EPROCESS 구조체 얻기
        status = PsLookupProcessByProcessId(ProcessId, &Process);

        if (!NT_SUCCESS(status)) {
            KdPrint(("PsLookupProcessByProcessId fail 0x%08X\n", status));
            return;
        }

        // 2. Get ETHREAD by thread ID
        // 2. 스레드 ID로 ETHREAD 구조체 얻기
        status = PsLookupThreadByThreadId(ThreadId, &Thread);

        if (!NT_SUCCESS(status)) {
            KdPrint(("PsLookupThreadByThreadId fail 0x%08X\n", status));
            return;
        }

        auto size = 300;
        PUNICODE_STRING pTargetProcessName = (UNICODE_STRING*)ExAllocatePool(PagedPool, size);
        PUNICODE_STRING pCalc = (UNICODE_STRING*)ExAllocatePool(PagedPool, size);
        RtlCreateUnicodeString(pCalc, L"\\Device\\HarddiskVolume1\\Windows\\System32\\calc.exe");

        status = SeLocateProcessImageName(Process, &pTargetProcessName);

        if (!NT_SUCCESS(status)) {
            KdPrint(("SeLocateProcessImageName fail 0x%08X\n", status));
            return;
        }

        //KdPrint(("Pid %p - Tid %p -  %wZ\n", ProcessId, ThreadId, pTargetProcessName));

        // 4. Determine whether the process name is a calculator
        // 4. 프로세스 대상 정하기
        if (RtlEqualUnicodeString(pTargetProcessName, pCalc, TRUE)) {

            //5. If yes. Find the callback function address. And change it to C3
            //Modify the callback function code
            pWin32Address = *(UCHAR**)((UCHAR*)Thread + 0x394);

            if (MmIsAddressValid(pWin32Address)) {
                *pWin32Address = 0xC3;
            }
        }

        if (pTargetProcessName != nullptr) {
            ExFreePool(pTargetProcessName);
            pTargetProcessName = NULL;
        }
    }
    else KdPrint(("Exit Thread"));

    if (Process) ObDereferenceObject(Process); //reference count--
    if (Thread) ObDereferenceObject(Thread);
}

void HookTest1DriverUnload(PDRIVER_OBJECT DriverObject)
{
    UNREFERENCED_PARAMETER(DriverObject);

    PsRemoveCreateThreadNotifyRoutine(CreateThreadNotify);
}