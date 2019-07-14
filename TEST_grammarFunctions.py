import sys
sys.path.append('../')

import time
from grammarFunctions import spaceOut

spaceTest = open("testMaterial/spaceTestMaterial.txt", 'r')

for line, linePreTest in enumerate(spaceTest):     # make the bitstring the length of michel sayings, each bit corresponds to a line in michelSayings.txt
    linePostTest = spaceOut(linePreTest)
    print(linePreTest + linePostTest + "\n")