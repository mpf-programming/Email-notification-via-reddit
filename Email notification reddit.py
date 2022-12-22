import praw
from datetime import datetime
import smtplib
import os

#Daten für Zugriff auf API
r = praw.Reddit(client_id = "",
                     client_secret = 
                     username = 
                     password = 
                     user_agent = "notifications")
# Welcher User soll "getrackt" werden
user = r.redditor("thisisbillgates")
comments = user.comments
comments_list = []
for comment in comments.new(limit=5):
    #print(dir(comment))
    sub = comment.subreddit
    comment_body = comment.body.split("\n")
    unix_time = comment.created_utc
    upvotes = comment.score
    comments_list += ["Subreddit: " + str(sub) + " ---- Comment: " + str(comment_body) + " ---- Date: " + str(datetime.fromtimestamp(unix_time))+ " ---- Score: " +str(upvotes) +"\n"]   
"""
# Einmalige Ausführung: Eine Datei kommentare.txt wird mit den Kommentaren von Reddit erstellt   
datei = open("kommentare.txt", "w")
datei.writelines(comments_list)
datei.close()
"""
print(comments_list)
print(str(comments_list).split("\n"))



datei = open("kommentare.txt", "r")
dateiinhalt = datei.readlines()


if dateiinhalt == comments_list:
    print(f"Kein neues Kommentar von {user} geschrieben seit der letzten Ausführung des Skripts")
else:
    #aktualisiere die Textdatei mit den aktuellsten Kommentaren
    datei = open("kommentare.txt", "w")
    datei.writelines(comments_list)
    datei.close()
    #Sende eine E-Mail mit den fünf neuesten Kommentaren: https://www.youtube.com/watch?v=PRiluD-qHFA
    user_gmail = "gmailaccount"
    password_gmail = ""
    mail_text = comments_list
    subject = f"Neues Reddit-Kommentar von {user}"

    MAIL_FROM = "gmailaccount"
    RCPT_TO = "youremail"
    DATA = f"From: {user_gmail}\nTo:{RCPT_TO}\nSubject:{subject}\n\n{mail_text}"
    #Vermeidet Fehler bei Umwandlung von UTF8 zu ASCII falls komische Zeichen in den Kommentaren auftauchen https://stackoverflow.com/questions/40810431/ascii-encoding-error-during-sending-a-mail
    DATA_ASCII_CONFORM = DATA.encode("ascii", errors="ignore")
    #smtp-Server Instanz erstellen
    server = smtplib.SMTP("smtp.gmail.com:587")
    server.starttls()
    server.login(user_gmail, password_gmail)
    server.sendmail(MAIL_FROM, RCPT_TO, DATA_ASCII_CONFORM)
    server.quit()
    print("E-Mail sent")



print(dateiinhalt)
print(comments_list)

print(dateiinhalt == comments_list)

