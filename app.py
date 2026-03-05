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
    examples = CORPORATE_EXAMPLES if style_choice == "Corporate Speak" else GENZ_EXAMPLES
    # We add a very strict instruction here
    prefix = (
        f"You are a professional linguistic style-transfer engine. "
        f"Translate the user's input into {style_choice}. "
        f"Respond ONLY with the translation. Do not include any introductory text."
    )
    
    example_prompt = PromptTemplate(
        input_variables=["input", "output"],
        template="Input: {input}\nTranslation: {output}"
    )
    
    prompt = FewShotPromptTemplate(
        examples=examples,
        example_prompt=example_prompt,
        prefix=prefix + "\n\nExamples:",
        # The suffix now explicitly demands the Input/Translation format
        suffix="\nInput: {text}\nTranslation:", 
        input_variables=["text"]
    )
    
    return prompt

def translate_text(text, style):
    llm = ChatGroq(
        model="llama-3.1-8b-instant", 
        temperature=0.0, # Keeps it strictly to the pattern 
        api_key=os.getenv("GROQ_API_KEY")
    )
    
    prompt_template = get_translator(style)
    final_prompt = prompt_template.format(text=text)
    
    # Get the raw translation from the model
    response = llm.invoke(final_prompt).content.strip()
    
    # Return as a list or a string with clear newlines
    return f"**Input:** {text}  \n**Output:** {response}"


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
            # Use markdown to respect the line breaks and bolding
            st.info(result) 
            
            # Show the "Why" (Resume value)
            with st.expander("See how the prompt was built"):
                st.code(get_translator(style).format(text=text_input))