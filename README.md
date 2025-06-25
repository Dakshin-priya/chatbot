
#  Chatbot Project

This is a simple chatbot project built using **Python** and **Streamlit**. It utilizes packages like `streamlit`, `openai`, `requests`, `beautifulsoup4`, `fuzzywuzzy`, and `torch`.

---

##  Features

- Interactive chatbot UI using Streamlit  
- Web scraping capability using BeautifulSoup  
- Text matching via fuzzy string logic  
- AI/ML support with Torch (for model loading, if needed)

---

## Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
````

### 2. Create virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

* On **Windows**:

  ```bash
  venv\Scripts\activate
  ```

* On **Linux/macOS**:

  ```bash
  source venv/bin/activate
  ```

### 4. Install required dependencies

#### If you're using OpenAI API:

```bash
pip install streamlit openai requests beautifulsoup4
```

#### For advanced string matching and ML:

```bash
pip install streamlit requests beautifulsoup4 fuzzywuzzy python-Levenshtein torch
```

>  Note: You may combine all the above into a single `requirements.txt` file for easier installation.

---

##  Running the Chatbot

```bash
streamlit run chatbot.py
```

The app will open in your default browser at `http://localhost:8501`.

---

##  Project Structure (Example)

```
chatbot/
├── chatbot.py
├── venv/
├── README.md
└── .gitignore
```
