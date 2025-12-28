# Customer Complaint Classifier Responder

Streamlit app that classifies customer complaints into predefined response categories using a Groq-hosted language model (`openai/gpt-oss-20b`). You enter a Groq API key, paste a complaint, and the app returns the matching response label.

## Requirements
- Python 3.9+
- See `requirements.txt`:
  - streamlit
  - groq

## Setup (Windows PowerShell)
```powershell
cd "c:\Users\wilke\Coding Projects\Customer Complaint Classifier Responder"
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Run
```powershell
cd "c:\Users\wilke\Coding Projects\Customer Complaint Classifier Responder"
.\.venv\Scripts\python.exe -m streamlit run cccrapp.py
```

## Usage
1) Get a Groq API key from https://console.groq.com/keys.  
2) Open the app, enter your key, and review the listed response categories.  
3) Paste a customer complaint and click **Classify Complaint**.  
4) The predicted response category is shown below the button.

## Response categories (ID -> Label)
- 0: Company believes complaint caused principally by actions of third party outside the control or direction of the company  
- 1: Company believes it acted appropriately as authorized by contract or law  
- 2: Company can't verify or dispute the facts in the complaint  
- 3: Company chooses not to provide a public response  
- 4: Company disputes the facts presented in the complaint  
- 5: Company has responded to the consumer and the CFPB and chooses not to provide a public response

## Notes
- Network access is required to call the Groq API.  
- The app uses deterministic settings (`temperature=0.0`) for stable classifications.  
- Errors initializing the client or classifying will be surfaced in the UI; verify your API key and connection if you see them.***
