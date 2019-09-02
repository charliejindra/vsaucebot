import sys

import time
from METHODS_Grammar import containsBlackListed
spaceTest = open("testMaterial/blacklistTestMaterial.txt", 'r')

print("TRUE : contains a blacklisted term. FALSE : does not.")

for line, linePreTest in enumerate(spaceTest):     # make the bitstring the length of michel sayings, each bit corresponds to a line in michelSayings.txt
    print("{} : {}\n".format(linePreTest, containsBlackListed(linePreTest)))