# MAS Credit Scoring Simulation
This project is part of my Master's study assessment for the course "Enterprise Intelligent Agent". It explores a case within the context of multiple enterprises, focusing on collaboration between global financial companies such as banks, digital payment platforms, loan providers, insurance companies, and fintech providers to manage an integrated financial ecosystem.

In this ecosystem, these entities leverage technologies like AI, blockchain, and big data to optimize processes including risk analysis, transaction management, and financial service personalization. With a many-to-many relationship, they enable real-time data exchange for more accurate credit scoring, enhanced transaction transparency through blockchain, and the development of customer-driven services powered by AI-driven analytics. The result is a smart financial ecosystem that is more efficient, inclusive, and capable of driving sustainable digital economic growth.

For this project, I focused on simulating a simplified credit scoring model based on income and transaction data using basic calculations. The algorithm used aims to calculate a credit score by considering two main factors: transactions and income. 

- **Transaction Score** is calculated based on the frequency, type, and value of transactions made by the customer. The more frequent and valuable the transactions, the higher the transaction score.  
- **Income Score** is calculated based on the customer's income, with higher income resulting in a higher score.

These two scores are then combined to produce an **overall credit score**, which is a weighted combination of the transaction and income scores. The weights control the relative contributions of transactions and income to the final credit score. The algorithm operates within a **multi-agent framework**, where agents representing the analysis system process and combine transaction and income data to generate a credit assessment.

This project utilizes the following technologies to build and run the credit scoring model:

- **Python:** Used for implementing the credit scoring algorithm and data processing.
- **Streamlit:** Used for building the interactive web application and user interface.
- **SQLite:** Used for storing and managing transaction and income data.

## How to Run Locally
1. Ensure you have Python 3.7 or higher installed.
2. Install the required libraries by running `pip install requirements.txt`.
3. Run the application using Streamlit `python -m streamlit run main.py`. This will open a new browser window with the application.
