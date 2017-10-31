import re
from nltk.corpus import stopwords

scentence = 'El problema del matrimonio es que se acaba todas las noches despues de hacer el amor, y hay que volver a reconstruirlo todas las mananas antes del desayuno.'

#We only want to work with lowercase for the comparisons
scentence = scentence.lower()

#remove punctuation and split into seperate words
words = re.findall(r'\w+', scentence,flags = re.UNICODE | re.LOCALE)

#This is the simple way to remove stop words
important_words=[]
for word in words:
    if word not in stopwords.words('spanish'):
        important_words.append(word)

print (important_words)

#This is the more pythonic way
important_words = filter(lambda x: x not in stopwords.words('spanish'), words)

print (important_words)
