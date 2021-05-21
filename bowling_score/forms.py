from django import forms

class EntryForm(forms.Form):
    entry = forms.CharField(
        max_length=1,
        min_length=1,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Add one entry at a time"
        })
    )
