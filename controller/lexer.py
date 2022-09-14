class Lexer:
    def __init__(self):
        self.states = []
        self.alphabet = []
        self.transitions = []
        self.initial_state = None
        self.final_states = []
