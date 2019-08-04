import constants
import time

#spaces out the trend if it was a hashtag.
def spaceOut(oldString): # takes string as input, returns string with spaces inserted at every capital letter
    pos = 0
    newString = ''
    constants.lastCapFlag = False # if a space has been placed bc of the lastCapFromAcronym, then this is true.
    while pos < len(oldString) - 1: # len - 1 so you don't go one index over when doing pos + 1
        newString = newString + oldString[pos]  # add letter from old to new
        getSpaceData(pos, oldString) # get the data for this giant if statement
        try:
            if not(constants.lastCapFlag) and ((constants.nextLetterIsCapital and not(constants.at0thPosition or constants.onASpace or constants.inAcronym)) or constants.atEndOfAcronym or constants.lastCapFromAcronym):
                # if the next letter is capital
                # and not at the 0th position (so we dont have a space at the beginning)
                # and we're not at a space (so we dont have double spaces)
                # and 2 characters from now we dont have an uppercase (to check if we're in the middle of an acronym or something thats all caps)
                # OR (in a new branch) if this character and the last one were capital, and the next one is lowercase (end of an acronym)
                # OR (in a new branch) if this character is capital but every character after isnt
                #print('put a space!')
                newString = newString + ' '    # add space to new string
                if constants.lastCapFromAcronym: #if this is entered then no more spaces can be put for acronyms for the string
                    constants.lastCapFlag = True
        except:   # when it gets to end of string it goes here, this is probably sloppy as hell
            time.sleep(0)

        pos = pos + 1
    return newString

#part that idk wtf i was thinking
#((not oldString[pos+2].isupper()) or oldString[pos].islower())

#sets various global flags pertaining to an index of the spaced out word for the spaceOut function.
def getSpaceData(pos, old):
    constants.nextLetterIsCapital = True if (old[pos + 1].isupper()) else False
    constants.at0thPosition = True if (pos == 0) else False
    constants.onASpace = True if (old[pos] == ' ') else False
    constants.inAcronym = True if (old[pos: pos + 2].isupper() and (not ' ' in old[pos:pos+2])) else False
    constants.atEndOfAcronym = True if (old[pos-1:pos+1].isupper() and (not ' ' in old[pos-1:pos+1]) and old[pos+1].islower()) else False
    constants.lastCapFromAcronym = True if (old[pos+1].isupper() and constants.inAcronym and old[pos+2:len(old)].islower()) else False

def containsBlackListed(trend):
    trend = trend.lower()
    try:
        with open('blackListedWords.txt', 'r', encoding="utf8") as michelSayings:
            for line in michelSayings:
                if (line in trend):
                    return True
    except:
        with open('blackListedWords.txt', 'r') as michelSayings:
            for line in michelSayings:
                if (line in trend):
                    return True
    return False