from game import Character


class Neuron:
    """A neuron for the neuronal field."""
    def __init__(self, entry, output, w):
        self.entry = entry
        self.output = output
        self.W = w
        self.to_be_send = 0

    def update(self, v):
        """
        Updates the neuron state.
        :param v: The inputs values.
        :return: None
        """
        self.to_be_send = 0
        for x, e in enumerate(v):
            self.to_be_send += self.W[x] * e

    def set_genome(self, w):
        """
        Sets the neuron genome.
        :param w: The new genome.
        :return: None
        """
        self.W = w


class Controller:
    """
    Handles a character.
    """
    def __init__(self, character):
        self.current_entry = []
        self.character = character

    def check_entry(self):
        pass

    def play(self):
        pass
