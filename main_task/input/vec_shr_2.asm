start:
    ; Инициализация вектора A (адреса 0..7)
    acc = 4095
    mem[0] = acc ; 4095
    mem[1] = acc ; 4095
    mem[2] = acc ; 4095
    mem[3] = acc ; 4095
    mem[4] = acc ; 4095
    mem[5] = acc ; 4095
    mem[6] = acc ; 4095
    mem[7] = acc ; 4095

    ; Инициализация вектора B (адреса 10..17)
    acc = 0
    mem[10] = acc ; B[0] = 0
    acc = 1
    mem[11] = acc ; B[1] = 1
    acc = 2
    mem[12] = acc ; B[2] = 2
    acc = 3
    mem[13] = acc ; B[3] = 3
    acc = 4
    mem[14] = acc ; B[4] = 4
    acc = 8
    mem[15] = acc ; B[5] = 8
    acc = 11
    mem[16] = acc ; B[6] = 11
    acc = 12
    mem[17] = acc ; B[7] = 12

    ; Поэлементный логический сдвиг вправо (адреса 20..27)
    acc = 0
    acc = mem[acc] ; acc = A[0] (4095)
    acc = acc >> mem[10] ; 4095 >> 0 = 4095
    mem[20] = acc ; C[0] = 4095

    acc = 1
    acc = mem[acc] ; acc = A[1] (4095)
    acc = acc >> mem[11] ; 4095 >> 1 = 2047
    mem[21] = acc ; C[1] = 2047

    acc = 2
    acc = mem[acc] ; acc = A[2] (4095)
    acc = acc >> mem[12] ; 4095 >> 2 = 1023
    mem[22] = acc ; C[2] = 1023

    acc = 3
    acc = mem[acc] ; acc = A[3] (4095)
    acc = acc >> mem[13] ; 4095 >> 3 = 511
    mem[23] = acc ; C[3] = 511

    acc = 4
    acc = mem[acc] ; acc = A[4] (4095)
    acc = acc >> mem[14] ; 4095 >> 4 = 255
    mem[24] = acc ; C[4] = 255

    acc = 5
    acc = mem[acc] ; acc = A[5] (4095)
    acc = acc >> mem[15] ; 4095 >> 8 = 15
    mem[25] = acc ; C[5] = 15

    acc = 6
    acc = mem[acc] ; acc = A[6] (4095)
    acc = acc >> mem[16] ; 4095 >> 11 = 1
    mem[26] = acc ; C[6] = 1

    acc = 7
    acc = mem[acc] ; acc = A[7] (4095)
    acc = acc >> mem[17] ; 4095 >> 12 = 0
    mem[27] = acc ; C[7] = 0