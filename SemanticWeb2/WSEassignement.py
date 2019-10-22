import nltk
import requests as requests

nltk.download('punkt')

# Section 1

# utf-8-sig to have unicode without the BOM (Byte Order Mark)
bookFile = open('The Adventures of Tom Sawyer by Mark Twain', mode='r', encoding='utf-8-sig')
# Read the text of the book and remove the new line characters
book = bookFile.read()
# book = book.rstrip() # NB: here I still have the \n!!! TODO Remove this
book = book.replace('\n', ' ')
bookFile.close()

tokenized_book = nltk.word_tokenize(book)
# number of tokens (words and punctuation symbols) in the text
answer1 = len(tokenized_book)
# number of UNIQUE tokens (words and punctuation symbols) in the text. Same words with diff case letters will be
# considered as separate
answer2 = len(set(tokenized_book))

# performing Lemmatization

from nltk.stem.wordnet import WordNetLemmatizer

nltk.download('wordnet')
lemmatizer = WordNetLemmatizer()


# Takes a list of tokens as argument and returns the list lemmatized on the noun
def lemmatize_tokens(list_of_tokens):
    lemmatized_tokens = []
    for token in list_of_tokens:
        word = token
        # the if-else branches are needed to lemmatize correctly words that start with capital letters or that are
        # completely written in capital letters
        if word[0].isupper():
            if word.isupper():
                word = word.lower()
                word = lemmatizer.lemmatize(word, "n")
                word = word.upper()
            else:
                word = word.lower()
                word = lemmatizer.lemmatize(word, "n")
                word = word[0].upper() + word[1:]
            lemmatized_tokens.append(word)
        else:
            lemmatized_tokens.append(lemmatizer.lemmatize(token, "n"))

    return lemmatized_tokens


lemmatized_tokens = lemmatize_tokens(tokenized_book)
answer3 = len(set(lemmatized_tokens))


# What are the 20 most frequently occurring (unique) tokens in the text? What is their
# frequency?

def n_most_frequent_tokens(tokens, n):
    # variable that indicates if the token has already been found and so it's useless to redo the computation
    found = 0
    result = []
    for i in range(0, len(tokens)):
        for tup in result:
            if tokens[i] in tup:
                found = 1
                break
        if found == 0:
            result = result + [(tokens[i], tokens.count(tokens[i]))]
        else:
            found = 0
    return sorted(result, key=lambda x: x[1], reverse=True)[:n]


# I supposed that I have to find the lemmatized tokens and not just the tokens
answer4 = n_most_frequent_tokens(lemmatized_tokens, 20)

# ---------------------------------------------------------------------------------
# Section2

from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

# 2.1 No Filter: Consider all the words
text = book.replace('\n', ' ')
wordcloud1 = WordCloud(width = 800, height = 800, stopwords = set(),background_color='white').generate(text)
plt.imshow(wordcloud1, interpolation="bilinear")
plt.axis('off')
plt.show()
# #
# # #2.2 No Stopwords: Remove stopwords → You probably noticed that the most important
# # # words were mostly uninformative. To address this problem, a typical approach is to remove so called stopwords, which don’t carry a lot of meaning.
# # wordcloud2 = WordCloud(width = 800, height = 800, stopwords = STOPWORDS,background_color='white').generate(text)
# # plt.imshow(wordcloud2, interpolation="bilinear")
# # plt.axis('off')
# # plt.show()
# #
# # 2.3 NER: To further remove the words and only keep the entities in text, first extract the
# # entities using NLTK library then perform the wordcloud.
#
# import spacy
# from spacy import displacy
# from collections import Counter
# import en_core_web_sm
# nlp = en_core_web_sm.load()
# # Extraction of the named entities from the book's text
# entities = nlp(text)
# # I can use this to see how many times each entity appear (not requested)
# labels = [x.label_ for x in entities.ents]
# Counter(labels)
# # Remove words and only keep the entities (just concatenation of all the entities to obtain a word cloud from this)
# entitiesConcatenated = ""
# for entity in entities.ents:
#     entitiesConcatenated += entity.text + " "
# wordcloud3 = WordCloud(width = 800, height = 800, stopwords = STOPWORDS,background_color='white').generate(entitiesConcatenated)
# plt.imshow(wordcloud3, interpolation="bilinear")
# plt.axis('off')
# plt.show()
#
# # 2.4
# # TODO
# # newText = [x for x in tokenized_text if x[0].isupper()]
# # newText = ' '.join(newText)
# # import requests
# # PROBLEM: URL too long
# # url='http://api.dbpedia-spotlight.org/en/candidates?text='+ newText +'&types=Person'
# # r = requests.get(url = url)
# # print(r.content)
#
# # 3
# # In order to use real word vectors, I need to download a larger model (instead of the precedent spaCy's small model)
# import en_core_web_lg
# nlp = en_core_web_lg.load()
#
# # this function returns the content of the file passed as an argument
# def get_file_contents(filename):
#   with open(filename, mode = 'r', encoding = 'utf-8-sig') as filehandle:
#     file = filehandle
#     filecontent = file.read().rstrip()
#     file.close()
#     return (filecontent)
#
# # list of the book titles
# booksTitles = ["A Christmas Carol in Prose; Being a Ghost Story of Christmas by Charles Dickens",
#                "The Brothers Karamazov by Fyodor Dostoyevsky",
#                "The Iliad by Homer",
#                "The Innocents Abroad by Mark Twain",
#                "The Picture of Dorian Gray by Oscar Wilde",
#                "The Prince by Niccolò Machiavelli",
#                "The Strange Case of Dr. Jekyll and Mr. Hyde by Robert Louis Stevenson"]
#
# # list of tuples that contains (title, content) pairs
# booksToBeCompared = [(title, get_file_contents(title)) for title in booksTitles]
#
# # needed since the default limit is 1000000 and some of the picked books is longer
# nlp.max_length = 2000000
#
# firstBook = nlp(text)
# result = []
# for i in range(0, len(booksToBeCompared)):
#     title = booksToBeCompared[i][0]
#     similarity = nlp(booksToBeCompared[i][1]).similarity(firstBook)
#     result += [(title, similarity)]
#
# # sort the element in the result according to the similarity in a descending order
# section3result = sorted(result ,key=lambda x: x[1], reverse=True)
