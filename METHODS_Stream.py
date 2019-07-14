import random

#function for sending email
def send_email(subject, msg, Log):
    try:
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()

        passW = open("dietMtnDew.txt", 'r')
        #print("opened password file")
        michelPass = passW.readline()
        #print("read password")
        passW.close()
        #print("closed password file")

        server.login("michelvsace@gmail.com", michelPass)

        print("got thru the email opening")

        try:
            print('message abttta be stored')
            message = 'Subject: {}\n\n{}'.format(subject, msg)
            print('message stored man')
            server.sendmail("michelvsace@gmail.com", "charlessjindra@gmail.com", message)
        except:
            print('didnt work :(')
            message = 'Subject: {}\n\n{}'.format(subject, "Copying tweet failed.")
            server.sendmail("michelvsace@gmail.com", "charlessjindra@gmail.com", message)
        server.quit()
        print("Success: Email sent!")
    except:
        print("Email failed to send.")

#function to make message out of thing
def makeStatus(term, Log):
    isPlural = False
    if term.endswith('s') :
        isPlural = True

    fp = open("michelSayings.txt", 'r') # open michelSayings.txt in plaintext

    lineNo = random.randint(0, 90) # pick random line number from michelSayings
    print("Line from michelSayings: " + str(lineNo))

    j = 0
    while j != lineNo:
        line = fp.readline()
        j = j + 1
    #print("got through for")
    sayingUse = fp.readline() # set sayingUse to that line
    sayingUse = sayingUse.decode('utf-8')
    try:
        Log.write("Term: " + term+ "\n")
    except:
        Log.write("###ERROR: trend not able to be recorded for unknown reason\n")

    sayingUse = sayingUse.replace('+', term)
    sayingUse = sayingUse.replace('$', term + "'s")
    termPlural = term + "s"
    #print(useTrendPlural)
    if isPlural:
        #print("it's plural!")
        sayingUse = sayingUse.replace('@', "are")     #set of things to replace if the word is plural
        sayingUse = sayingUse.replace('[', "")
        sayingUse = sayingUse.replace(']', "have")
        sayingUse = sayingUse.replace('=', "do")
        sayingUse = sayingUse.replace('#', term)
        sayingUse = sayingUse.replace('^', "don't")
        sayingUse = sayingUse.replace('~', "")
    else:
        sayingUse = sayingUse.replace('@', "is")      #set of things to replace if the word is singular
        sayingUse = sayingUse.replace('[', "a")
        sayingUse = sayingUse.replace(']', "has")
        sayingUse = sayingUse.replace('=', "does")
        sayingUse = sayingUse.replace('#', termPlural)
        sayingUse = sayingUse.replace('^', "doesn't")
        sayingUse = sayingUse.replace('~', "s")
    #print(sayingUse)
    fp.close()

    #print('got here')
    message = sayingUse

    #print(message)
    try:
        Log.write(message + "\n")
    except:
        Log.write("###ERROR: message not able to be recorded for unknown reason\n")
    return message
    #print("updated status")
    #exeLog.write("updated status"  + "\n\n")