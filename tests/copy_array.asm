; Запись исходного массива [100, 200, 300, 400] в адреса 10..13
acc = 100
mem[10] = acc

acc = 200
mem[11] = acc

acc = 300
mem[12] = acc

acc = 400
mem[13] = acc

; Копирование элементов с адресов 10..13 в адреса 20..23
acc = 10
acc = mem[acc]
mem[20] = acc

acc = 11
acc = mem[acc]
mem[21] = acc

acc = 12
acc = mem[acc]
mem[22] = acc

acc = 13
acc = mem[acc]
mem[23] = acc