import random
import subprocess
import mysql.connector
import tty, termios, sys
from colorama import Fore, init
from getpass import getpass

init(autoreset=True)

def speak_question(question):
    subprocess.run(['espeak-ng', '-v', 'es', question])

def speak_answer(answer):
    subprocess.run(['espeak-ng', '-v', 'en-us', answer])

def get_random_question(cursor, deck):
    cursor.execute("SELECT COUNT(*) FROM flashcards WHERE deck = %s", (deck,))
    total_questions = cursor.fetchone()[0]
    cursor.execute("SELECT id, question, answer FROM flashcards WHERE deck = %s", (deck,))
    questions = cursor.fetchall()
    random.shuffle(questions)
    for question in questions:
        if question[0] not in asked_questions:
            asked_questions.append(question[0])
            return question, total_questions
    return None, total_questions

def ask_user():
    answer = input("Choose an option (delete/show answer/skip) [show answer]: ")
    return answer.lower() if answer else 'show answer'

def add_new_card(cursor, cnx, deck):
    answer = input("Enter the English answer: ")
    translation_output = subprocess.check_output(['trans', answer]).decode('utf-8')
    print(translation_output)
    question = input("Enter the question for the card: ")
    cursor.execute("INSERT INTO flashcards (question, answer, deck) VALUES (%s, %s, %s)", (question, answer, deck))
    cnx.commit()

def list_all_cards(cursor, deck):
    cursor.execute("SELECT question, answer FROM flashcards WHERE deck = %s ORDER BY RAND()", (deck,))
    cards = cursor.fetchall()
    for i, card in enumerate(cards, start=1):
        print(Fore.GREEN + f"{i}. Question: {card[0]}, Answer: {card[1]}")

def change_deck():
    return input("Enter the name of the deck you'd like to switch to: ")

def list_decks(cursor):
    cursor.execute("SELECT DISTINCT deck FROM flashcards")
    decks = cursor.fetchall()
    print("\nDecks")
    
    for index, deck in enumerate(decks):
        print(str(index + 1) + ") " + Fore.MAGENTA + deck[0])
    print("\n")

def start_quiz(deck):
    cnx = mysql.connector.connect(user='flashcards', password='flashcards', database='flashcards')
    cursor = cnx.cursor()

    # Fetch the total number of questions for the specified deck
    cursor.execute("SELECT COUNT(*) FROM flashcards WHERE deck = %s", (deck,))
    total_questions = cursor.fetchone()[0]

    current_question_number = 0

    while True:
        question, _ = get_random_question(cursor, deck)
        if question is None:
            print("No more questions in this deck.")
            break

        current_question_number += 1
        print(f"Question {current_question_number} of {total_questions}:\n")
        print(Fore.MAGENTA + question[1])
        print("\n")
        speak_question(question[1])

        user_choice = ask_user()
        if user_choice == "show answer":
            print(Fore.BLUE + f"\nAnswer: {question[2]}\n")
            speak_answer(question[2])
        elif user_choice == "delete":
            cursor.execute("DELETE FROM flashcards WHERE id = %s", (question[0],))
            cnx.commit()
            print("Question deleted from the database.\n")
        elif user_choice == "skip":
            continue

        another_question = input("Do you want to see another question? (Y/N) [Y]: ")
        if another_question.lower() != 'y' and another_question != '':
            break

    cursor.close()
    cnx.close()


def display_menu():
    print("\n"+Fore.YELLOW+ "Welcome to Linux CLI Flashcards")
    print(Fore.CYAN+ "1) Quiz me")
    print(Fore.GREEN+ "2) Add a new card")
    print(Fore.MAGENTA+ "3) List all cards")
    print(Fore.BLUE+ "4) Select a different deck")
    print(Fore.WHITE+ "5) List decks")
    print(Fore.RED+ "Q) Quit\n")    
    print("Choose an option: ", end="", flush=True)
    choice = get_single_keypress()
    print(choice)  # to echo back the choice after it's made
    return choice.lower()

def get_single_keypress():
    """Get a single key press from user, depending on the OS."""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
       tty.setraw(sys.stdin.fileno())
       ch = sys.stdin.read(1)
    finally:
       termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

if __name__ == "__main__":
    asked_questions = []
    deck = 'spanish'
    while True:
        choice = display_menu()
        
        if choice == 'q':
            break
        elif choice == '1':
            start_quiz(deck)
        elif choice == '2':
            cnx = mysql.connector.connect(user='flashcards', password='flashcards', database='flashcards')
            cursor = cnx.cursor()
            add_new_card(cursor, cnx, deck)
            cursor.close()
            cnx.close()
        elif choice == '3':
            cnx = mysql.connector.connect(user='flashcards', password='flashcards', database='flashcards')
            cursor = cnx.cursor()
            list_all_cards(cursor, deck)
            cursor.close()
            cnx.close()
        elif choice == '4':
            deck = change_deck()
        elif choice == '5':
            cnx = mysql.connector.connect(user='flashcards', password='flashcards', database='flashcards')
            cursor = cnx.cursor()
            list_decks(cursor)
            cursor.close()
            cnx.close()
