import time


def spaceOut(oldString): # takes string as input, returns string with spaces inserted at every capital letter
    pos = 0
    newString = ''
    while pos < len(oldString):
        newString = newString + oldString[pos]  # add letter from old to new

        try:
            if ((oldString[pos + 1].isupper()) and (pos != 0) and (oldString[pos] != ' ') and ((not oldString[pos+2].isupper()) or oldString[pos].islower())) and (not(oldString[pos-1].isupper() and oldString[pos].isupper() and oldString[pos+1].isupper())) or (oldString[pos-1].isupper() and oldString[pos].isupper() and oldString[pos+1].islower()):
            #if ((oldString[pos + 1].isupper()) and (pos != 0) and (oldString[pos] != ' ') and ((not oldString[pos+2].isupper()) or oldString[pos].islower())) and (not(oldString[pos-1].isupper() and oldString[pos].isupper() and oldString[pos+1].isupper()) or (not(oldString[pos+2:].isupper()))) or (oldString[pos-1].isupper() and oldString[pos].isupper() and oldString[pos+1].islower() and (not newString[len(newString)-1] != ' ') and (not oldString[pos].isupper())):

                #COMMENTED OUT ONE IS WIP, THE ONE RUNNING NOW IS FUNCTIONAL BUT TESTFOUR DOESNT WORK 6/9/2019
                # if the next letter is capital
                # and not at the 0th position (so we dont have a space at the beginning)
                # and we're not at a space (so we dont have double spaces)
                # and 2 characters from now we dont have an uppercase (to check if we're in the middle of an acronym or something thats all caps)
                # or the rest of the string is lowercase (if it is then the last letter of the acronym is likely a proper noun.)
                # OR (in a new branch) if this character and the last one were capital, and the next one is lowercase (end of an acronym)
                # or if the last thing we put was a space in newString and we dont wanna put another (for TESTFour, works for that rn but nothing else)
                newString = newString + ' '    # add space to new string
        except:   # when it gets to end of string it goes here, this is probably sloppy as hell
            time.sleep(0)

        pos = pos + 1
    return newString

spaceTest = open("spaceTestMaterial.txt", 'r')

for line, linePreTest in enumerate(spaceTest):     # make the bitstring the length of michel sayings, each bit corresponds to a line in michelSayings.txt
    linePostTest = spaceOut(linePreTest)
    print(linePreTest + linePostTest + "\n")