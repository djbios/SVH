from django import forms


class AddFolderForm(forms.Form):
    magnet = forms.CharField()


class RenameForm(forms.Form):
    find = forms.CharField(max_length=100)
    replace = forms.CharField(required=False, max_length=100)
    ids = forms.CharField(widget=forms.HiddenInput())
