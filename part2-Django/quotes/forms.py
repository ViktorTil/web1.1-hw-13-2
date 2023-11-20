from django.forms import ModelForm, CharField, TextInput, DateTimeField
from .models import Author, Tag, Quote


class AuthorForm(ModelForm):
    fullname = CharField(max_length=50) 
    born_date = CharField(max_length=50)
    born_location = CharField(max_length=50)
    description = TextInput()
    
    class Meta:
        model = Author
        fields = ['fullname', 'born_date', 'born_location', 'description']
        

    def __str__(self):
        return f"{self.fullname}"

class TagForm(ModelForm):

    name = CharField(min_length=3, max_length=35, required=True, widget=TextInput())
    
    class Meta:
        model = Tag
        fields = ['name']

   
class QuoteForm(ModelForm):
    quote = TextInput()
    
    class Meta:
        model = Quote
        fields = ['quote']
        exclude = ['author','tags']
        
