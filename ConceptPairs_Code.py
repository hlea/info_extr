# -*- coding: utf-8 -*-
"""
Created on Mon Jul 24 18:17:44 2017

@author: bercheng
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Jul 17 13:46:26 2017

@author: bercheng

"""

# This program reads verbatim and outputs concept pairs that are adjusted for negation
# Input file has ID as column1, Verbatim as column2
# Output file writes ID as column1, Concept pairs as columns2-4, Verbatim as column5

import csv
import spacy
import time

nlp = spacy.load('en')

# Establish Parameters - customize your desired outputs here
depList = ['nsubj', 'pobj', 'amod', 'nsubj', 'dobj', 'advmod', 'aux', 'auxpass']
priorNegsList = ['not', 'no', 'never']
postNegsList = ["n't"]
allNegsList = priorNegsList + postNegsList

# Functions -----------------------------

# i.e., "not good" --> "not_good"
def priorNegJoin(negConcept, postConcept):
    if negConcept in priorNegsList:
        return(negConcept + "_" + postConcept)        
    else:
        return(postConcept)

# i.e. "do n't" --> "don't"
def postNegJoin(negConcept, priorConcept):
    if negConcept in postNegsList:
        return(priorConcept + negConcept)
    else:
        return(priorConcept)

def replaceUnderscore(conceptList):
    for i in range(len(conceptList)):
        conceptList[i][0] = conceptList[i][0].replace("_", " ")
        conceptList[i][2] = conceptList[i][2].replace("_", " ")
    return(conceptList)
    
          
# Main Function Starts Here -------------

t0 = time.time()

# Open CSV files
infile = open('ConceptPairs_Input.csv')
outfile = open('ConceptPairs_Output.csv', 'a')

# Read inputs into array, then close file
csvReader = csv.reader(infile)

tweets = []
for column1, column2 in csvReader:
    tweets.append([column1, column2])

infile.close()

t1 = time.time()

# Column headers for output file
outfile.write("ID, Concept1, Dependency, Concept2, Verbatim\n")

# Iterate through tweets
for i in range(len(tweets)):

    # Read in, parse raw tweets
    ID = tweets[i][0]
    verbatim = tweets[i][1].replace(",", "")
    parsedVerbatim = nlp(verbatim)
    
    # PART 1 - Dealing with Negation
    # Read concept pairs into array
    allCPs = []
    for token in parsedVerbatim:
        allCPs.append([token.orth_, token.dep_, token.head.orth_])
    
    # Join neg concepts (prior/post)
    for i in range(len(allCPs)):
        if allCPs[i][1] == 'neg':
            # Prior negation cases
            allCPs[i+1][0] = priorNegJoin(allCPs[i][0], allCPs[i+1][0])
            # Post negation cases
            allCPs[i-1][0] = postNegJoin(allCPs[i][0], allCPs[i-1][0])
    
    # PART 2 - Craft sentence after negation manipulation
    words = []
    for i in range(len(allCPs)):
        if allCPs[i][0] not in allNegsList:
            words.append(allCPs[i][0])
    
    sentence = " ".join(words)
    
    # PART 3 - Get desired concept pairs, replacing underscores with spaces
    # Underscores originally in place for spacy to read negations together correctly
    finalCPs = []
    for token in nlp(sentence):
        finalCPs.append([token.orth_, token.dep_, token.head.orth_])
    
    finalCPs = replaceUnderscore(finalCPs)
    
    # Write relevant concept pairs onto CSV output file
    for i in range(len(finalCPs)):
        if finalCPs[i][1] in depList:
            outfile.write(ID + "," + finalCPs[i][0] + "," + finalCPs[i][1] + "," + finalCPs[i][2] + "," + verbatim + "\n")
    
t2 = time.time()

# Close outfile
outfile.close()

# Print time records
print("Done!")
print("Start time is: ", t0)
print("Time spent reading data is: ", (t1-t0) / 60)
print("Time spent processing tweets into concept pairs is: ", (t2-t1) / 60)