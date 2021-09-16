"""
@Author: Longxiang Zhang

Example app built using streamlit for annotation type of task
"""
import jsonlines
import numpy as np
import os
import pandas as pd
import streamlit as st


@st.cache(ttl=1800)
def load_data(file):
    results = []
    with jsonlines.open(file) as reader:
        for obj in reader:
            results.append(obj)
    out = pd.DataFrame(results)
    return out


def navigate_data(limit=np.inf, direction='f'):
    loc = st.session_state.data_pointer
    if direction == 'f':
        loc = min(limit, loc+1)
        st.session_state.current_annotation = st.session_state.data_annotation[loc]
        st.session_state.data_pointer = loc
    else:
        loc = max(0, loc-1)
        st.session_state.current_annotation = st.session_state.data_annotation[loc]
        st.session_state.data_pointer = loc


def format_snippet(text):
    return text.replace('this', '**This**').replace('\n', '  \n:male-doctor: ')


def format_summary(text):
    return text


def set_session_states():
    # set session wide state variables
    if 'data_pointer' not in st.session_state:
        st.session_state.data_pointer = 0  # used to navigate dataset
    if 'data_frame' not in st.session_state:
        st.session_state.data_frame = load_data('test_data.jsonl')  # used to store annotation results
    if 'data_annotation' not in st.session_state:
        st.session_state.data_annotation = [None] * st.session_state.data_frame.shape[0]


def update_data():
    loc = st.session_state.data_pointer
    st.session_state.data_annotation[loc] = st.session_state.current_annotation


def save_data(file='test_results.jsonl'):
    update_data()
    df = st.session_state.data_frame
    df['annotation'] = [x if x else None for x in st.session_state.data_annotation]
    with jsonlines.open(file, 'w') as writer:
        for (i, row) in df.iterrows():
            writer.write(row.to_dict())


def main():
    st.title('Example annotaton task')

    set_session_states()

    df = st.session_state.data_frame
    loc = st.session_state.data_pointer

    snippet_container, summary_container = st.columns(2)
    with snippet_container:
        snippet = format_snippet(df.iloc[loc]['snippet'])
        snippet_cell = st.markdown(snippet)
    with summary_container:
        summary = format_summary(df.iloc[loc]['summary'])
        summary_cell = st.text(summary)
    
    prev_button = st.button('previous', on_click=navigate_data, kwargs=dict(direction='b', limit=df.shape[0]-1))
    next_button = st.button('next', on_click=navigate_data, kwargs=dict(direction='f', limit=df.shape[0]-1))

    labelset = ['valid', 'hallucinated', 'inaccurate', 'irrelevant']
    # buttonarray = st.columns(len(labelset))
    # for (label, container) in zip(labelset, buttonarray):
    #     with container:
    #         st.button(label)

    annotation = st.multiselect('Select a label', labelset, default=None, on_change=update_data, key='current_annotation')

    save_button = st.button('save', on_click=save_data)
    

if __name__ == '__main__':
    main()
   

    