def key_gen(_name):
    name = _name
    count = 0
    v5 = []
    v6 = []
    v7 = []
    v8 = []
    v9 = []
    v18 = ""
    v19 = []
    v20 = ""
    v20_reversed = ""
    for i in range(0, len(name)):
        count = i
        v5 = ord(name[count])
        v6 = v5 * ord(name[count])
        v7 = v6 * ord(name[i])
        v8 = v7 * ord(name[i])
        v9.insert(i, ord(name[i]))
        v19.insert(i, format((v8 * v9[i]), 'x'))

    # make string
    for i in range(0, len(v19)):
        for j in range(0, len(v19[i])):
            v20 += v19[i][j]

    # make reverse
    v20_reversed += v20[::-1]

    # make upper
    v18 = v20_reversed.upper()

    print(v18)

if __name__ == '__main__':
    key_gen("Anime")
    key_gen("중급 리버서/43/RCE,Linux.")