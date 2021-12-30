def key_gen(_name):
    name = _name
    v15 = []
    v15_str = ""
    v15_reversed = ""
    v16 = ""
    for i in range(0, len(name)):
        v14 = format(15 * ord(name[i]), 'x')
        v15.insert(i, str(v14))

    # make string
    for i in range(0, len(v15)):
        for j in range(0, len(v15[i])):
            v15_str += v15[i][j]

    # make reverse
    v15_reversed = v15_str[::-1]

    # make upper
    v16 = v15_reversed.upper()

    print(v16)

if __name__ == '__main__':
    name = input()
    key_gen(name)