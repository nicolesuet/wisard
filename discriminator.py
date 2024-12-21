import random
from bitarray import BitArray
import math

class Discriminator:
    """
    A class that uses RAM-based memory to learn and rank binary patterns.
    """
    def __init__(self, entry_size, tuple_size):
        self.entry_size = entry_size
        self.tuple_size = tuple_size
        self.num_rams = math.ceil(entry_size/tuple_size)

        # Create a pseudo-random mapping of entries to RAMs
        self.tuples_mapping = list(range(entry_size))
        random.shuffle(self.tuples_mapping)

        # Initialize RAMs as bit arrays capable of storing 2^tuple_size patterns
        self.rams = [BitArray(1 << tuple_size) for _ in range(self.num_rams)]

    def train(self, data):
        """
        Train the discriminator by storing binary patterns in the RAMs.

        Args:
            data (list[int]): A binary list representing the input pattern.
        """
        k = 0  # Index in the tuples mapping

        for ram in self.rams:
            addr = 0  # Address to be constructed for the current RAM
            addr_pos = self.tuple_size - 1  # Position to insert the bit

            # Build the address using tuple_size bits
            for _ in range(self.tuple_size):
                if k >= self.entry_size:
                    break
                mapped_index = self.tuples_mapping[k]  # Map to shuffled index
                addr |= (data[mapped_index] << addr_pos)
                addr_pos -= 1  # Move to the next bit position
                k += 1

            # Store the constructed address in the RAM
            ram.set_bit(addr)

    # def rank(self, data):
        # """
        # Compute the rank (count of matching patterns) for the given input data.

        # Args:
        #     data (list[int]): A binary list representing the input pattern.

        # Returns:
        #     int: The rank of the input pattern.
        # """
        # rank = 0  # Counter for matching patterns
        # k = 0  # Index in the tuples mapping

        # for ram in self.rams:
        #     addr = 0  # Address to be constructed for the current RAM
        #     addr_pos = self.tuple_size - 1  # Position to insert the bit

        #     # Build the address using tuple_size bits
        #     for _ in range(self.tuple_size):
        #         if k >= self.entry_size:
        #             break
        #         mapped_index = self.tuples_mapping[k]  # Map to shuffled index
                
        #         # Bitwise operations to construct the address:
        #         # Same logic as in train():
        #         # addr |= (data[mapped_index] << addr_pos)
        #         addr |= (data[mapped_index] << addr_pos)

        #         addr_pos -= 1  # Move to the next bit position
        #         k += 1

        #     # Check if the constructed address exists in the RAM
        #     # If the bit at 'addr' is 1, it indicates a match
        #     rank += ram.get_bit(addr)

        # return rank

    def rank(self, data):
        rank = 0
        k = 0

        for i in range(self.num_rams):
            addr_pos = self.tuple_size - 1
            addr = 0

            for j in range(self.tuple_size):
                if k < self.entry_size:
                    addr |= (data[self.tuples_mapping[k]] << addr_pos)
                    addr_pos -= 1
                    k += 1

            i1 = addr >> 6  # Divide by 64 to find the bitarray id
            i2 = addr & 0x3F  # Obtain remainder to access the bitarray position
            rank += (self.rams[i].bitarray[i1] & (1 << i2)) >> i2

        return rank

    def display_info(self):
        """
        Display detailed information about the discriminator configuration and memory usage.
        """
        total_bits = sum(ram.num_bits for ram in self.rams)
        print(f"Discriminator Configuration:")
        print(f"  Entry Size: {self.entry_size}")
        print(f"  Tuple Size: {self.tuple_size}")
        print(f"  Number of RAMs: {self.num_rams}")
        print(f"  RAM Size: {self.rams[0].num_bits} bits per RAM")
        print(f"  Total Bits: {total_bits}")

    def reset(self):
        """
        Reset the discriminator by re-shuffling the mapping and clearing all RAMs.
        """
        random.shuffle(self.tuples_mapping)
        for ram in self.rams:
            ram.reset()

# Example usage
# if __name__ == "__main__":
#     # Create a discriminator with 1024 entries and tuples of size 16
#     discriminator = Discriminator(entry_size=1024, tuple_size=16)

#     # Generate example binary data: alternating 0s and 1s
#     data = [i % 2 for i in range(1024)]

#     # Train the discriminator with the binary data
#     discriminator.train(data)

#     # Compute the rank of the input data
#     print("Rank of input data:", discriminator.rank(data))

#     # Display detailed information about the discriminator
#     discriminator.display_info()
