# https://chatgpt.com/share/f85773e8-094f-42d9-8220-358d74fa144b


class BKT:
    def __init__(self, learn_rate, guess_rate, slip_rate, initial_mastery):
        self.L = learn_rate
        self.G = guess_rate
        self.S = slip_rate
        self.P = initial_mastery

    def update(self, correct):
        if correct:
            P_correct = (self.P * (1 - self.S)) / (self.P * (1 - self.S) + (1 - self.P) * self.G)
        else:
            P_correct = (self.P * self.S) / (self.P * self.S + (1 - self.P) * (1 - self.G))
        
        # Update mastery probability after observation
        self.P = P_correct
        # Update for learning
        self.P = self.P + (1 - self.P) * self.L