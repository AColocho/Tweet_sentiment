import nltk
from nltk.corpus import stopwords
import string
from nltk import word_tokenize, FreqDist
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import numpy as np
from nltk.stem import WordNetLemmatizer
from sklearn.metrics import f1_score,accuracy_score,precision_score,recall_score,confusion_matrix,classification_report

def uniqueWords(tokenList):
    """
    Parameters:
        TokenList: List of tokenized words.
    returns:
        Number of unique words in list.
    
    Additional:
        Parameter does not have to tokenized. However, it does have to be in list format.
    """
    tokens = []
    for i in tokenList:
        tokens.extend(i)
    
    mySet = set()
    for i in tokens:
        mySet.add(i)
    
    return len(mySet)

def cleanTokenList(tokenList):
    """
    Parameters:
        tokenList: List of tokenized words. 
    returns:
        Clean list of words.
        
    Removes English stopwords and punctuation.
    """
    stopwordsList = stopwords.words('english') + list(string.punctuation)
    tokens = []
    for i in tokenList:
        tokens.extend(i)
    
    cleanList = []
    for word in tokens:
        word = word.lower()
        if word not in stopwordsList:
            cleanList.append(word)
    
    return cleanList

def cleanToken(tokenList,additionalWords=False):
    """"
    Parameters:
        tokenList: List of tokenized words.
        additionalWords: Set to False or pass a list of additional words to remove
        from tokenList.
    Returns:
        Clean list of words.
        
    Removes English stopwords, punctionation, and additional words assigned to additionalWords.
    """
    stopwordsList = stopwords.words('english') + list(string.punctuation)
    
    if additionalWords is not False:
        stopwordsList.extend(additionalWords)
    
    cleanList = []
    for word in tokenList:
        word = word.lower()
        if word not in stopwordsList:
            cleanList.append(word)
    return cleanList

def cleanTweets(tweet,additionalWords = False):
    """
    Parameters:
        tweet: A sentence in string form.
        additionalWords: Set to False or pass a list of additional words to remove
        from tokenList.
    Returns:
        String remaining words after cleaning process.
        
    Tokenizes words, cleans words, lemmatizes words, and combines them into a string.
    """
    wml = WordNetLemmatizer()
    tokenized = word_tokenize(tweet)
    
    if additionalWords is not False:
        cleanWords = cleanToken(tokenized,additionalWords)
    else:
        cleanWords = cleanToken(tokenized)
        
    cleanLemmatize = [wml.lemmatize(i) for i in cleanWords]
    stringTweet = " ".join(cleanLemmatize)
    return stringTweet

def ModelCompare(algos,X_train,y_train,X_test,y_test):
    """
    Parameters:
        algos: Dictionary of all algorithms from sklearn to fit
        X_train: X training data
        y_train: y training data
        X_test: X testing data
        y_test: y testing data
    returns:
        data frame with training and testing accuracy scores and f1 scores
    """
    algo = []
    trainAccuracy = []
    testAccuracy = []
    f1Train = []
    f1Test = []

    for i in algos.keys():
        algo.append(i)
        model = algos.get(i)
        model.fit(X_train,y_train)

        train = model.predict(X_train)
        test = model.predict(X_test)

        trainAccuracy.append(accuracy_score(y_train,train))
        testAccuracy.append(accuracy_score(y_test,test))

        f1Train.append(f1_score(y_train,train))
        f1Test.append(f1_score(y_test,test))
        
    return pd.DataFrame({'Models':algo,'Training Accuracy':trainAccuracy,'Test Accuracy':testAccuracy,'F1 Train':f1Train,'F1 Test':f1Test})


def ModelCompareMulti(algos,X_train,y_train,X_test,y_test,labels=None):
    """
    Parameters:
        algos: Dictionary of all algorithms from sklearn to fit
        X_train: X training data
        y_train: y training data
        X_test: X testing data
        y_test: y testing data
        labels: Labels of data. 
    returns:
        prints algorithm name, training accuracy, confusion matrix, and classification report.
    
    *Compares ternary classification models*
    """
    algo = []
    trainAccuracy = []
    confusion = []
    report = []

    for i in algos.keys():
        algo.append(i)
        model = algos.get(i)
        model.fit(X_train,y_train)

        train = model.predict(X_train)
        test = model.predict(X_test)

        trainAccuracy.append(accuracy_score(y_train,train))
        confusion.append(confusion_matrix(y_test,test,labels=labels))
        report.append(classification_report(y_test,test,labels=labels))
        
    for i in range(len(algo)):
        print(algo[i])
        print('Training Accuracy: {}'.format(trainAccuracy[i]))
        print(confusion[i])
        print(report[i])

