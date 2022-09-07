from random import randint
from django.shortcuts import render
from django import forms
import time
from markdown2 import Markdown
from . import util
from .models import Entries
from django.http import HttpResponseRedirect


markdowner = Markdown()

class NewPageForm(forms.Form):
    title = forms.CharField(max_length=24, widget=forms.TextInput(attrs={'class': 'test2'}))
    markdown = forms.CharField(widget=forms.Textarea(attrs={'class': 'test'}))
       
    
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "Entries": Entries.objects.all()       
    })
    

def wiki(request):
    try:
        if request.method == "GET":
            print(request)
            test = str(request)
            test1 = test[25:-6]
            print(test1)
            title = util.get_entry(test1)
            print(title)
            return render(request, "encyclopedia/title.html", {
            "title" : util.get_entry(test1)
        })
            
        if request.method =="POST":
            searchform = request.POST
            searchquery = searchform["search_query"]
            print(searchquery)
            test = util.get_entry(searchquery)
            words = util.list_entries()
            print(words)
            wordcount = 0
            entrylength = len(words)
            wordlist = []
            words = sorted(words)
            if test != None:
                search = markdowner.convert(test)
                return render(request, "encyclopedia/title.html", {
                        "wiki" : search ,
                        "title": searchquery
                        }) 
            if test == None:
                simcheck = []          
                while wordcount < entrylength:                            
                    for word in words:
                        words = str(words)     
                        wordcount += 1
                        for letter in word:
                            for letters in searchquery:
                                if letter.upper() in letters or letter.lower() in letters:
                                    print(letters)
                                    simcheck += [letters]                         
                                    if len(simcheck) > 3:
                                        if word in wordlist:
                                            continue
                                    wordlist.append(word)
                                    print(word)
                                        
                        else:
                            wordcount += 1 
                            print(searchquery)
                            continue                    
                print(sorted(wordlist))
                if not wordlist:
                    return render(request, "encyclopedia/NotFound.html", {})
                    
            return render(request, "encyclopedia/otherpages.html",{
                            "name" : sorted(wordlist),
                            "wiki": util.get_entry(test)
                        })
    except ValueError:
            print("Symbols are not accepted in the query")
            return render(request, "encyclopedia/wiki.html", {})
            
def title(request, title):
    if request.method == "GET":
        print(request)
        test = str(request)
        test1 = test[25:-6]
        print(test1)
        title = util.get_entry(test1)
        test2 = markdowner.convert(title)
        print(title)
        return render(request, "encyclopedia/title.html", {
            "wiki" : test2,
            "title": test1           
        })
    

def createpage(request):
        return render(request, "encyclopedia/createpage.html", {
        "form": NewPageForm()
    })
    
    
def entries(request):
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            text = form.cleaned_data['markdown']
            msg = "Error: File name exists, please choose another title"
            if util.get_entry(title) is not None:
                print("WORKS")
                return render(request, "encyclopedia/exists.html", {
                         "FileExists": msg 
                         }) 
                
            util.save_entry(title, text)
            time.sleep(1)
        
        return render(request, "encyclopedia/title.html")  
        
def edit(request):
    if request.method == "POST":  
        title = request.POST['entrytitle']
        markdown = util.get_entry(title)     
        return render(request, "encyclopedia/edit.html", {
        "data" : title,
        "test": markdown
    })
    return render(request, "encyclopedia/edit.html")



def save_entries(request):
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            text = form.cleaned_data['markdown']         
            util.save_entry(title, text)
            print(text)
            time.sleep(1)
            entrylist = util.list_entries()
        
        return HttpResponseRedirect(f"wiki/{title}.md")
        
def random(request):
    lst = util.list_entries()
    length = len(lst) - 1
    value = randint(0, length)
    print(value)
    entry = lst[value]
    
    return HttpResponseRedirect(f"wiki/{entry}.md")
    
        

        
    