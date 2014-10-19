from urllib.request import urlopen
import random
import find_data
import re
def readPage(url):
    return str(urlopen(url).read())


from html.parser import HTMLParser

class MyHTMLParser2(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.inlist=False
        self.inlink=False
        self.curr_link=''
        self.links=[]
        self.done=False
    def handle_starttag(self, tag, attrs):
        if tag in ['li','p','td']:
            self.inlist=True
            return
        if tag=='a':
            if self.inlist or 1:
                self.inlink=True
                for item in attrs:
                    if item[0]=='href':
                        self.curr_link=item[1]
                        if 'wiki' not in self.curr_link:
                            self.bad_link=True
                        elif ':' in self.curr_link:
                            self.bad_link=True
                        elif '.' in self.curr_link:
                            self.bad_link=True
                        elif '#' in self.curr_link:
                            self.bad_link=True
                        elif self.done:
                            self.bad_link=True
                        else:
                            self.bad_link=False
                        if not self.bad_link:
                            for item2 in attrs:
                                if item2[0]=='title':
                                    for link in self.links:
                                        if link[0]==self.curr_link:
                                            return
                                    self.links.append((self.curr_link,item2[1]))
                                    return
                        return
        if tag =='span':
            for item in attrs:
                if item[0]=='id':
                    if item[1]=='References' or item[1]=='Notes' or item[1]=='See_also':
                        self.done=True
    def handle_endtag(self, tag):
        if tag in ['li','p','td']:
            self.inlist=False
        if tag=='a':
            self.inlink=False
    def handle_data(self, data):
        """donothing"""
def getLinks(url):
    """returns a list of tuples, where each tuple contains(<link>,<title>) for each link in the page. links that are not articles are filtered out"""
    parser = MyHTMLParser2()
    parser.feed(readPage(url))
    return parser.links
def play():
    print("wikipedia guessing game!")
    print()
    donePlaying=False
    while(not donePlaying):
        url='http://en.wikipedia.org/wiki/'+input("Enter a url to pull links from... http://en.wikipedia.org/wiki/")
        links = getLinks(url)
        print()
        print('word bank created... would you like to see the word bank? (Y/N)')
        response=input()
        if response=='Y':
            print('_'*80)
            [print(link[1]) for link in links]
            print('_'*80)
        doneEditing=False
        while(not doneEditing):  
            print() 
            print('would you like to edit the word bank? (Y/N)')
            response=input()
            if response=='Y':
                links=edit(links)
                print()
                input("press enter to see new word bank...")
                print('_'*80)
                [print(link[1]) for link in links]
                print('_'*80)
            else:
                doneEditing=True        
        doneUrl=False
        print()
        input("press enter to start a round...")
        while(not doneUrl):
            print()
            print("round started. Say 'I give up' to give up. Say 'Show bank' to see word bank. Say 'Show clues' to see all clues.")
            chosen=random.choice(links)
            text=find_data.ParseURL('http://en.wikipedia.org'+str(chosen[0]))
            #print(text)
            #print(chosen[0])
            won=False
            #print(chosen[0],chosen[1])
            guesses=0
            given=0
            clues=[]
            while(not won):
                clues.append(random.choice(text))
                print()
                print('clue:',clues[-1])
                guesses+=1
                given+=1
                guess=input("guess "+str(guesses)+": ")
                if guess==chosen[1]:
                    won=True
                    print('Congrats! You took',guesses,'guesses and',given,'clues!')
                if guess=='I give up':
                    print('Better luck next time! You attempted',guesses,'times with',given,'clues.')
                    print(chosen[1])
                    won=True
                if guess=='Show bank':
                    print('_'*80)
                    [print(link[1]) for link in links]
                    print('_'*80)
                if guess=='Show clues':
                    print(clues)
                if guess=='':
                    guesses-=1
            print('play again with this url? (Y/N)')
            response=input()
            if response=='N':
                doneUrl=True
        print('play again with new url? (Y/N)')
        response=input()
        if response=='N':
            donePlaying=True
    print('done')
def edit(links):
    print()
    print("Type in a word to delete it. Say 'Iterate through all' to iterate through every word. Say slice[<start>:<end>] to slice the bank. Say 'I am done' to quit")
    print()
    done = False
    toRemove=[]
    while (not done):
        response=input()
        if 'slice' in response:
            data=response.split(':')
            links=links[int(data[0][6:]):int(data[1][:-1])]
            return links
        if response=='I am done':
            purge(links,toRemove)
            return links
        if response=='Iterate through all':
            print("say anything (besides 'I am done') to remove each item")
            print()
            i=0
            while(not done and i<len(links)):
                response=input(links[i][1]+": ")
                if response=='I am done':
                    purge(links,toRemove)
                    return links
                if len(response):
                    toRemove.append(links[i][1])
                i+=1
            purge(links,toRemove)
            return links
        toRemove.append(response)
    return links
def purge(links,keys):
    for key in keys:
        for link in links:
            if key==link[1]:
                links.remove(link)

play()