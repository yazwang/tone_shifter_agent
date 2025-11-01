# Tone_Shifter_Agent
> Developed by **Yazhi (Esther) Wang**, 2025 — a bilingual tone-adaptive chatbot for empathetic and compliant communication.

![Python](https://img.shields.io/badge/python-3.13-blue)
![OpenAI](https://img.shields.io/badge/API-OpenAI%20gpt--4o--mini-orange)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-active-success)

🧩 *Bridging empathy and precision — a tone-adaptive bilingual chatbot for compliant communication.*

A simple bilingual chatbot built with OpenAI API that shifts tone (neutral, empathetic, professional) in real time for cross-cultural communication.

## ✨ Features
- **Language Detection:** Automatically detects English or Chinese and replies in the same language.  
- **Tone Recognition:** Uses sentiment analysis to determine tone automatically.  
- **Finance Mode:** Generates compliant and empathetic financial communication.  
- **Graceful Fallback:** Works offline via local templates when API quota is exceeded.  
- **Evaluation Framework:** Includes `evaluate.py` to compare API vs local reliability, showing *~13% improvement* in tone consistency.  

## 🚀 How to Run

1. **Install dependencies**
   ···bash
   pip3 install -r requirements.txt

2. Run the chatbot:
python3 app.py

3. Type your message and choose a tone.

---

## 📚 Legacy Prototype

Before the tone-adaptive version, an early prototype focused on bilingual translation nuance and emotion-preserving prompts.  
That version (archived in `GenAI Works Hackathon repo`) explored **prompt-based tone transfer** between English and Chinese.  
This current project evolved from that idea into a **code-driven real-time system** using OpenAI API and sentiment analysis.
