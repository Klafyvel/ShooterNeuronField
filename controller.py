from game import Character


class Neuron:
    def __init__(self, entry, output, w):
        self.entry = entry
        self.output = output
        self.W = w
        self.to_be_send = 0

    def update(self, v):
        self.to_be_send = 0
        for x, e in enumerate(v):
            self.to_be_send += self.W[x] * e

    def send(self):
        self.output(self.to_be_send)

    def set_genome(self, w):
        self.W = w


class Controller:
    def __init__(self, character):
        self.current_entry = []
        self.character = character

    def check_entry(self):
        pass

    def play(self):
        pass
