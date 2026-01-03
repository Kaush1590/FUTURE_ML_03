# Chatbot for Customer Support
**A customer support chatbot built using Dialogflow, Streamlit, SQLite, and Flask webhook.**

This project implements a virtual customer support assistant capable of answering user queries, assisting with common issues, and responding automatically 24/7 through a conversational interface.
The chatbot is designed to simulate real-world customer support interactions such as handling FAQs, guiding users, and managing fallback responses when queries are unclear.

**This project has been made over <a href="https://www.kaggle.com/datasets/thoughtvector/customer-support-on-twitter">Customer Support on Twitter</a> dataset.**

# Problem Statement
Modern businesses receives a large volume of customer queries that requires instant responses, such as order status, service availability and general support. Handling these requests manually can be time consuming, costly and inefficient.

The goal of this project is to design and implement a customer support chatbot that can operate 24/7, respond to user queries in real time, and simulate the behavior of chatbots used by platforms such as Amazon, Flipkart, and Zomato.

**The chatbot should be capable of:**
- Greeting users and initiating conversations
- Answering common customer questions using predefined intents
- Handling unrecognized or unclear queries with a smart fallback response
- Being tested and validated using the Dialogflow interface

# System Requirements
1. Operating System: Windows/ Linux/ MacOS
2. Python version: 3.9+
3. Internet Connection: Required for Dialogflow API access and webhook communication
4. Browser: Any modern browser for Dialogflow console and Streamlit UI
5. (Optional) Cloud Platform: Render

# Dependencies
## Standard Python Libraries:
1. <code>datetime</code>:- For handling timestamps in chat messages
2. <code>uuid</code>:- For generating unique session identifiers
3. <code>time</code>:- For generating unique session identifiers
4. <code>collections</code>:- For grouping and managing session labels
5. <code>sqlite3</code>:- For lightweight local database storage
6. <code>pathlib</code>:- For handling file system paths in a platform-independent way

## Third Party Libraries
1. <code>streamlit</code>:- For handling file system paths in a platform-independent way
2. <code>google-cloud-dialogflow</code>:- For integrating Dialogflow intent detection
3. <code>google-auth</code>:- For secure authentication with Google Cloud services
4. <code>flask</code>:- For creating a webhook to handle Dialogflow fulfillment
5. <code>requests</code>:- For making HTTP requests

## Deployment Dependencies
1. <code>gunicorn</code>:- Production-ready WSGI server for hosting the Flask webhook
2. <code>python-dotenv</code>:- For managing environment variables securely

# Features
1. Provides real-time responses to user queries using Dialogflow
2. Supports intent-based conversation flow for accurate answers
3. Includes a smart fallback mechanism for unrecognized inputs
4. Displays a friendly greeting message to initiate conversations
5. Offers quick-reply buttons for frequently asked questions
6. Automatically creates a new chat session for each conversation
7. Allows users to resume previous chat sessions
8. Supports auto-naming based on the first user message and renaming sessions
9. Stores complete chat history using SQLite
10. Preserves messages across browser refreshes and app restarts
11. Uses a Flask webhook to process Dialogflow fulfillment requests
12. Easily deployable to cloud platforms like Render

# Installation
**Follow the steps below to set up the Customer Support Chatbot locally.**
## 1. Clone the repository
```bash
git clone https://github.com/Kaush1590/FUTURE_ML_03.git
cd FUTURE_ML_03
```

## 2. Create and activate a virtual environment
### Linux / macOS
```bash
python -m venv <environment_name>
source venv/bin/activate
```
### Windows
```bash
python -m venv <environment_name>
venv\Scripts\activate
```
### Anaconda
```bash
conda create -n chatbot-env python=3.9 -y
conda activate chatbot-env
```
## 3. Install required dependencies
```bash
pip install -r requirements.txt
```
## 4. Configure Dialogflow credentials (optional)
- Create a Dialogflow ES agent in Google Cloud
- Download the service account JSON key
- Add it to Streamlit secrets <code>.streamlit/secrets.toml</code>
## 5. Run the Streamlit chatbot UI
```bash
cd app
streamlit run app.py
```
## 6. Run the Dialogflow webhook (optional)
```bash
cd webhook
python webhook.py
```

# Industry Impacts
1. **24/7 Customer Support Automation**:- Reduces dependency on human agents by handling common customer queries automatically, enabling businesses to provide continuous support without increased operational costs.
2. **Improved Customer Experience**:- Delivers instant responses and consistent information, reducing customer wait times and improving satisfaction across digital platforms.
3. **Operational Cost Reduction**:- Minimizes support overhead by automating repetitive queries, allowing customer service teams to focus on complex and high-value issues.
4. **Scalable and Deployable Solution**:- Demonstrates a scalable chatbot architecture that can be integrated into websites, mobile apps, or messaging platforms, making it suitable for startups and large enterprises alike.

# Acknowlegdement
1. Kaggle for providing dataset
2. Open-source Python community
