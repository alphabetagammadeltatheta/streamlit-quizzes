import streamlit as st import PyPDF2 import random import os

def extract_text_from_pdf(pdf_file): reader = PyPDF2.PdfReader(pdf_file) text = "" for page in reader.pages: text += page.extract_text() + "\n" return text

def parse_idioms(text): idioms = {} lines = text.split("\n") for line in lines: parts = line.split(" - ")  # Assuming idioms are formatted as "Idiom - Meaning" if len(parts) == 2: idioms[parts[0].strip()] = parts[1].strip() return idioms

def main(): st.title("PDF-Based Idiom Quiz App") st.sidebar.header("Upload PDF") uploaded_file = st.sidebar.file_uploader("Upload a PDF file", type=["pdf"])

if uploaded_file:
    text = extract_text_from_pdf(uploaded_file)
    idioms_dict = parse_idioms(text)
    
    if idioms_dict:
        st.session_state.idioms = idioms_dict
        st.session_state.correct_answers = 0
        st.session_state.total_questions = 0
        st.session_state.mistakes = {}
        st.session_state.quiz_started = True
    else:
        st.error("No idioms found in the PDF. Please upload a valid file.")

if "quiz_started" in st.session_state and st.session_state.quiz_started:
    idiom, meaning = random.choice(list(st.session_state.idioms.items()))
    st.write(f"What is the meaning of: '{idiom}'?")
    user_answer = st.text_input("Your answer:", key="answer")
    
    if st.button("Submit Answer"):
        st.session_state.total_questions += 1
        if user_answer.lower().strip() == meaning.lower():
            st.session_state.correct_answers += 1
            st.success("Correct!")
        else:
            st.session_state.mistakes[idiom] = st.session_state.mistakes.get(idiom, 0) + 1
            st.error(f"Incorrect. The correct meaning is: {meaning}")
    
    st.write(f"### Progress: {st.session_state.correct_answers}/{st.session_state.total_questions} correct")
    
    if st.session_state.mistakes:
        st.write("### Mistakes analysis:")
        for idiom, count in st.session_state.mistakes.items():
            st.write(f"- {idiom}: {count} mistake(s)")

if name == "main": main()

