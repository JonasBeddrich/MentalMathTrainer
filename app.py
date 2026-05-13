import time 
import streamlit as st
from question_engine import generate_question

################################################
# Initialization 
################################################

def reset_question_counter(): 
    st.session_state.count = 1

def reset_score(): 
    st.session_state.score = 0

if "page" not in st.session_state:
    st.session_state.page = "home"

if "addition" not in st.session_state:
    st.session_state.addition = True 
if "multiplication" not in st.session_state:
    st.session_state.multiplication = True 
if "division" not in st.session_state:    
    st.session_state.division = True
if "integers" not in st.session_state:    
    st.session_state.integers = True
if "decimals" not in st.session_state:    
    st.session_state.decimals = True
if "fractions" not in st.session_state:    
    st.session_state.fractions = True

if "count" not in st.session_state:
    reset_question_counter() 
if "score" not in st.session_state: 
    reset_score()

if "results" not in st.session_state:
    st.session_state.results = None 

################################################
# Logic 
################################################

def new_question(was_correct):
    if was_correct: 
        st.session_state.score += 1
    st.session_state.question = generate_question(st.session_state.addition, st.session_state.multiplication, st.session_state.division, st.session_state.integers, st.session_state.decimals, st.session_state.fractions) 
    st.session_state.count += 1 

def restart(): 
    st.session_state.question = generate_question(st.session_state.addition, st.session_state.multiplication, st.session_state.division, st.session_state.integers, st.session_state.decimals, st.session_state.fractions) 
    st.session_state.page = "home"

def calculate_quiz_results():
    """Calculate quiz metrics from session state."""
    correct_count = st.session_state.score
    questions_answered = st.session_state.count - 1
    total_time = time.time() - st.session_state.start_time
    avg_time = total_time / questions_answered if questions_answered > 0 else 0
    
    return {
        "correct_count": correct_count,
        "questions_answered": questions_answered,
        "total_time": total_time,
        "avg_time": avg_time
    }

def redo_quiz():
    """Reset quiz state and start new quiz with same settings."""
    reset_question_counter()
    reset_score()
    st.session_state.start_time = time.time()
    st.session_state.question = generate_question(st.session_state.addition, st.session_state.multiplication, st.session_state.division, st.session_state.integers, st.session_state.decimals, st.session_state.fractions)
    st.session_state.page = "question"

def go_home_from_results():
    """Return to home page from results, preserving settings."""
    st.session_state.page = "home"
    st.session_state.results = None

def format_number(num):
    """Format a number to display as int if it's a whole number, else as float."""
    if isinstance(num, float) and num.is_integer():
        return int(num)
    return num

################################################
# UI 
################################################

# Home page 

if st.session_state.page == "home":
    st.title("Mental Math Trainer")
    reset_question_counter()
    reset_score() 
    
    col1, col2 = st.columns(2, gap="small")
    with col1: 
        st.session_state.n_questions = st.number_input("Number of questions: ", value = 10)
    with col2: 
        st.session_state.time_limit = 60 * st.number_input("Time limit (minutes): ", value = 2)

    if st.button("Start", type="primary"):
        st.session_state.page = "question"
        st.session_state.start_time = time.time() 
        st.session_state.question = generate_question(st.session_state.addition, st.session_state.multiplication, st.session_state.division, st.session_state.integers, st.session_state.decimals, st.session_state.fractions) 
        st.rerun()

    st.divider() 
    col1, col2, col3 = st.columns(3, gap="small")
    with col1:    
        st.session_state.addition = st.checkbox("Addition",value=True)
    with col2:
        st.session_state.multiplication = st.checkbox("Multiplication",value=True)
    with col3:
        st.session_state.division = st.checkbox("Division",value=True)

    st.divider()
    col1, col2, col3 = st.columns(3, gap="small")
    with col1:
        st.session_state.integers = st.checkbox("Integers",value=True) 
    with col2:
        st.session_state.decimals = st.checkbox("Decimals",value=True)
    with col3:
        st.session_state.fractions = st.checkbox("Fractions",value=False)

# Question page 

elif st.session_state.page == "question":    

    question, correct, answers = st.session_state.question

    elapsed = time.time() - st.session_state.start_time
    remaining = int(max(0.0, st.session_state.time_limit - elapsed))
    
    if remaining <= 0:
        st.session_state.results = calculate_quiz_results()
        st.session_state.page = "results" 
        st.rerun()

    if st.session_state.count > st.session_state.n_questions: 
        st.session_state.results = calculate_quiz_results()
        st.session_state.page = "results" 
        st.rerun() 

    st.title("Mental Math Trainer")

    col1, col2, col3 = st.columns(3, gap="small") 

    with col1:
        st.markdown(f'<div style="text-align: left;">Question {st.session_state.count}</div>', unsafe_allow_html=True)
    with col2: 
        st.markdown(f'<div style="text-align: left;">Score: {st.session_state.score}</div>', unsafe_allow_html=True)
    with col3: 
        timer_placeholder = st.empty() 

    st.markdown(f"""<div style="text-align: center; margin-top: 20px; margin-bottom: 20px;">
        <h1 style="font-size: 60px; font-weight: 800;">
            {question}
        </h1>
        </div>""", unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4, gap="small")

    with col1: 
        st.button(f"{format_number(answers[0])}", on_click=new_question, args=(answers[0] == correct,),use_container_width=True) 
    with col2:
        st.button(f"{format_number(answers[1])}", on_click=new_question, args=(answers[1] == correct,),use_container_width=True)
    with col3:
        st.button(f"{format_number(answers[2])}", on_click=new_question, args=(answers[2] == correct,),use_container_width=True)
    with col4:
        st.button(f"{format_number(answers[3])}", on_click=new_question, args=(answers[3] == correct,),use_container_width=True)
    
    st.divider() 

    st.button("Quit test", on_click=restart, use_container_width=True)
    
    @st.fragment(run_every=0.2)
    def update_timer():
        elapsed = time.time() - st.session_state.start_time
        remaining = int(max(0.0, st.session_state.time_limit - elapsed))

        with timer_placeholder.container(): 
            st.markdown(f"""<div style="display: flex; justify-content: flex-end;"> Timer: {remaining}s </div> """, unsafe_allow_html=True)

        if remaining <= 0:
            st.session_state.page = "home" 
            st.rerun()

    update_timer() 

# Results page

elif st.session_state.page == "results":
    st.title("Quiz complete!")
    
    results = st.session_state.results
    
    # Display metrics in dashboard style
    col1, col2, col3 = st.columns(3, gap="large")
    
    with col1:
        st.markdown(
            f"""
            <div style="text-align: center; padding: 20px; border-radius: 10px; background-color: #e8f4f8;">
                <p style="font-size: 14px; color: #666; margin-bottom: 10px;">Correct Answers</p>
                <p style="font-size: 48px; font-weight: bold; color: #2c5aa0; margin: 0;">{results['correct_count']}/{results['questions_answered']}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown(
            f"""
            <div style="text-align: center; padding: 20px; border-radius: 10px; background-color: #f0e8f4;">
                <p style="font-size: 14px; color: #666; margin-bottom: 10px;">Total Time</p>
                <p style="font-size: 48px; font-weight: bold; color: #6b2c9d; margin: 0;">{format_number(round(results['total_time'], 1))}s</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col3:
        st.markdown(
            f"""
            <div style="text-align: center; padding: 20px; border-radius: 10px; background-color: #f4e8e8;">
                <p style="font-size: 14px; color: #666; margin-bottom: 10px;">Avg Time/Question</p>
                <p style="font-size: 48px; font-weight: bold; color: #9d2c2c; margin: 0;">{format_number(round(results['avg_time'], 2))}s</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    st.divider()
    
    # Action buttons
    col1, col2 = st.columns(2, gap="small")
    
    with col1:
        st.button("Redo quiz", on_click=redo_quiz, use_container_width=True, type="primary")
    
    with col2:
        st.button("Back to home", on_click=go_home_from_results, use_container_width=True)
