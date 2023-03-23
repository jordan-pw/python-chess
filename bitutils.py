import numpy as np

index64_fw = [
    0,  1, 48,  2, 57, 49, 28,  3,
   61, 58, 50, 42, 38, 29, 17,  4,
   62, 55, 59, 36, 53, 51, 43, 22,
   45, 39, 33, 30, 24, 18, 12,  5,
   63, 47, 56, 27, 60, 41, 37, 16,
   54, 35, 52, 21, 44, 32, 23, 11,
   46, 26, 40, 15, 34, 20, 31, 10,
   25, 14, 19,  9, 13,  8,  7,  6
]

index64_bw = [
    0, 47,  1, 56, 48, 27,  2, 60,
   57, 49, 41, 37, 28, 16,  3, 61,
   54, 58, 35, 52, 50, 42, 21, 44,
   38, 32, 29, 23, 17, 11,  4, 62,
   46, 55, 26, 59, 40, 36, 15, 53,
   34, 51, 20, 43, 31, 22, 10, 45,
   25, 39, 14, 33, 19, 30,  9, 24,
   13, 18,  8, 12,  7,  6,  5, 63
]

def square_index_serialization(bitboard):
    move_list = list()
    if bitboard:
        while(bitboard):
            square = bitscan_forward(bitboard)
            move_list.append(square)
            bitboard &= bitboard - np.uint64(1)
    return move_list


def bitscan_forward(bitboard):
    debruijn64 = np.uint64(0x03f79d71b4cb0a89)
    if (bitboard == np.uint64(0)):
        return 0
    return index64_fw[((bitboard & -bitboard) * debruijn64) >> np.uint64(58)]

def bitscan_reverse(bitboard):
    debruijn64 = np.uint64(0x03f79d71b4cb0a89)
    if (bitboard == np.uint64(0)):
        return 0
    bitboard |= bitboard >> np.uint64(1)
    bitboard |= bitboard >> np.uint64(2)
    bitboard |= bitboard >> np.uint64(4)
    bitboard |= bitboard >> np.uint64(8)
    bitboard |= bitboard >> np.uint64(16)
    bitboard |= bitboard >> np.uint64(32)
    return index64_bw[(bitboard * debruijn64) >> np.uint64(58)]

def north_one(bitboard):
    return bitboard << np.uint64(8)

def northwest_one(bitboard):
    return bitboard << np.uint64(7)

def northeast_one(bitboard):
    return bitboard << np.uint64(9)

def west_one(bitboard):
    return bitboard >> np.uint64(1)

def east_one(bitboard):
    return bitboard << np.uint64(1)

def south_one(bitboard):
    return bitboard >> np.uint64(8)

def southwest_one(bitboard):
    return bitboard >> np.uint64(9)

def southeast_one(bitboard):
    return bitboard >> np.uint64(7)