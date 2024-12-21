from discriminator import Discriminator
import sys

class Wisard:
    """
    A class representing the WiSARD model, which consists of multiple discriminators.
    """
    def __init__(self, entry_size=0, tuple_size=0, num_discriminator=0):
        self.entry_size = entry_size
        self.tuple_size = tuple_size
        self.num_discriminator = num_discriminator
        self.discriminators = []

        # Initialize discriminators if parameters are provided
        for _ in range(num_discriminator):
            self.discriminators.append(Discriminator(entry_size, tuple_size))

    def add_discriminator(self):
        """
        Add a new discriminator to the WiSARD model.
        """
        self.discriminators.append(Discriminator(self.entry_size, self.tuple_size))
        self.num_discriminator += 1

    def train(self, data, labels):
        """
        Train the WiSARD model by training the appropriate discriminator for each labeled data point.

        Args:
            data (list[list[int]]): A list of binary input patterns.
            labels (list[int]): A list of labels corresponding to the input patterns.
        """
        for pattern, label in zip(data, labels):
            self.discriminators[label].train(pattern)

    def rank(self, data):
        """
        Determine the label of the input pattern by finding the discriminator with the highest rank.

        Args:
            data (list[int]): A binary input pattern.

        Returns:
            int: The label of the discriminator with the highest rank.
        """
        max_response = 0
        best_label = 0

        for label, discriminator in enumerate(self.discriminators):
            response = discriminator.rank(data)
            if response > max_response:
                max_response = response
                best_label = label

        return best_label

# Example usage
# if __name__ == "__main__":
#     # Create a WiSARD model with 1024 entries, tuple size of 16, and 3 discriminators
#     wisard = Wisard(entry_size=1024, tuple_size=16, num_discriminator=3)

#     # Example training data (binary patterns) and their labels
#     training_data = [[i % 2 for i in range(1024)], [1 - (i % 2) for i in range(1024)], [i % 2 for i in range(1024)]]
#     training_labels = [0, 1, 2]

#     # Train the model
#     wisard.train(training_data, training_labels)

#     # Test the model with a sample input pattern
#     test_data = [i % 2 for i in range(1024)]
#     print("Predicted Label:", wisard.rank(test_data))
