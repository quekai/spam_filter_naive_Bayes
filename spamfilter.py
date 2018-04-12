import nltk
from codecs import open
import os
import  re
from collections import defaultdict
import math
from nltk import NaiveBayesClassifier


def textParser(text):
    reg = re.compile(r'[^a-zA-Z]|\d')
    words = reg.split(text)
    for i in \
            [';', ':', ',', '.', '?', '!', '(', ')', ' ', '/', '@', \
             '+', '-', '=', '*', '“', '”', \
             '；', '：', '，', '。', '？', '！', '（', '）', '　', '、']:
        if i in words:
            words.remove(i)
    words = [word.lower() for word in words if len(word) > 0]
    str = ''
    for word in words:
        str +=word + ' '
    return str

def participles(text):
    pattern = r"""(?x)                   # set flag to allow verbose regexps 
              (?:[A-Z]\.)+           # abbreviations, e.g. U.S.A. 
              |\d+(?:\.\d+)?%?       # numbers, incl. currency and percentages 
              |\w+(?:[-']\w+)*       # words w/ optional internal hyphens/apostrophe 
              |\.\.\.                # ellipsis 
              |(?:[.,;"'?():-_`])    # special characters with meanings 
            """
    text = textParser(text)
    t=nltk.regexp_tokenize(text, pattern)
    return t



def gethams(hams_path):
    hams = (open(entry.path,'r','utf-8','ignore').read()
    for entry in os.scandir(hams_path)
    if entry.is_file()
    )
    return hams

def getspams(spams_path):
    spams = (open(entry.path,'r','utf-8','ignore').read()
        for entry in os.scandir(spams_path)
        if entry.is_file()
    )
    return spams

def getfeatures(hams,spams): # hams or spams
    features = [(participles(ham),'ham') for ham in hams]
    features += [(participles(spam),'spam') for spam in spams]
    return features

def train(samples):
    classes = defaultdict(lambda: 0)
    freq = defaultdict(lambda: 1)    #避免为0

    for feats, label in samples:
        classes[label] +=1
        ls ={}
        for feat in feats:
            if(ls.__contains__((label,feat)) == False):
                freq[label,feat] +=1
                ls[label,feat] =1
    
    # freq['spam','subject'] -=1
    for label,feat in freq.keys():
        if(freq[label,feat] >= classed[label]):
            freq[label,feat] = classed[label] - 1


    for label, feat in freq:
        freq[label,feat] /= classes[label]          #P(H or S | W) 后验概率


    # for label in classes:
    #     classes[label] /= len(samples)             #P(S/H) 先验概率

    return classes,freq

def classify(sample,classifier):
    classes,freq = classifier
    words,label = sample
    ps = 0
    for word in words:
        ps+=-math.log(freq.get(('spam',word),10**(-7)))
    ph = 0
    for word in words:
        ph+=-math.log(freq.get(('ham',word),10**(-7)))
    if(ps>ph):
        return 'spam'
    else:
        return 'ham'

def main():
    hams_path_train = r'enron1/ham'
    spams_path_train = r'enron1/spam'
    hams_path_test = r'enron1/ham'
    spams_path_test = r'enron1/spam'

    hams_train = gethams(hams_path_train)
    spams_train = getspams(spams_path_train)
    features = getfeatures(hams_train,spams_train)

    hams_test = gethams(hams_path_test)
    spams_test = getspams(spams_path_test)
    samples = getfeatures(hams_test,spams_test)

    classifier = train(features)

    mistakes = 0

    file_names = []

    for root,dirs,files in os.walk(hams_path_test):
        for file in files:
            file_names.append(file)
    for root,dirs,files in os.walk(spams_path_test):
        for file in files:
            file_names.append(file)

    for i in range(len(samples)):
        sample = samples[i]
        if(classify(sample,classifier)==sample[1]):
            mistakes+=1
        print(file_names[i])
        print("actual type: "+classify(sample,classifier))
        print("result: "+sample[1])
        print("----------------------------------------")
    print(mistakes,mistakes/len(samples))




if __name__ == '__main__':
    main()




