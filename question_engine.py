import random

def generate_question(addition, multiplication, division, integers, decimals, fractions):
    operator_list = [op for op, include in zip(["+", "*", "/"], [addition, multiplication, division]) if include]
    number_type_list = [nt for nt, include in zip(["int", "dec", "frac"], [integers, decimals, fractions]) if include]

    if not operator_list: 
        operator_list = ["+"]
    if not number_type_list:
        number_type_list = ["int"]

    operator = random.choice(operator_list)
    number_type = random.choice(number_type_list)

    mapping = {
        ("+", "int"): generate_add_int_question,
        ("+", "dec"): generate_add_dec_question,
        ("+", "frac"): generate_add_int_question,
        ("*", "int"): generate_mul_int_question,
        ("*", "dec"): generate_mul_dec_question,
        ("*", "frac"): generate_mul_int_question,
        ("/", "int"): generate_div_int_question,
        ("/", "dec"): generate_div_dec_question,
        ("/", "frac"): generate_div_int_question}

    generate_function = mapping.get((operator, number_type))
    return generate_function() 

def generate_add_int_question(): 
    a = random.randint(-999,999)
    b = random.randint(-999,999)
    c = int(a + b)

    if b < 0: 
        op = "-"
        b = -b 
    else: 
        op = "+"
    question, correct = create_question_string(op, a,b,c)    
    
    options = generate_int_options(correct)
    return question, correct, options 

def generate_mul_int_question():
    a = random.randint(-99,99)
    b = random.randint(-99,99)
    c = int(a * b)

    question, correct = create_question_string("*", a,b,c)    
    
    options = generate_int_options(correct)
    return question, correct, options 

def generate_div_int_question():
    b = random.randint(-99,99)
    while (b == 0):
        b = random.randint(-99,99)
    c = random.randint(-99,99)
    a = int(b * c)

    question, correct = create_question_string("/", a, b, c)    
    
    options = generate_int_options(correct)
    return question, correct, options 

def generate_add_dec_question(): 
    a = random.randint(-999,999) / random.choice([1,10,100])
    b = random.randint(-999,999) / random.choice([1,10,100])
    c = round(a + b, 8)

    if b < 0: 
        op = "-"
        b = -b 
    else: 
        op = "+"
    question, correct = create_question_string(op, a,b,c)    
    
    options = generate_dec_options(correct)
    return question, correct, options 

def generate_mul_dec_question():
    a = random.randint(-99,99) / random.choice([1,10,100])
    b = random.randint(-99,99) / random.choice([1,10,100])
    c = round(a * b, 8)

    question, correct = create_question_string("*", a,b,c)    
    
    options = generate_dec_options(correct)
    return question, correct, options 

def generate_div_dec_question():
    b = random.randint(-99,99) / random.choice([1,10,100])
    while (b == 0):
        b = random.randint(-99,99) / random.choice([1,10,100])
    c = random.randint(-99,99) / random.choice([1,10,100])
    a = round(b * c, 8)

    question, correct = create_question_string("/", a, b, c)    
    
    options = generate_dec_options(correct)
    return question, correct, options 

def generate_int_options(correct):
    wrongs = [
        correct + random.randint(-100, -11), 
        correct + random.randint(-10, -6), 
        correct + random.randint(-5, -3), 
        correct-10, correct-2, correct-1, correct+1, correct+2, correct+10, 
        correct + random.randint(3, 5), 
        correct + random.randint(6, 10),
        correct + random.randint(11, 100)]
    random.shuffle(wrongs)

    options = wrongs[:3] + [correct]
    random.shuffle(options)
    return options

def generate_dec_options(correct):
    wrongs = [
        correct + random.randint(-100, -11) / 100, 
        correct + random.randint(-10, -6) / 100, 
        correct + random.randint(-5, -3) / 100, 
        correct-1, correct- 0.1, correct-0.01, correct+0.01, correct+0.1,correct+1, 
        correct + random.randint(3, 5) / 100, 
        correct + random.randint(6, 10) / 100,
        correct + random.randint(11, 100) / 100,
        correct / 10, correct * 10, correct / 100, correct * 100]
    random.shuffle(wrongs)

    options = wrongs[:3] + [correct]
    options = [round(opt,8) for opt in options]
    random.shuffle(options)
    return options

def create_question_string(op, a, b, c): 
    hidden = random.choice([0,1,2])
    if hidden == 0:
        question = f"? {op} {b} = {c}"
        correct = a
    elif hidden == 1:
        question = f"{a} {op} ? = {c}"
        correct = b
    else:
        question = f"{a} {op} {b} = ?"
        correct = c
    return question, correct