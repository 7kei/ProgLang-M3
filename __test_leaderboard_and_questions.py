from Database import *

def main():
    database = Database()

    # Fill questions db
    database.insertIntoQuestions("What is 3+4?", "7")
    database.insertIntoQuestions("What is 5*2?", "10")
    database.insertIntoQuestions("What is 9-3?", "6")
    database.insertIntoQuestions("What is 8/2?", "4")
    database.insertIntoQuestions("What is 1+1?", "2")
    database.insertIntoQuestions("Color of an apple?", "red")
    database.insertIntoQuestions("Color of the sea?", "blue")
    database.insertIntoQuestions("Is orange a fruit?", "yes")

    # Template leaderboard

if __name__ == "__main__":
    main()