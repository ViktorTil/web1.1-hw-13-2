from bson.objectid import ObjectId
from django.shortcuts import redirect, render
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .forms import AuthorForm, TagForm, QuoteForm
from .models import Author, Tag, Quote
from .utils import get_mongodb, save_tag_to_quote, top_ten_tags

def main(request, page = 1):
    db = get_mongodb()
    quotes = db.quotes.find()
    top_tags = top_ten_tags()
    per_page = 10
    paginator = Paginator(list(quotes), per_page)
    quotes_on_page = paginator.page(page)
    return render(request, 'quotes/index.html', context={'quotes': quotes_on_page, 'top_tags': top_tags})

def get_author_info(request):
    author_ = request.path.removeprefix('/author/')
    db = get_mongodb()
    author = db.authors.find_one({"_id": ObjectId(author_)})
    author_info={"fullname" : author['fullname'], "born_date" : author['born_date'], "born_location" : author['born_location'], "description" : author['description']}
    return render(request, 'quotes/author.html', context=author_info)
    
    
@login_required
def upload_author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            fullname = form["fullname"].value()
            born_date = form["born_date"].value()
            born_location = form["born_location"].value()
            description = form["description"].value()
            db = get_mongodb()
            db.authors.insert_one({"fullname": fullname,
                                   "born_date": born_date,
                                   "born_location": born_location,
                                   "description": description})
            return redirect(to='quotes:root')
        else:
            return render(request, 'quotes/add_author.html', {'form': form})

    return render(request, 'quotes/add_author.html', {'form': AuthorForm()})

@login_required
def upload_quote(request):
    db = get_mongodb()
    authors=db.authors.find()
    tags = db.tags.find()
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            author=request.POST['author']
            author_id = db.authors.find_one({"fullname": author})['_id']
            tags_list =request.POST.getlist('tags')        
            db.quotes.insert_one({"quote": form['quote'].value(),
                                   "tags": tags_list,
                                   "author": author_id})

            save_tag_to_quote(form['quote'].value(), tags_list)
            return redirect(to='quotes:root')
        else:
            return render(request, 'quotes/add_quote.html', {'authors': authors, 'tags': tags, 'form': form})

    return render(request, 'quotes/add_quote.html', {'authors': authors, 'tags': tags, 'form': QuoteForm()})
   
                


@login_required
def upload_tag(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            db = get_mongodb()
            db.tags.insert_one({"name": form['name'].value()}) 
            return redirect(to='quotes:root')
        else:
            return render(request, 'quotes/add_tag.html', {'form': form})

    return render(request, 'quotes/add_tag.html', {'form': TagForm()})


def get_tag_quotes(request):
    tag_ = request.path.removeprefix('/tag/')
    print(tag_)
    db = get_mongodb()
    quotes = db.quotes.find({"tags": tag_})
    return render(request, 'quotes/tag.html', context={'tag': tag_,'quotes': quotes})
