from django import forms


class ChatInputForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)
