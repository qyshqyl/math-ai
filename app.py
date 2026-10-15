import json
import os
import random
import re
import streamlit as st
from math_engine import TRIPLES, Problem, validate, question, steps, is_correct
from prompts import SYSTEM_PROMPT, generation_prompt

st.set_page_config(page_title='AI Pythagoras Lab',page_icon='📐',layout='centered')
st.markdown('''<style>.block-container{max-width:820px;padding-top:2rem} .stButton>button{border-radius:12px} h1{color:#254d85}</style>''',unsafe_allow_html=True)
st.title('📐 AI Pythagoras Lab')
st.caption('Grade 8 • AI for Differentiated Learning • Adaptive Geometry')
st.write('Choose your level, generate a new right-triangle challenge, and learn at your own pace.')

try:
    API_KEY=st.secrets.get('GEMINI_API_KEY','')
except (FileNotFoundError, KeyError):
    API_KEY=''
API_KEY=API_KEY or os.getenv('GEMINI_API_KEY','')


def ai_generate(level: str, previous: list[str]) -> Problem:
    if not API_KEY:
        raise RuntimeError('GEMINI_API_KEY is missing. Add it to Streamlit Secrets or environment variables.')
    from google import genai
    client=genai.Client(api_key=API_KEY)
    response=client.models.generate_content(
        model='gemini-2.5-flash',
        contents=generation_prompt(level,previous),
        config={'system_instruction':SYSTEM_PROMPT,'response_mime_type':'application/json','temperature':0.9},
    )
    raw=json.loads(response.text)
    return validate(raw,level)


def fallback(level: str, previous: list[str]) -> Problem:
    """Explicit offline sample mode; NOT claimed to be AI-generated."""
    candidates=[]
    for a,b,c in TRIPLES:
        if level=='Foundation' and c>17: continue
        if level=='Advanced' and c<29: continue
        if level=='Standard' and not (13<=c<=37): continue
        unknown='c' if level=='Foundation' else ('a' if level=='Standard' else 'b')
        sig=f'{a}-{b}-{c}-{unknown}'
        if sig not in previous: candidates.append((a,b,c,unknown))
    if not candidates:
        candidates=[(a,b,c,'c' if level=='Foundation' else ('a' if level=='Standard' else 'b')) for a,b,c in TRIPLES if (level!='Foundation' or c<=17)]
    a,b,c,unknown=random.choice(candidates)
    return Problem(level,'Offline sample problem',a,b,c,unknown,'Identify the hypotenuse first, then use a² + b² = c².','Use the Pythagorean theorem to find the missing side.')

if 'history' not in st.session_state: st.session_state.history=[]
if 'problem' not in st.session_state: st.session_state.problem=None
if 'mode' not in st.session_state: st.session_state.mode=''

level=st.selectbox('Difficulty level',['Foundation','Standard','Advanced'],help='Foundation: missing hypotenuse; Standard/Advanced: missing leg')
mode=st.radio('Generation mode',['Gemini AI (required for assessed submission)','Offline sample (practice only)'],horizontal=False)
if st.button('✨ Generate New Problem',type='primary',use_container_width=True):
    try:
        previous=st.session_state.history
        if mode.startswith('Gemini'):
            # Retry up to three times if AI returns malformed or mathematically invalid JSON.
            errors=[]
            for attempt in range(3):
                try:
                    p=ai_generate(level,previous)
                    if p.signature in previous:
                        raise ValueError('Repeated triple and unknown.')
                    break
                except Exception as e:
                    errors.append(str(e))
            else:
                raise RuntimeError('AI generation failed verification after 3 attempts: '+errors[-1])
            st.session_state.mode='Gemini AI — independently verified'
        else:
            p=fallback(level,previous)
            st.session_state.mode='Offline sample — not AI generated'
        st.session_state.problem=p
        st.session_state.history=(previous+[p.signature])[-50:]
        st.session_state.show_hint=False
        st.session_state.show_solution=False
        st.session_state.feedback=''
    except Exception as e:
        st.error(f'Could not generate a problem: {e}')

p=st.session_state.problem
if p is not None:
    st.info(f'**Generation:** {st.session_state.mode}  |  **Problem level:** {p.level}')
    st.subheader('Your problem')
    st.write(question(p))
    st.latex('a^2+b^2=c^2')
    c1,c2=st.columns(2)
    with c1:
        if st.button('💡 Show Hint',use_container_width=True):
            st.session_state.show_hint=True
    with c2:
        if st.button('📖 Show Solution',use_container_width=True):
            st.session_state.show_solution=True
    if st.session_state.get('show_hint'):
        st.warning(p.hint)
    if st.session_state.get('show_solution'):
        for i,line in enumerate(steps(p),1): st.write(f'**Step {i}:** {line}')
    st.divider()
    st.subheader('Check your answer')
    with st.form('answer_form',clear_on_submit=False):
        answer=st.text_input('Missing side length (cm)',placeholder='Enter a number, e.g. 5')
        submitted=st.form_submit_button('Check Answer')
    if submitted:
        if not answer.strip():
            st.warning('Enter a numerical answer first.')
        elif is_correct(answer,p):
            st.success('Correct! Excellent work. 🎉')
        else:
            st.error('Not quite. Identify the hypotenuse and use a² + b² = c². Try again or open the hint.')
else:
    st.info('Select a difficulty and click Generate New Problem to start.')
st.caption('Mathematical answers and worked solutions are computed by Python, not trusted from the AI response. The displayed problem is generated from verified numerical fields.')
