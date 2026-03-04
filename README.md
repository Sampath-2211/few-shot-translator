# The Few-Shot Translator 🎭

**Status:** Active | **Tech:** LangChain, Few-Shot Prompting, Groq

> "The best way to control an LLM isn't to tell it what to do, but to show it."

## 🧠 The Problem
Standard LLMs often fail to capture specific **tones** or **brand voices** when simply instructed. Asking a model to "sound corporate" often results in generic, cheesy output.

## 💡 The Solution: Few-Shot Prompting
Instead of zero-shot instructions, this application feeds the model **5 distinct examples** of the desired input-output pairing *before* processing the user's request. This technique, known as **In-Context Learning**, drastically improves style adherence without fine-tuning.

### Capabilities
| Input (English) | Style: Corporate 👔 | Style: Gen-Z 💀 |
| :--- | :--- | :--- |
| "I made a mistake" | "A suboptimal outcome was observed." | "Big L." |
| "I agree" | "We are aligned on this initiative." | "Bet." |

## 🛠️ Installation

1. **Clone & Install**
   ```bash
   git clone <repo_url>
   cd few-shot-translator
   pip install -r requirements.txt
   ```

Configure Credentials  
Create a `.env` file in the root directory:

```
GROQ_API_KEY=gsk_your_api_key_here
```

Run the App

```bash
streamlit run app.py
```