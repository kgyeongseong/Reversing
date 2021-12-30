#include <iostream>
#include <atlstr.h>

using namespace std;

int main()
{
    CString cString = L"abcd";

    wchar_t v5;
    wchar_t v14[4];
    wchar_t v15[4];
    
    unsigned int nameLength = 0;
    unsigned int i = 0;
    nameLength = wcslen(cString);
    
    while (i < nameLength) {
        v5 = cString.GetAt(i);

        v14[i] = 15 * v5;
        cout << hex << v14[i] << endl;

        ++i;
    }

    return 0;
}
