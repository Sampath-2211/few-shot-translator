import streamlit as st
import os
from langchain_groq import ChatGroq
from langchain_core.prompts import (
    PromptTemplate, 
    FewShotPromptTemplate, 
    ChatPromptTemplate
)
from styles import CORPORATE_EXAMPLES, GENZ_EXAMPLES
from dotenv import load_dotenv

# Load Environment
load_dotenv()

# --- LOGIC ---
def get_translator(style_choice):
    """
    Constructs a Few-Shot Prompt Template based on user selection.
    """
    examples = CORPORATE_EXAMPLES if style_choice == "Corporate Speak" else GENZ_EXAMPLES
    prefix = "You are a translator. Convert the user's input into corporate jargon." if style_choice == "Corporate Speak" else "You are a translator. Convert the user's input into Gen-Z slang."
    
    # 1. Define how each example should look
    example_prompt = PromptTemplate(
        input_variables=["input", "output"],
        template="Input: {input}\nTranslation: {output}"
    )
    
    # 2. Assemble the Few-Shot Prompt
    prompt = FewShotPromptTemplate(
        examples=examples,
        example_prompt=example_prompt,
        prefix=prefix + "\n\nExamples:",
        suffix="Input: {text}\nTranslation:",
        input_variables=["text"]
    )
    
    return prompt

def translate_text(text, style):
    llm = ChatGroq(
        model="llama3-8b-8192", 
        temperature=0.5,
        api_key=os.getenv("GROQ_API_KEY")
    )
    
    prompt_template = get_translator(style)
    # Format the prompt with the user's input
    final_prompt = prompt_template.format(text=text)
    
    return llm.invoke(final_prompt).content

# --- UI ---
st.set_page_config(page_title="Few-Shot Translator", layout="centered")

st.title("🎭 The Few-Shot Translator")
st.markdown("### Style Transfer using In-Context Learning")

col1, col2 = st.columns([1, 2])

with col1:
    style = st.radio("Choose Target Persona:", ["Corporate Speak", "Gen-Z Slang"])

with col2:
    text_input = st.text_input("Enter plain English:", placeholder="e.g., I am very tired.")

if st.button("Translate Style"):
    if text_input:
        with st.spinner("Applying style transfer..."):
            result = translate_text(text_input, style)
            st.success(result)
            
            # Show the "Why" (Resume value)
            with st.expander("See how the prompt was built"):
                st.code(get_translator(style).format(text=text_input))