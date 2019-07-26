from django import forms


class AddFolderForm(forms.Form):
    magnet = forms.CharField()
