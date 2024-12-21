class BitArray:
    def __init__(self, num_bits):
        self.num_bits = num_bits
        self.bitarray_size = (num_bits + 63) >> 6  # Equivalent to (num_bits + 63) // 64
        self.bitarray = [0] * self.bitarray_size

    def set_bit(self, index):
        array_index = index // 64
        bit_position = index % 64
        self.bitarray[array_index] |= (1 << bit_position)

    def get_bit(self, index):
        array_index = index // 64
        bit_position = index % 64
        return (self.bitarray[array_index] >> bit_position) & 1

    def reset(self):
        self.bitarray = [0] * self.bitarray_size