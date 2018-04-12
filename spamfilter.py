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

    freq['spam','subject'] -=1


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

    # ac_label = label
    # pl = []
    # pw = []
    # for word in words:
    #     if (freq.__contains__(('spam',word)) or freq.__contains__(('ham',word))):
    #         pn = freq[('spam',word)]
    #         if(pn == 1):
    #             pn /= classes['spam']
    #     else:
    #         pn = 0.4         #经验值
    #     pl.append(pn)
    #     pw.append(word)
    # ppp = 1
    # for pn in pl:
    #     ppp *=pn
    # _p = 1
    # for pn in pl:
    #     _p *=(1-pn)
    # p = ppp/(ppp+_p)
    # print(str(p)+" "+str(ppp)+" "+str(_p))
    # if (p>=0.9):
    #     return 'spam'
    # else:
    #     return 'ham'
    #
    # # for i in range(len(pl)):
    # #     if(pl[i]>1):
    # #         print(str(pl[i])+pw[i])
    #
    # # sp = 0
    # # for pn in pl:
    # #     sp += (math.log(1-pn)-math.log(pn))
    # # standard = math.log((1/0.9)-1)
    # # if(sp<=standard):
    # #     return 'spam'
    # # else:
    # #     return 'ham'
    #
    # # return 'spam'















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

    # flag = classify(samples[0],classifier)
    # print(samples[0][0])
    # # for feat in samples[0]:
    # pl = []
    # freq = classifier[1]
    # print(freq['spam','hplc'])
    # for word in samples[0][0]:
    #     if (freq.__contains__(('spam', word)) or freq.__contains__(('ham', word))):
    #         pn = freq[('spam',word)]
    #     else:
    #         pn = 0.4  # 经验值
    #     pl.append(pn)
    # print(pl)

    # freq = classifier[1]
    # values = []
    # print(classifier[1].values())





if __name__ == '__main__':
    main()











