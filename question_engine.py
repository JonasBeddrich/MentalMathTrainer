import random

def generate_question():
    a = random.randint(0, 10)
    b = random.randint(0, 10)
    c = a + b
    question = f"{a} + {b} = ?"
    correct = c
    wrongs = [c - 1, c + 1, c + 2]
    options = [correct] + wrongs
    random.shuffle(options)
    return question, correct, options