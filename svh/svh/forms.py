from django import forms


class AddFolderForm(forms.Form):
    magnet = forms.CharField()


class RenameForm(forms.Form):
    find = forms.CharField()
    replace = forms.CharField(required=False)