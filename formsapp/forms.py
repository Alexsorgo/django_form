from django import forms
from models import req, res, proj
from splitjson.widgets import SplitJSONWidget


class ProjectForm(forms.ModelForm):

    class Meta:
        model = proj
        fields = ('project',)


class RequestForm(forms.ModelForm):

    class Meta:
        model = req
        fields = ('url', 'method', 'data_form', 'body', 'tag', 'header', 'project')
