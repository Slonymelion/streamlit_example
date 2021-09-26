"""
@Author: Longxiang Zhang

Example app built using streamlit for annotation type of task
"""
import jsonlines
import numpy as np
import os
import pandas as pd
import streamlit as st
import time


#%% session state configuration
def set_session_states():
    # set session wide state variables
    if 'data_pointer' not in st.session_state:
        st.session_state.data_pointer = 0  # used to navigate dataset
    if 'data_frame' not in st.session_state:
        st.session_state.data_frame = load_data('test_data.jsonl')  # used to store annotation results
    if 'data_annotation' not in st.session_state:
        st.session_state.data_annotation = [None] * st.session_state.data_frame.shape[0]


#%% data processing and navigation
@st.cache(ttl=1800)
def load_data(file):
    results = []
    with jsonlines.open(file) as reader:
        for obj in reader:
            results.append(obj)
    out = pd.DataFrame(results)
    return out


def update_data():
    loc = st.session_state.data_pointer
    value = st.session_state.current_annotation
    if value:
        st.session_state.data_annotation[loc] = value


def navigate_data(limit=np.inf, direction='f'):
    update_data()  # save current annotation first
    loc = st.session_state.data_pointer
    if direction == 'f':
        loc = min(limit, loc+1)
    else:
        loc = max(0, loc-1)
    display_label(loc)
    st.session_state.data_pointer = loc


def navigate_data_unlabeled(limit=np.inf, direction='f'):
    # naviage through unlabeled data in the dataset only
    update_data()  # save current annotation first
    loc = st.session_state.data_pointer
    labels = st.session_state.data_annotation
    if direction == 'f':
        try:
            loc = labels[loc+1:].index(None) + loc + 1
            st.session_state.data_pointer = loc
        except:
            st.warning('No unlabeled data found after current sample')
    else:
        try:
            loc = loc - 1 - labels[:loc][::-1].index(None)
            st.session_state.data_pointer = loc
        except:
            st.warning('No unlabeled data found before current sample')
    display_label(loc)
    

def save_data(file='test_results.jsonl'):
    with st.spinner(f'Saving annotation to {file}'):
        update_data()
        df = st.session_state.data_frame
        df['annotation'] = st.session_state.data_annotation
        with jsonlines.open(file, 'w') as writer:
            for (i, row) in df.iterrows():
                writer.write(row.to_dict())
        time.sleep(1)
    st.success('Saved!')


#%% formatting
def format_snippet(text):
    lines = text.split('\n')
    lines[::2] = [':male-doctor: '+x.strip() for x in lines[::2]]
    lines[1::2] = [':hospital: '+x.strip() for x in lines[1::2]]
    return '  \n'.join(['**Snippet**', ' ']+lines)


def format_summary(text):
    return '  \n'.join(['**Summary**', ' ']+[text, ])


def display_label(loc):
    label_loc = st.session_state.data_annotation[loc]
    st.session_state.current_annotation = label_loc if label_loc else []


def navigate_dispmsg():
    n = len(st.session_state.data_annotation)
    loc = st.session_state.data_pointer
    return f'**Viewing:** {loc+1}/{n} Examples'


#%% main
def main():
    st.title('Example annotaton task')

    set_session_states()

    df = st.session_state.data_frame
    loc = st.session_state.data_pointer

    containers = st.columns([0.15, 0.3, 0.4, 0.3, 0.3])
    with containers[3]:
        prev_button = st.button('prev unlabeled', on_click=navigate_data_unlabeled, kwargs=dict(direction='b', limit=df.shape[0]-1))
    with containers[0]:
        prev_button = st.button('prev', on_click=navigate_data, kwargs=dict(direction='b', limit=df.shape[0]-1))
    with containers[1]:
        next_button = st.button('next', on_click=navigate_data, kwargs=dict(direction='f', limit=df.shape[0]-1))
    with containers[4]:
        next_button = st.button('next unlabeled', on_click=navigate_data_unlabeled, kwargs=dict(direction='f', limit=df.shape[0]-1))
    with containers[2]:
        st.markdown(navigate_dispmsg())

    snippet_container, summary_container = st.columns(2)
    with snippet_container:
        snippet = format_snippet(df.iloc[loc]['snippet'])
        snippet_cell = st.markdown(snippet)
    with summary_container:
        summary = format_summary(df.iloc[loc]['summary'])
        summary_cell = st.markdown(summary)
    
    labelset = ['valid', 'hallucinated', 'inaccurate', 'irrelevant']
    # buttonarray = st.columns(len(labelset))
    # for (label, container) in zip(labelset, buttonarray):
    #     with container:
    #         st.button(label)

    annotation = st.multiselect('Select a label', labelset, default=None, on_change=None, key='current_annotation')

    save_button = st.button('save', on_click=save_data)
    

if __name__ == '__main__':
    main()
   

    