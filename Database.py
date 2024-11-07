import sqlite3

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('database.db')
        print("Database connected!")
        self.cursor = self.conn.cursor()

        # Question Table schema:
        # question    : TEXT    -> the question text
        # answer      : TEXT    -> the question answer
        self.cursor.execute("CREATE TABLE IF NOT EXISTS questions (question TEXT, answer TEXT)")

        # Leaderboard Table schema:
        # player_name : TEXT    -> player name
        # kill_count  : INTEGER -> kill count in 1 stage
        # time_spent  : INTEGER -> time spent in seconds
        self.cursor.execute("CREATE TABLE IF NOT EXISTS leaderboard (player_name TEXT, kill_count INTEGER, time_spent INTEGER)")
        self.conn.commit()
        print("Database initialized!")
    
    def getQuestions(self):
        rows = self.cursor.execute("SELECT * FROM questions").fetchall()
        return rows
    
    def insertIntoQuestions(self, question: str, answer: str):
        currentQuestions = [i[0] for i in self.getQuestions()]
        if question in currentQuestions:
            return
        self.cursor.execute("INSERT INTO questions VALUES (?, ?)",
                            (str(question), str(answer)))
        self.conn.commit()
    
    def getLeaderboard(self):
        rows = self.cursor.execute("SELECT * FROM leaderboard").fetchall()
        return rows
    
    def insertIntoLeaderboard(self, name: str, killCount: int, timeSpent: int):
        self.cursor.execute("INSERT INTO leaderboard VALUES (?, ?, ?)",
                            (name, killCount, timeSpent))
        self.conn.commit()
    

