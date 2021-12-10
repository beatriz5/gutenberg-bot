import requests
import re
from collections import Counter
from nltk.corpus import stopwords
import csv
import random
import threading
import time

def bag_of_words():

    characters_to_remove = ".!()@,;:?*"

    ## Variables always needed for BoW
    tokens = Counter()
    STOP = stopwords.words("english")
    STOP.append('the')

    ## GET the target (url
    response = requests.get("https://www.gutenberg.org/files/3807/3807-0.txt", stream = True)

    ## if on windows must add:
    response.encoding = "utf-8"

    ## The book doesn't start until "*** START OF TH" and has copywrite after '*** END OF TH'
    start_flag = True
    start_counter = 0
    end_flag = False

    ## quick load and make bag of words
    for curline in response.iter_lines():
        # Append-adds at last
        if curline.strip(): # "" = False
            ## Check if we are at the start of poems
            if start_flag:
                #skip this line until this line is found
                if curline.startswith(b'*** START OF TH'):
                    start_flag = False
            else:
                ##We have stsrted the book
                if not curline.startswith(b'*** END OF TH'):
                    
                    ## we are officially looking at Poems!
                    for word in curline.lower().split():
                        pattern = "[" + characters_to_remove + "]"
                        w = re.sub(pattern, "", word.decode())
                    
                        if w not in STOP and w!="":
                            ## decode word because not in STOP words
                            tokens[w] +=1

                else:
                    break

    ## 5 most common words
    most_common_element = tokens.most_common(5)
    for key, value in tokens.most_common(5):
        print('%15s    %15d' % (key, value))


    ## csv with Bag of Words
    with open('words.csv', mode='w', encoding='utf-8', newline='') as wordsfile:
        writer = csv.writer(wordsfile, dialect = 'excel')
        writer.writerow(["word", "count"])

        for token, count in tokens.items():
            if count > 3:
                writer.writerow([token, count])
            

print("\n5 Most Common Words In A Book")
print("Book: The Different Forms of Flowers on Plants of the Same Species, by Charles Darwin\n")
print('%15s    %15s' % ("WORD", "OCCURENCES"))
threading.Thread(target=bag_of_words()).start()
