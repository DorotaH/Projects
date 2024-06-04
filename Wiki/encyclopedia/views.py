from django.shortcuts import render
import markdown

from . import util   

def convert(title):
    temp = markdown.Markdown()
    if util.get_entry(title) == None:
        return None
    else:
        return temp.convert(util.get_entry(title))


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
    
def entry(request, title):
    entry_content = convert(title)
    if entry_content == None:
        return render(request, "encyclopedia/error.html", {
            "message": "Error 404: this entry does not exist"
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "text": convert(title)
        })

def submit(request):
    if request.method == "POST":
        input = request.POST['q']
        entry_content = convert(input)
        if entry_content is not None:
            return render(request, "encyclopedia/entry.html", {
                "title": input,
                "text": entry_content 
            })
        else:
            list_of_entries = util.list_entries()
            print = []
            for entry in list_of_entries:
                if input in entry:
                    print.append(entry)
            return render(request, "encyclopedia/recommendations.html", {
                "entries": print
            })
            
def newPage(request):
    if request.method == "GET":
        return render(request, "encyclopedia/NewPage.html")
    else:
        title = request.POST['title']
        entry_content = request.POST['text']
        
        if util.get_entry(title) is not None:
            return render(request, "encyclopedia/error.html", {
                "message": "Page with this title already exists"
            }) 
        else:
            util.save_entry(title, entry_content)
            return render(request, "encyclopedia/entry.html", {
                "title" : title,
                "text": convert(title)
            })
            
def edit(request, title):
    return render(request, "encyclopedia/edit.html", {
        "text": util.get_entry(title),
        "title": title 
    })
        
def save(request):
    if request.method == "POST":
        title = request.POST['title']
        text = request.POST['text']
        util.save_entry(title, text)
        return render(request, "encyclopedia/entry.html", {
            "title" : title,
            "text": convert(title)
        })
        
def random(request):
    import random
    lucky_number = random.choice(util.list_entries())
    return render(request, "encyclopedia/entry.html", {
        "title": lucky_number,
        "text": convert(lucky_number)
    })