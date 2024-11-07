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
    database.insertIntoLeaderboard("Test_Keian1", 10, 5)
    database.insertIntoLeaderboard("Test_Keian2", 11, 4)
    database.insertIntoLeaderboard("Test_Keian3", 12, 3)
    database.insertIntoLeaderboard("Test_Keian4", 13, 2)

if __name__ == "__main__":
    main()