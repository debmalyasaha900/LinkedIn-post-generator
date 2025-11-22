# 🔗 LinkedIn Post Generator  
AI-powered tool to generate high-quality LinkedIn posts inspired by top influencers.

[![Streamlit App](https://img.shields.io/badge/Launch%20App-Streamlit-brightgreen)](https://YOUR-APP-LINK-HERE)
![Python](https://img.shields.io/badge/Python-3.10-blue)
![MongoDB](https://img.shields.io/badge/Database-MongoDB-green)
![Streamlit](https://img.shields.io/badge/Framework-Streamlit-red)
![Llama4](https://img.shields.io/badge/Model-Llama4-purple)

---

## 🚀 Live Demo  
🔗 **App Link:** [https://YOUR-APP-LINK-HERE](https://linkedin-post-generator-fkj76vlcfhnhku2fdzftbc.streamlit.app/)

---

## 📌 Project Overview  
The **LinkedIn Post Generator** is an AI-powered Streamlit application that creates personalized LinkedIn posts based on:

- Influencer writing styles  
- Topic/Tag  
- Language (English / Hinglish)  
- Post length (Short / Medium / Long)

The app uses a **few-shot prompt system**, pulling examples from MongoDB and generating new posts using **Llama 4 via Groq API**.

Designed with polished UI, dark mode theme, and UX improvements — ideal for portfolio and resume projects.

---

## ✨ Features  

### 🔥 AI Generation
- Generates LinkedIn posts with influencer-specific tone  
- Supports English & Hinglish  
- Length control: short, medium, long  

### 🧠 Few-Shot Learning (MongoDB-powered)
- Pulls real examples from database  
- Auto-fallback logic if no matching posts found  
- Influencer-wise tag filtering  

### 🎨 Polished Streamlit UI  
- Full dark mode  
- Disabled dropdown typing (no text cursor)  
- Rate limiter to prevent spam  
- Copy-to-clipboard button  
- Success message and smooth UX  

### ⚙️ Admin / Data Support  
- Scripts to add influencers  
- Scripts to import processed posts  
- Fully modular codebase  

---

## 🏗️ Tech Stack  

| Component | Technology |
|----------|------------|
| Frontend | Streamlit |
| Backend | Python |
| Database | MongoDB Atlas |
| AI Model | Llama 4 (via Groq API) |
| Deployment | Streamlit Cloud |
| Logic | Few-shot prompting |

---
