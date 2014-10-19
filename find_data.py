from html.parser import HTMLParser
from urllib.request import urlopen
from string import ascii_letters

def readPage(url):
    return str(urlopen(url).read())

def ParseURL(URL):
    parser = MyHTMLParser()
    parser.feed(readPage(URL))
    parser.filter_length(parser.word_list)
    return parser.word_list

class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.text = []
        self.in_p = False
    def handle_starttag(self, tag, attrs):
        #print("Encountered a start tag:", tag)
        if tag=='p':
            self.in_p=True
    def handle_endtag(self, tag):
        #print("Encountered an end tag :", tag)
        if tag=='p':
            self.in_p=False
    def extract_words(self,text):
        words=[]
        curr_word=''
        for letter in text:
            if letter in ascii_letters:
                curr_word+=letter
            else:
                if(curr_word):
                    words.append(curr_word)
                curr_word=''
        if(curr_word):
                words.append(curr_word)
        return words
#returns list of only words
    def handle_data(self, data):
        #print("Encountered some data  :", data)
        if self.in_p==True:
            #if '\\' in data:
             #   new_data = data.replace('\\','')
            self.text.append(data)
            whole_string = ''

            for phrase in self.text:
                whole_string+=phrase
            word_list = self.extract_words(whole_string)

            #print(word_list)
            #self.filter_length(word_list)
            self.word_list = word_list

#FILTERTING 
    def filter_length(self,list):
        new_word_list = []
        for element in self.word_list:
            if len(element) >=4:
                 new_word_list.append(element)
        self.word_list = new_word_list
            


#ParseURL('http://en.wikipedia.org/wiki/Acting').





