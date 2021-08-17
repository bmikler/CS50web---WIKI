from django.shortcuts import redirect, render
from django import forms
import markdown
import random
from . import util

# form for search
class SearchForm(forms.Form):
    q = forms.CharField()

# form for new page
class NewPageForm(forms.Form):
    title = forms.CharField()
    content = forms.CharField()

# form for edit page
class EditPageForm(forms.Form):
    edit_content = forms.CharField()


def index(request):

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, entry):

    if request.method == "POST":
        return redirect('edit_page', entry=entry)

    # check if entry exist in entries directory
    try:
        text = markdown.markdown(util.get_entry(entry))
        edit = True
    except:
        text = "<h1>Entry not found!</h1>"
        edit = False

    # render page with entry text
    return render(request, "encyclopedia/entry.html", {
        "entry": text,
        "edit": edit
    })


def search(request):

    if request.method == "POST":

        # fill the form by informations posted by form
        form = SearchForm(request.POST)

        if form.is_valid():
            query = form.cleaned_data["q"]

            # check if query is in the list of entries
            if list_check(query, util.list_entries()):
                # redirect to entry with entry name entry
                return redirect('entry', entry=query)

            list = []

            for entry in util.list_entries():
                if entry.lower().count(query.lower()) > 0:
                    list.append(entry)

            # check if input match any of entries
            if len(list) > 0:
                return render(request, "encyclopedia/search.html", {
                    "list": list
                })
            else:
                return render(request, "encyclopedia/search.html", {
                    "message": "Not Found"
                })

        else:
            # if user submit empty prompt error
            return render(request, "encyclopedia/search.html", {
                "message": "No search query given"
            })

    else:
        return redirect('index')


def new_page(request):

    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():

            title = form.cleaned_data['title']
            content = "#" + title + "\n" + form.cleaned_data['content']

            # check if the title is in the list of entries
            if list_check(title, util.list_entries()):
                return render(request, "encyclopedia/new_page.html", {
                    "message": "Error. This entry exist in the wiki."
                })

            else:
                util.save_entry(title, content)
                return redirect('entry', entry=title)
        else:
            return render(request, "encyclopedia/new_page.html", {
                "message": "Please fill all fields."
            })

    return render(request, "encyclopedia/new_page.html")


def edit_page(request, entry):

    if request.method == "POST":
        form = EditPageForm(request.POST)
        if form.is_valid():
            edit_content = form.cleaned_data['edit_content']
            print(edit_content)
            util.save_entry(entry, edit_content)
            return redirect('entry', entry=entry)

    content = util.get_entry(entry)

    return render(request, "encyclopedia/edit_page.html", {
        "title": entry,
        "content": content
    })


def random_page(request):
    entry_no = (random.randrange(len(util.list_entries())))
    entry = util.list_entries()[entry_no]
    return redirect('entry', entry=entry)

# function to check if title is in the wiki


def list_check(title, list):
    for entry in list:
        if title.lower() == entry.lower():
            return True

    return False
