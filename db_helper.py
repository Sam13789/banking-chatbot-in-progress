import mysql.connector

class DatabaseHelper:
    def __init__(self, host, user, password, database):
        self.db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="bank_chatbot_db"
        )
        self.cursor = self.db_connection.cursor()

    def check_balance(self, user_id):
        try:
            query = "SELECT balance FROM accounts WHERE user_id = %s"
            self.cursor.execute(query, (user_id,))
            balance = self.cursor.fetchone()[0]
            return balance
        except Exception as e:
            print("Error fetching balance:", e)
            return None

    def transfer_funds(self, sender_id, receiver_id, amount):
        try:
            # Check sender's balance
            sender_balance = self.check_balance(sender_id)
            if sender_balance < amount:
                return "Insufficient funds"
            
            # Update sender's balance
            query = "UPDATE accounts SET balance = balance - %s WHERE user_id = %s"
            self.cursor.execute(query, (amount, sender_id))

            # Update receiver's balance
            query = "UPDATE accounts SET balance = balance + %s WHERE user_id = %s"
            self.cursor.execute(query, (amount, receiver_id))

            # Insert transaction record
            query = "INSERT INTO transactions (sender_account_id, receiver_account_id, amount, transaction_type) VALUES (%s, %s, %s, 'transfer')"
            self.cursor.execute(query, (sender_id, receiver_id, amount))

            self.db_connection.commit()
            return "Transfer successful"
        except Exception as e:
            print("Error transferring funds:", e)
            self.db_connection.rollback()
            return "Error transferring funds"

    def deposit_funds(self, user_id, amount):
        try:
            query = "UPDATE accounts SET balance = balance + %s WHERE user_id = %s"
            self.cursor.execute(query, (amount, user_id))

            # Insert transaction record
            query = "INSERT INTO transactions (sender_account_id, amount, transaction_type) VALUES (%s, %s, 'deposit')"
            self.cursor.execute(query, (user_id, amount))

            self.db_connection.commit()
            return "Deposit successful"
        except Exception as e:
            print("Error depositing funds:", e)
            self.db_connection.rollback()
            return "Error depositing funds"

    def withdraw_funds(self, user_id, amount):
        try:
            # Check user's balance
            user_balance = self.check_balance(user_id)
            if user_balance < amount:
                return "Insufficient funds"

            query = "UPDATE accounts SET balance = balance - %s WHERE user_id = %s"
            self.cursor.execute(query, (amount, user_id))

            # Insert transaction record
            query = "INSERT INTO transactions (sender_account_id, amount, transaction_type) VALUES (%s, %s, 'withdrawal')"
            self.cursor.execute(query, (user_id, amount))

            self.db_connection.commit()
            return "Withdrawal successful"
        except Exception as e:
            print("Error withdrawing funds:", e)
            self.db_connection.rollback()
            return "Error withdrawing funds"

    def get_transaction_history(self, user_id):
        try:
            query = "SELECT * FROM transactions WHERE sender_account_id = %s OR receiver_account_id = %s"
            self.cursor.execute(query, (user_id, user_id))
            transactions = self.cursor.fetchall()
            return transactions
        except Exception as e:
            print("Error fetching transaction history:", e)
            return None

    # Add more functions for additional functionalities (e.g., update_account_info, set_alerts, etc.)

