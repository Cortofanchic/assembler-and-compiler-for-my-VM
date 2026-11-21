start:
    ; Инициализация вектора A (адреса 0..7)
    acc = 256
    mem[0] = acc ; A[0] = 256
    acc = 512
    mem[1] = acc ; A[1] = 512
    acc = 1024
    mem[2] = acc ; A[2] = 1024
    acc = 2048
    mem[3] = acc ; A[3] = 2048
    acc = 128
    mem[4] = acc ; A[4] = 128
    acc = 64
    mem[5] = acc ; A[5] = 64
    acc = 32
    mem[6] = acc ; A[6] = 32
    acc = 16
    mem[7] = acc ; A[7] = 16

    ; Инициализация вектора B (адреса 10..17)
    acc = 1
    mem[10] = acc ; B[0] = 1
    acc = 2
    mem[11] = acc ; B[1] = 2
    acc = 3
    mem[12] = acc ; B[2] = 3
    acc = 4
    mem[13] = acc ; B[3] = 4
    acc = 5
    mem[14] = acc ; B[4] = 5
    acc = 6
    mem[15] = acc ; B[5] = 6
    acc = 7
    mem[16] = acc ; B[6] = 7
    acc = 8
    mem[17] = acc ; B[7] = 8

    ; Поэлементный логический сдвиг вправо  (адреса 20..27)
    acc = 0
    acc = mem[acc] ; acc = A[0] (256)
    acc = acc >> mem[10] ; 256 >> 1 = 128
    mem[20] = acc ; C[0] = 128

    acc = 1
    acc = mem[acc] ; acc = A[1] (512)
    acc = acc >> mem[11] ; 512 >> 2 = 128
    mem[21] = acc ; C[1] = 128

    acc = 2
    acc = mem[acc] ; acc = A[2] (1024)
    acc = acc >> mem[12] ; 1024 >> 3 = 128
    mem[22] = acc ; C[2] = 128

    acc = 3
    acc = mem[acc] ; acc = A[3] (2048)
    acc = acc >> mem[13] ; 2048 >> 4 = 128
    mem[23] = acc ; C[3] = 128

    acc = 4
    acc = mem[acc] ; acc = A[4] (128)
    acc = acc >> mem[14] ; 128 >> 5 = 4
    mem[24] = acc ; C[4] = 4

    acc = 5
    acc = mem[acc] ; acc = A[5] (64)
    acc = acc >> mem[15] ; 64 >> 6 = 1
    mem[25] = acc ; C[5] = 1

    acc = 6
    acc = mem[acc] ; acc = A[6] (32)
    acc = acc >> mem[16] ; 32 >> 7 = 0
    mem[26] = acc ; C[6] = 0

    acc = 7
    acc = mem[acc] ; acc = A[7] (16)
    acc = acc >> mem[17] ; 16 >> 8 = 0
    mem[27] = acc ; C[7] = 0