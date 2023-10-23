import os
import mysql.connector
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Read MySQL credentials from environment variables
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")

# Connect to MySQL server
cnx = mysql.connector.connect(user=db_user, password=db_password)

# Create the flashcards database
cursor = cnx.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS flashcards")
cursor.execute("USE flashcards")

# Create the flashcards table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS flashcards (
        id INT AUTO_INCREMENT PRIMARY KEY,
        deck VARCHAR(255),
        question VARCHAR(255),
        answer VARCHAR(255)
    )
""")

# Commit the changes and close the connection
cnx.commit()
cursor.close()
cnx.close()

# uncomment if you want to  Install required packages
#os.system("sudo apt install translate-shell")
#os.system("sudo apt install espeak-ng")
