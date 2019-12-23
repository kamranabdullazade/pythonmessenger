import sqlite3
import datetime
import threading
import time

con = sqlite3.connect("database.db", check_same_thread=False)

cursor = con.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS messages (id,name,message,time)")
con.commit()

cursor.execute("INSERT INTO messages VALUES (?,?,?,?)",(1, "System", "Connect", datetime.datetime.now()))
con.commit()

user1 = "Test1"
passw1 = "v123"

user2 = "Test2"
passw2 = "s123"

user3 = "Test3"
passw3 = "s12"

user4 = "Test4"
passw4 = "k123"

my_username = input("Username: ")
passw = input("Password : ")


lock = threading.Lock()  #stackoverflow Thanks :D

if user1 == my_username and passw1 == passw or user2 == my_username and passw2 == passw or user3 == my_username and passw3 == passw or user4 == my_username and passw4 == passw:
    cursor.execute("INSERT INTO messages VALUES (?,?,?,?)", (2, my_username, "Sign in", datetime.datetime.now()))
    con.commit()

    class Message_app():
        def __init__(self):
            cursor.execute("SELECT id FROM messages")
            data2 = cursor.fetchall()
            self.num = data2[-1][0]


        def run(self):
            lock.acquire(True)

            while True:

                cursor.execute("SELECT id FROM messages")
                data2 = cursor.fetchall()
                self.num = data2[-1][0]
                self.num += 1


                message = input(my_username + " Message : ")

                cursor.execute("INSERT INTO messages VALUES (?,?,?,?)",(self.num, my_username, message, datetime.datetime.now()))
                con.commit()
                cursor.execute("SELECT * FROM messages")
                data = cursor.fetchall()
                print(data[-1][0],":",data[-1][1],":",data[-1][2],"---",data[-1][3])



        def check(self):
            cursor.execute("SELECT * FROM messages")
            data = cursor.fetchall()

            while True:
                lock.acquire(True)

                if self.num != data[-1][0]:
                    cursor.execute("SELECT * FROM messages")
                    data = cursor.fetchall()

                    print(data[-2][0],":",data[-2][1],":",data[-2][2],"---",data[-2][3])
                    print(data[-1][0], ":", data[-1][1], ":", data[-1][2], "---", data[-1][3])
                time.sleep(1)


        def go(self):
            t1 = threading.Thread(target=self.run)
            t2 = threading.Thread(target=self.check)
            t1.start()
            t2.start()


a = Message_app()
a.go()

