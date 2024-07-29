# AI-Email-Automation

## Overview
This project automates the process of drafting email responses by leveraging historical email data and FAQs. Using Python and the RelevanceAI platform, the application reads unread emails, generates responses based on past interactions, and drafts them in Gmail.

## Prerequisites
1. Python 3.10.0
2. A Gmail account
3. OpenAI API key
4. RelevanceAI account (100 free credits per day)

## Setup Instructions
### 1. Environment Setup
1. Clone the repository:
    ```
    git clone <repository_url>
    cd <repository_name>
    ```

2. Create a virtual environment:
    ```
    python -m venv env
    source env/bin/activate  # On Windows use `env\Scripts\activate`
    ```

3. Install dependencies:

    ```
    pip install -r requirements.txt
    ```
4. Configure environment variables:

    Create a .env file in the root directory and add your OpenAI API key:

    ```
    OPENAI_API_KEY=<your_openai_api_key>
    ```

### 2. Prepare Email Data
1. Download emails as mbox files from Gmail.

2. Convert mbox to CSV:
    ```
    python mbox_to_csv.py
    ```
    This will generate an intermediate CSV file.

3. Clean the email data:
    ```
    python email_cleaning.py
    ```
    This will generate `email_pairs.csv`.

### 3. Generate FAQs
```
python extract_faq.py
```
This will generate `faq.csv`.
### 4. Setup RelevanceAI
1. Create a RelevanceAI account: You get 100 free credits per day.

2. Create Tables:

    Upload `email_pairs.csv`. Optimize for the `prospect_email` field.

    Upload `faq.csv`. Optimize for both `answer` and `question` fields.

3. Create a New Tool:

4. Add both knowledge bases (email_pairs and faq) in the knowledge section.
5. Add a text input section named client_email in the user inputs section.
6. Add an LLM section with your chosen LLM provider (e.g., OpenAI GPT-3.5). Use the following prompt:
    ```
    You are the email inbox manager for Zubair Atha - an AI developer and Photographer; Your goal is to help draft email response for Zubair that mimics the past reply:

    Rule: Whenever you have to reply with a link only mention the link and not the hyperlink.

    PAST EXAMPLE:

    """ 
    {{
    knowledge.email_pairs_csv
    }}
    """

    KNOWLEDGE:

    """
    {{
    knowledge.faq_csv
    }}
    """

    ===

    New email to reply:

    NEW PROSPECT EMAIL THREAD: 
    {{
    client_email
    }}

    ===

    GENERATE RESPONSE:
    ```
7. Get the API Endpoint under the `Use>API` tab


### 5. Configure Gmail
1. Enable IMAP: Follow this [YouTube video](https://youtu.be/l-3BSCrAiXY?si=Rd_m7nAZPPeeD6lA) for instructions.
2. Add IMAP Password to .env file
    ```
    EMAIL_PASSWORD=<your_email_imap_password>
    ```
### 6. Run the Application
1. Draft email replies:
Update `draft_replies.py` with your email address and the API key copied from RelevanceAI.
2. Run the script:
    ```
    python draft_replies.py
    ```
3. Your application will now check for unread emails from the past day using IMAP and generate replies using the RelevanceAI tool, drafting them in Gmail via SMTP.
