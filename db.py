import sqlite3
import datetime



class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def add_user(self, user_id, signup):
        with self.connection:
            self.cursor.execute("INSERT INTO 'users' ('user_id', 'signup') VALUES (?, ?)", (user_id, signup,))

    def user_exists(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchall()
            return (bool(len(result)))
        
    def reg_date(self, user_id):
        with self.connection:
            print (str(self.cursor.execute("SELECT signup FROM users WHERE user_id = ?", (user_id,)).fetchone()).split("'"))
            return str(self.cursor.execute("SELECT signup FROM users WHERE user_id = ?", (user_id,)).fetchone()).split("'")[1]
    
    def bills(self, user_id):
        with self.connection:
            return str(self.cursor.execute("SELECT bills FROM users WHERE user_id = ?", (user_id,)).fetchone())[1:].split(",")[0]
        
    def set_admin(self, user_id):
        with self.connection:
            return self.cursor.execute("UPDATE users SET admin = 1 WHERE user_id = ?", (user_id,))
    
    def del_admin(self, user_id):
        with self.connection:
            return self.cursor.execute("UPDATE users SET admin = 0 WHERE user_id = ?", (user_id,))

    def admin_exists(self, user_id):
        with self.connection:
            result = str(self.cursor.execute("SELECT admin FROM users WHERE user_id = ?", (user_id,)).fetchall())[2:][:1]
            return (result)

    def add_product(self, amount, number):
        with self.connection:
            self.cursor.execute("INSERT INTO 'cards' ('amount','number') VALUES (?, ?)", (amount, number,))      

    def del_product(self, number):
        with self.connection:
            self.cursor.execute("DELETE FROM cards WHERE number = ?", (number,))

    def buy_history(self, user_id):
        with self.connection:
            answer = str(self.cursor.execute("SELECT orders FROM users WHERE user_id = ?", (user_id,)).fetchall()).split()
            return answer
    
    def new_buy(self, amount, user_id, product):
        with self.connection:
            date = datetime.date.today()
            number = str(self.cursor.execute("SELECT number FROM cards WHERE amount = ?", (amount,)).fetchone()).split("'")[1]
            self.cursor.execute("DELETE FROM cards WHERE number = ?", (number,))
            print(str(self.cursor.execute("SELECT orders FROM users WHERE user_id = ?", (user_id,)).fetchone()))
            if len(str(self.cursor.execute("SELECT orders FROM users WHERE user_id = ?", (user_id,)).fetchone())) > 7:
                old_description = str(self.cursor.execute("SELECT orders FROM users WHERE user_id = ?", (user_id,)).fetchone())[2:][:-3]
                description = f"{old_description}{date, amount, product}|"
                self.cursor.execute("UPDATE users SET orders = ? WHERE user_id = ?", (description, user_id))
                print('Старое описание', old_description)
                print('Новое описание', description)            
            else:
                description = f"{date, amount, product}|"
                self.cursor.execute("UPDATE users SET orders = ? WHERE user_id = ?", (description, user_id))
                print('Новое описание', description)

            buy_int = str(self.cursor.execute("SELECT bills FROM users WHERE user_id = ?", (user_id,)).fetchone()).split(",")[0][1:]
            new_int = int(buy_int)+1
            self.cursor.execute("UPDATE users SET bills = ? WHERE user_id = ?", (new_int, user_id))
            return number