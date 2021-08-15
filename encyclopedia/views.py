from django.shortcuts import redirect, render
from django import forms
import markdown
import random

from . import util


class SearchForm (forms.Form):
    q = forms.CharField()


def index(request):

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": SearchForm()
    })


def entry(request, entry):

    # check if entry exist in entries directory
    try:
        text = markdown.markdown(util.get_entry(entry))
    except:
        text = "<h1>Entry not found!</h1>"

    # render page with entry text
    return render(request, "encyclopedia/entry.html", {
        "entry": text
    })


def search(request):
    if request.method == "POST":

        # fill the form by informations posted by form
        form = SearchForm(request.POST)

        if form.is_valid():
            query = form.cleaned_data["q"]

            # check if query is in the list of entries
            for entry in util.list_entries():
                if query.lower() == entry.lower():
                    # redirect to entry with entry name entry
                    return redirect('entry', entry=entry)

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

def random_page(request):
    entry_no = (random.randrange(len(util.list_entries())))
    entry = util.list_entries()[entry_no]
    return redirect('entry', entry=entry)



