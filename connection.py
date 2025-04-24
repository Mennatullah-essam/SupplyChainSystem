import sqlite3 
from icecream import ic as print 

def get_connection (db_name) :
    try : 
        return sqlite3.connect(db_name)
    except Exception as e : 
        print (f"exception1 {e}")
        raise
    
def create_table(connection):
    query = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        role TEXT NOT NULL,
        email TEXT UNIQUE
    )
    
    """
    try :
        with connection :
            connection.execute(query)
        print ("table created")
    except Exception as e:
        print (f"exception2 {e}")
        
def insert_users (connection , id: int, name :str , role:str , email: str)  :
    query =  "INSERT INTO users (id, name ,role , email) Values (? ,? ,? ,?)"
    try : 
        with connection:
            connection.execute(query, (id , name , role , email))
            print (f"User {name} was added")
    except Exception as e:
        print (f"exception3 {e}")

def fetch_users (connection, condition: str = None) -> list[tuple] :
    query = "SELECT * FROM users "
    if condition :
        query += f"WHERE {condition} "
    
    try :
        with connection :
            rows =   connection.execute(query).fetchall()
        return rows    
        
    except Exception as e :
        print (f"exception 4 {e} ")  

def delete_user (connection ,id: int)  :
    query = "DELETE FROM users WHERE id = ?"
    try: 
        with connection :
            connection.execute(query,(id,))
        print (f"user : {id} deleted. ")
    except Exception as e :
        print (f"exception 5 {e}")

def update_user (connection , id , email):
    query = "UPDATE users SET email = ? WHERE id = ? "
    try : 
        with connection :
            connection.execute(query,(email, id,))
        print ("user email updated")
    except Exception as e :
        print (f"exception 6 {e}") 

def insert_users (connection, users: list[tuple[ int, str, str,str]]) :
    query = "INSERT INTO users VALUES (id , name ,role , email )"
    try : 
        with connection :
            connection.executemany( query, users)
        print (f"{len(users)} users were added" )
    except Exception as e :
        print (f"exception 7 {e}" )
        

def main ():
    connection = get_connection ("database3.db")
    
    try:
        create_table(connection)
        start = input("Enter option add, search, update, delete, add many : ").lower()
        if start == "add":
            id = int(input("Enter user ID: "))
            name = input("Enter name: ")
            role = input("Enter role: ")
            email = input("Enter email: ")
            
            insert_users(connection, id, name, role , email)
        elif start == "search" :
            for user in fetch_users(connection):
                print(user)
        
        elif start == "delete" :
            id = int(input(f"enter id you want to delete . "))
            delete_user ( connection , id )
            
        elif start == "update" :
            id = int(input("Enter the id you want to update its email "))
            new_email= input("enter the new email. ")
            update_user(connection, id, new_email)
            
        elif start== "add many" :
            id = int(input("Enter user ID: "))
            new_email = input("Enter email: ")
            update_user(connection, id, new_email)
            
                
    except Exception as e:
        print (f"exception f {e}")    
        
    finally :
        connection.close()


    
    
if __name__ == "__main__":
    main()
