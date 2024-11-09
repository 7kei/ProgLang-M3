from Database import *

connection = Database()

def viewQuestions(database: Database):
    curQues = database.getQuestions()
    print("\nCurrent questions and answers:")
    for i in curQues:
        print(f"{i[0]}: {i[1]}")

def viewLeaderboard(database: Database):
    curLeaderboard = database.getLeaderboard()
    print("Current leaderboard:")
    sortByTime = sorted(curLeaderboard, key=lambda tup: tup[2], reverse=True)
    for i in sortByTime:
        print(f"Player name: {i[0]}\tKill count: {i[1]}\tTime spent: {i[2]}")

def insertQuestion(database: Database):
    viewQuestions()
    ques = input("\nQuestion to add: ")
    ans = input("Answer: ")
    database.insertIntoQuestions(ques, ans)

while True:
    print("1. View questions")
    print("2. Insert questions")
    print("3. View leaderboard")
    print("4. Exit")
    choice = input()
    if choice[0] == "1":
        viewQuestions(connection)
    elif choice[0] == "2":
        insertQuestion(connection)
    elif choice[0] == "3":
        viewLeaderboard(connection)
    elif choice[0] == "4":
        break