# ShieldAI — AI-assisted Phishing & Scam Detector

A beginner-friendly BCA project prototype built with Python and Streamlit. It analyses pasted messages and URLs using explainable warning-sign rules.

## Features
- Message checks for urgency, credential requests, payment pressure, impersonation language, and suspicious formatting.
- URL checks for non-HTTPS links, URL shorteners, IP-address hosts, unusual subdomains, punycode, and other basic signals.
- Risk estimate from 0–100 with a plain-language explanation.
- Runs locally; no text or URL is sent to an external service.

## Run locally
1. Install Python 3.10 or newer.
2. Open a terminal in this project folder.
3. Create and activate a virtual environment (recommended).
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Start the app:
   ```bash
   streamlit run app.py
   ```

## Project structure
```text
ai_phishing_scam_detector/
├── app.py
├── detector.py
├── requirements.txt
└── README.md
```

## Important limitations
This is an educational heuristic prototype, not a production security product. The score is not a probability, the app does not visit URLs, and a low score does not mean a message or website is safe. Attackers can evade simple rules and legitimate messages can trigger false alarms. Do not enter real passwords, OTPs, banking details, or private messages.

## Suggested project-report sections
1. Abstract and problem statement
2. Objectives and scope
3. System requirements
4. Architecture and workflow
5. Detection rules and scoring method
6. Screenshots and test cases
7. Limitations, ethical considerations, and future scope
8. Conclusion and references

## Future improvements
- Add a properly licensed and documented dataset.
- Train a TF-IDF + Logistic Regression text classifier and evaluate it on a held-out test set.
- Report precision, recall, F1-score, and false-positive rate.
- Add trusted domain reputation checks with an API, with user consent.
