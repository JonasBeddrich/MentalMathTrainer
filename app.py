import time 
import streamlit as st
from question_engine import generate_question

# Initialization 

def reset_question_counter(): 
    st.session_state.count = 1

if "count" not in st.session_state:
    reset_question_counter() 

if "page" not in st.session_state:
    st.session_state.page = "home"

if "question" not in st.session_state: 
    st.session_state.question = generate_question() 

# Logic 

def new_question(was_correct):
    st.session_state.question = generate_question() 
    st.session_state.count += 1 

def restart(): 
    st.session_state.question = generate_question() 
    st.session_state.page = "home"

# UI 

# Home page 

if st.session_state.page == "home":
    st.title("Mental Math Trainer")
    reset_question_counter()
    
    col1, col2 = st.columns(2, gap="small")
    with col1: 
        st.session_state.n_questions = st.number_input("Number of questions: ", value = 10)
    with col2: 
        st.session_state.time_limit = 60 * st.number_input("Time limit (minutes): ", value = 2)

    if st.button("Start"):
        st.session_state.page = "question"
        st.session_state.start_time = time.time() 
        st.rerun()

# Question page 

elif st.session_state.page == "question":    

    question, correct, answers = st.session_state.question

    elapsed = time.time() - st.session_state.start_time
    remaining = int(max(0.0, st.session_state.time_limit - elapsed))
    
    if remaining <= 0:
        st.session_state.page = "home" 
        st.rerun()

    if st.session_state.count > st.session_state.n_questions: 
        st.success(f"{st.session_state.count},{st.session_state.n_questions}")
        st.session_state.page = "home" 
        st.rerun() 

    st.title("Mental Math Trainer")

    col1, col2 = st.columns(2, gap="small") 

    with col1:
        st.markdown(f'<div style="text-align: left;">Question {st.session_state.count}</div>', unsafe_allow_html=True)

    with col2: 
        timer_placeholder = st.empty() 

    st.markdown(f"""<div style="text-align: center; margin-top: 20px; margin-bottom: 20px;">
        <h1 style="font-size: 60px; font-weight: 800;">
            {question}
        </h1>
        </div>""", unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4, gap="small")

    with col1: 
        st.button(f"{answers[0]}", on_click=new_question, args=(answers[0] == correct,),use_container_width=True) 
    with col2:
        st.button(f"{answers[1]}", on_click=new_question, args=(answers[1] == correct,),use_container_width=True)
    with col3:
        st.button(f"{answers[2]}", on_click=new_question, args=(answers[2] == correct,),use_container_width=True)
    with col4:
        st.button(f"{answers[3]}", on_click=new_question, args=(answers[3] == correct,),use_container_width=True)
    
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