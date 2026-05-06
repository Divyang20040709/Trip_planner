# 💊 MediScan AI: Prescription Analysis Assistant

MediScan AI is a powerful, user-friendly Streamlit application designed to help users understand doctor prescriptions. By utilizing the cutting-edge **Google Gemini 3 Flash** multimodal AI, the app extracts and explains medical information from uploaded prescription images.

## 🚀 Features

- **OCR-Based Medicine Extraction**: Automatically identifies medicine names from handwritten or printed prescriptions.
- **Detailed Insights**: Provides clear explanations for each medicine, including:
  - **Uses**: What the medication is for.
  - **Side Effects**: Common reactions to watch out for.
  - **Dosage**: Recommended frequency (if visible).
  - **Warnings**: Important safety information.
- **Premium UI/UX**:
  - Modern, responsive interface with a medical-themed design.
  - Live image previews of uploaded documents.
  - Interactive status trackers and collapsible analysis results.
  - Sidebar for easy instructions and safety disclaimers.
- **Secure Configuration**: Uses environment variables (`.env`) to protect API keys.

## 🛠️ Technology Stack

- **Frontend**: [Streamlit](https://streamlit.io/)
- **AI Engine**: [Google Gemini 3 Flash Preview](https://deepmind.google/technologies/gemini/)
- **Programming Language**: Python 3.x
- **Key Libraries**: 
  - `google-genai`: For AI model interaction.
  - `Pillow`: For image processing and previews.
  - `python-dotenv`: For secure environment variable management.

## 📋 Installation & Setup

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd prescription_reader
   ```

2. **Install Dependencies**:
   ```bash
   pip install streamlit google-genai pillow python-dotenv
   ```

3. **Configure API Key**:
   Create a `.env` file in the root directory and add your Gemini API key:
   ```env
   GEMINI_API_KEY=your_actual_api_key_here
   ```

4. **Git Ignore**:
   Ensure your `.gitignore` includes the `.env` file to prevent leaking your API key.

## 🏃 How to Run

Launch the application using Streamlit:
```bash
streamlit run prescription_reader.py
```

## ⚠️ Safety Disclaimer

**MediScan AI is for educational purposes only.** 
It is designed to help you understand your prescription, but it **cannot** provide medical diagnoses or replace professional medical advice. Always consult a qualified doctor or pharmacist before taking or changing any medication.

---
*Created with ❤️ to empower health literacy.*
