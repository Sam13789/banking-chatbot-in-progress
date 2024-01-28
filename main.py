from fastapi import FastAPI, HTTPException
from typing import Optional
import mysql.connector
import requests

app = FastAPI()

# Establish MySQL database connection
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="bank_chatbot_db"
)
db_cursor = db_connection.cursor()

# Wit.ai access token
WIT_AI_ACCESS_TOKEN = 'JNUDF2GYAQVXDWT7GCYGALHORJOZ5AVJ'

@app.get("/")
async def read_root():
    return {"message": "Welcome to the banking chatbot!"}

@app.get("/greet/")
async def greet_user():
    return {"message": "Hello! How can I assist you today?"}

@app.get("/login/")
async def login(username: str, password: str):
    # Validate user credentials from the database
    query = "SELECT * FROM users WHERE username = %s AND password = %s"
    db_cursor.execute(query, (username, password))
    user = db_cursor.fetchone()
    if user:
        return {"message": "Login successful! How can I help you?"}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")

@app.get("/balance/")
async def check_balance(account_number: str):
    # Retrieve account balance from the database
    query = "SELECT balance FROM accounts WHERE account_number = %s"
    db_cursor.execute(query, (account_number,))
    balance = db_cursor.fetchone()
    if balance:
        return {"balance": balance[0]}
    else:
        raise HTTPException(status_code=404, detail="Account not found")

@app.post("/transfer/")
async def transfer_funds(sender_account: str, recipient_account: str, amount: float):
    # Deduct funds from sender's account and add to recipient's account
    # Perform database operations to transfer funds
    return {"message": f"Transferred {amount} from {sender_account} to {recipient_account} successfully"}

@app.post("/deposit/")
async def deposit_funds(account_number: str, amount: float):
    # Add funds to the specified account
    # Perform database operations to deposit funds
    return {"message": f"Deposited {amount} into account {account_number} successfully"}

@app.post("/withdraw/")
async def withdraw_funds(account_number: str, amount: float):
    # Deduct funds from the specified account
    # Perform database operations to withdraw funds
    return {"message": f"Withdrew {amount} from account {account_number} successfully"}

@app.get("/transactions/")
async def view_transactions(account_number: str, start_date: Optional[str] = None, end_date: Optional[str] = None):
    # Retrieve transaction history for the specified account within the date range
    # Perform database operations to fetch transaction history
    return {"message": "Transaction history fetched successfully"}

@app.get("/process-text/")
async def process_text(text: str):
    # Pass user input to Wit.ai for analysis
    wit_response = requests.get(
        "https://api.wit.ai/message",
        headers={"Authorization": f"Bearer {WIT_AI_ACCESS_TOKEN}"},
        params={"q": text}
    ).json()

    # Extract intent and entities from Wit.ai response
    intent = wit_response['intents'][0]['name']
    entities = wit_response['entities']

    # Perform actions based on intent and entities
    # Add your logic here based on the recognized intent and entities

    return {"intent": intent, "entities": entities}
