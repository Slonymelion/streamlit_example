"""
@Author: Longxiang Zhang

Example app built using streamlit for annotation type of task
"""
import jsonlines
import numpy as np
import os
import pandas as pd
import streamlit as st

@st.cache
def load_data(file):
    results = []
    with jsonlines.open(file) as reader:
        for obj in reader:
            results.append(obj)
    return pd.DataFrame(results)


def navigate_data(limit=np.inf, direction='f'):
    if direction == 'f':
        st.session_state.data_pointer = min(limit, st.session_state.data_pointer+1)
    else:
        st.session_state.data_pointer = max(0, st.session_state.data_pointer-1)


def format_snippet(text):
    return text.replace('this', '**This**').replace('\n', '  \n:male-doctor: ')


def format_summary(text):
    return text


def main():
    st.title('Example annotaton task')

    df = load_data('test_data.jsonl')
    if 'data_pointer' not in st.session_state:
        st.session_state.data_pointer = 0

    snippet_container, summary_container = st.columns(2)
    with snippet_container:
        snippet = format_snippet(df.iloc[st.session_state.data_pointer]['snippet'])
        snippet_cell = st.markdown(snippet)
    with summary_container:
        summary = format_summary(df.iloc[st.session_state.data_pointer]['summary'])
        summary_cell = st.text(summary)
    
    prev_button = st.button('previous', on_click=navigate_data, kwargs=dict(direction='b', limit=df.shape[0]-1))
    next_button = st.button('next', on_click=navigate_data, kwargs=dict(direction='f', limit=df.shape[0]-1))

    labelset = ['valid', 'hallucinated', 'inaccurate', 'irrelevant']
    buttonarray = st.columns(len(labelset))
    for (label, container) in zip(labelset, buttonarray):
        with container:
            st.button(label)
    st.multiselect('labels', labelset)
    color = st.select_slider(
        'Select a color of the rainbow',
        options=['red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'violet'])
    st.write('My favorite color is', color)

if __name__ == '__main__':
    main()
   

    