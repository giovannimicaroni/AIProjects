# 🌐 Simple AI Translator Using LangChain 🦜🔗 & Ollama 🦙

Welcome to a minimal AI-powered translation local web app built with [LangChain](https://python.langchain.com/) and [Ollama](https://ollama.com/)!  
This project was done as a hands-on exercise in using LangChain and Ollama.

---

## 🚀 Quick Start

1. **Clone the Repository**
    ```bash
    git clone https://github.com/giovannimicaroni/AIProjects.git
    cd Translator
    ```

2. **Set Up Your Environment**
    - Create and activate a virtual environment:
      ```bash
      python -m venv .venv
      source .venv/bin/activate
      ```
    - Install dependencies:
      ```bash
      pip install -r requirements.txt
      ```

3. **Configure Ollama**
    - Download and install [Ollama](https://ollama.com/).
    - Pull your desired model (e.g., mistral):
      ```bash
      ollama pull mistral
      ```
    - If Ollama is running on a remote server, set `OLLAMA_HOST` in your `.env` file.

4. **Set Up Environment Variables**
    - In the project folder, create a `.env` file:
      ```
      OLLAMA_HOST=(optional, e.g. http://192.168.1.100)
      INFERENCE_MODEL=mistral (change to your desired model)
      ```

5. **Run the Translator App**
    ```bash
    streamlit run app.py
    ```
    - Open your browser and go to [localhost:8000](http://localhost:8000) to use the translator.

---

## 📝 Features

- Translate text between multiple languages.
- Powered by LangChain and your chosen Ollama model.
- Simple Streamlit UI.

---

## 📦 Requirements

- Python 3.8+
- [Ollama](https://ollama.com/)
- [LangChain](https://python.langchain.com/)
- [Streamlit](https://streamlit.io/)

---

## ⚙️ Customization

- Change the translation model by editing `INFERENCE_MODEL` in your `.env` file.
- Point to a remote Ollama server by setting `OLLAMA_HOST`.

---

## 💡 Tips

- For best results, use a virtual environment.
- Make sure Ollama is running before starting the app.
- If you encounter issues, check your `.env` configuration and model availability.

---

## 📚 References

- [Ollama Documentation](https://ollama.com/)
- [LangChain Documentation](https://python.langchain.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)

---

> This project was made for practice purposes and the owner is not responsible for its further using.
