#The function 'write' on lines 8-15 overwrites a text file with a string input
#The function 'log' on lines 17-24 append a string followed by a new line allowing for another log in the future
#The function 'read' on lines 26-33 returns the contents of a text file in string form. It should be noted that there have been problems reading files encrypted with unicode
#The function 'split' on lines 35-38 takes a string and converts it into an array where each line gets its own pointer
#The function 'lineMod' on lines 41-58 takes a file, a string and line number. The function converts the contents of the file into a string and rewrites the file with the line appended at the point specified by the line number
#The function 'obtain' on lines 61-88 is a WIP and this shall be filled in later. It is likely the code will be scraped and replaced with a more modular version so to be used across many future ventures.
#The function 'arrayLocate' on lines 91-97 takes a 2D array and a keyword. It will search the first column of the array for the matching keyword. It will then return the row.
#The function 'arrayUpdate' on lines 101-103 take a 2D array, a pointer on the y axis, and a value. It will then overwrite the value on the second column of that row
#The function 'describe' on lines 107-127 is a nice one. Originally designed to read a pre-prepared file dictionary it is now used to retrieve information using a reference system.
#The function 
#The function 

import os
import urllib.request
import urllib.parse
import re
import sys
	
def write(file, text):
	w = open(file, 'w')

	w.write(text)

	w.close

	return True

def log(file, text):
	w = open(file, 'a')
	
	w.write(text + "\n")

	w.close

	return True

def read(file):
	r = open(file, 'r')
	
	text = r.read()
	
	r.close()

	return text

def split(string):
	lines = string.split('\n')

	return lines

def lineMod(file, inputText, lineNum):
	fileData = read(file)
	fileData = split(fileData)

	lineFirstNumber = lineNum - 1
	lineLastNumber = lineNum
	lineLength = len(fileData) - 1
	lineFirst = fileData[0:lineFirstNumber]
	lineLast = fileData[lineLastNumber:lineLength]

	lineFirst = '\n'.join(lineFirst)
	lineLast = '\n'.join(lineLast)

	inputText = lineFirst + '\n' + inputText + '\n' + lineLast

	write(file, inputText)

	return True

def obtain(group, attribute, array):
    i = 0
    file = str(group) + ".txt"
    preSplit = describe(file, attribute)
    print(preSplit)
    equi = split(preSplit)
    arrayValue = retreive(array, attribute)
    arrayLength = len(arrayValue)+len(equi)
    Equipment = [""]*arrayLength
    while i < len(equi):
        value = equi[i]
        if value[0] == "a":
            value = input("Would you rather" + "\n" + value + "\n" + "> ")
        else:
            value = value
        ii = 1
        if arrayLength != 1:
            while ii < arrayLength:
                Equipment[ii-1] = arrayValue[ii]
            Equipment[arrayLength-1] = value
        else:
            Equipment[0] = value
        i = i + 1

    print(arrayValue)
    array = update(array, attribute, Equipment)
    print("Array: " + str(array))
    return array

def arrayLocate(array, keyword):
    i = 0
    while array[i][0] != keyword:
        i = i + 1

    value = str(array[i][1])
    return value

def arrayUpdate(array, pointer, value):
    array[pointer][1] = str(value)
    return array

def describe(file, keyword):
    i = 0
    array = split(read(file))
    identifyer = "[" + keyword + "]"
    while array[i] != identifyer:
        i = i + 1
    i = i + 1
    start = i
    original = start
    while array[i] != identifyer:
        i = i + 1
    i = i - 1
    finish = i
    while start <= finish:
        if start == original:
            definition = array[start]
        else:
            definition = definition + "\n" + array[start]
        start = start + 1

    return definition

lineMod('test', 'Hi', 3)
#	os.system("echo {} | espeak".format(x))

#Calling area
#main()
