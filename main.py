from bs4 import BeautifulSoup
import re
import os
import sys

totalFrequencyList = dict()
totalLocationList = dict()

count = 0
for filename in os.listdir('pages'):
    file = open('pages/' + filename, 'r')
    soup = BeautifulSoup(file, 'html.parser')

    for script in soup(["script", "style"]):
        script.extract()

    soup = soup.find('div', {'id':'content'}) #the actual content is in the content tag
    soup = soup.find_all('p') # important content all in p tags
    text = ""
    for x in soup:
        text += x.get_text()

    text = text.lower() #sets everything to lowercase
    text = re.sub("\[.*\]", " ", text)  #removes all text looking like  [xx]
    text = re.sub("[!\"#$%&'()*+\,-.−–\—/:;<\=>?@[\]^_`{|}~“”…’]", " ", text) #removes all punctuation
    text = text.replace("\\", " ")

    tokens = text.split()

    frequencyTable = dict()
    locationTable = dict()
    index = 0
    for word in tokens:
        if word in locationTable:
            locationTable[word].append(index)
        else:
            locationTable[word] = [index]
        index += 1
        if word in frequencyTable:
            frequencyTable[word] += 1
        else:
            frequencyTable[word] = 1

    for key, value in frequencyTable.items():
        if key in totalFrequencyList:
            totalFrequencyList[key].append({filename: value})
        else:
            totalFrequencyList[key] = [{filename:value}]

    for key, value in locationTable.items():
        if key not in totalLocationList:
            totalLocationList[key] = []
        for entry in value:
            totalLocationList[key].append({filename: entry})

    count += 1
    print(str(count) + "/476")

f = open("frequencyList.txt", "w")
for key, value in totalFrequencyList.items():
    f.write(key + ": ")
    for entry in value:
        for listkey, listvalue in entry.items():
            f.write("(" + listkey + ": " + str(listvalue) +"), ")
    f.write("\n")
f.close()

f = open("locationList.txt", "w")
for key, value in totalLocationList.items():
    f.write(key + ": ")
    for entry in value:
        for listkey, listvalue in entry.items():
            f.write("(" + listkey + ": " + str(listvalue) +"), ")
    f.write("\n")
f.close()

f = open("uniqueTerms.txt", "w")
for key in totalFrequencyList:
    f.write(key + "\n")
f.close()

f = open("wordsThatOnlyOccurOnce.txt", "w")

# Some analysis
mostFrequentTermfile = ""
mostFrequentOccuranceFile = 0
numOfTermsThatOccurOnlyOnce = 0
mostFrequentWord = ""
mostFrequentWordOccurance = 0
for key, value in totalFrequencyList.items():
    entryOcc = len(value)
    termListValue = 0
    if entryOcc > mostFrequentOccuranceFile:
        mostFrequentTermFile = key
        mostFrequentOccuranceFile = entryOcc
    for entry in value:
        for listkey, listvalue in entry.items():
            termListValue += listvalue

    if termListValue is 1:
        f.write(key + "\n")
        numOfTermsThatOccurOnlyOnce += 1

    if termListValue > mostFrequentWordOccurance:
        mostFrequentWord = key
        mostFrequentWordOccurance = termListValue

f.close()
print(mostFrequentTermFile + " occurs in " + str(mostFrequentOccuranceFile) + " files")
print(mostFrequentWord + " occurs " + str(mostFrequentWordOccurance) + " times")
print(str(numOfTermsThatOccurOnlyOnce) + " terms only occur once")
