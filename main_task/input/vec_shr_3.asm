start:
    ; Инициализация вектора A (адреса 0..7)
    acc = 0
    mem[0] = acc ; A[0] = 0
    acc = 1
    mem[1] = acc ; A[1] = 1
    acc = 827
    mem[2] = acc ; A[2] = 827
    acc = 1000
    mem[3] = acc ; A[3] = 1000
    acc = 255
    mem[4] = acc ; A[4] = 255
    acc = 1024
    mem[5] = acc ; A[5] = 1024
    acc = 3000
    mem[6] = acc ; A[6] = 3000
    acc = 4000
    mem[7] = acc ; A[7] = 4000

    ; Инициализация вектора B (адреса 10..17)
    acc = 5
    mem[10] = acc ; B[0] = 5
    acc = 0
    mem[11] = acc ; B[1] = 0
    acc = 2
    mem[12] = acc ; B[2] = 2
    acc = 10
    mem[13] = acc ; B[3] = 10
    acc = 8
    mem[14] = acc ; B[4] = 8
    acc = 32
    mem[15] = acc ; B[5] = 32
    acc = 40
    mem[16] = acc ; B[6] = 40
    acc = 1
    mem[17] = acc ; B[7] = 1

    ; Поэлементный логический сдвиг вправо (адреса 20..27)
    acc = 0
    acc = mem[acc] ; acc = A[0] (0)
    acc = acc >> mem[10] ; 0 >> 5 = 0
    mem[20] = acc ; C[0] = 0

    acc = 1
    acc = mem[acc] ; acc = A[1] (1)
    acc = acc >> mem[11] ; 1 >> 0 = 1
    mem[21] = acc ; C[1] = 1

    acc = 2
    acc = mem[acc] ; acc = A[2] (827)
    acc = acc >> mem[12] ; 827 >> 2 = 206
    mem[22] = acc ; C[2] = 206

    acc = 3
    acc = mem[acc] ; acc = A[3] (1000)
    acc = acc >> mem[13] ; 1000 >> 10 = 0
    mem[23] = acc ; C[3] = 0

    acc = 4
    acc = mem[acc] ; acc = A[4] (255)
    acc = acc >> mem[14] ; 255 >> 8 = 0
    mem[24] = acc ; C[4] = 0

    acc = 5
    acc = mem[acc] ; acc = A[5] (1024)
    acc = acc >> mem[15] ; 1024 >> 32 = 0
    mem[25] = acc ; C[5] = 0

    acc = 6
    acc = mem[acc] ; acc = A[6] (3000)
    acc = acc >> mem[16] ; 3000 >> 40 = 0
    mem[26] = acc ; C[6] = 0

    acc = 7
    acc = mem[acc] ; acc = A[7] (4000)
    acc = acc >> mem[17] ; 4000 >> 1 = 2000
    mem[27] = acc ; C[7] = 2000