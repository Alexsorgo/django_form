from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template

from formsapp.models import req, res, proj
from pip._vendor import requests


def send_one(defin, pro):
    if defin.method == 'GET':
        try:
            r = requests.get(defin.url, headers=defin.header)
            b = res.objects.create(status=r.status_code, body=r.json(),
                                   project_id=pro, tag_id=defin.tag)
            print b
            b.save()
        except:
            raw = get_template("create_error.html")
            return HttpResponse(raw.render(Context({'wtf':
                                                        'Wrong request or something wrong with response'})))

    elif defin.method == 'POST':
        try:
            r = requests.post(defin.url, headers=defin.header, json=defin.body)
            b = res.objects.create(status=r.status_code, body=r.json(),
                                   project_id=pro, tag_id=defin.tag)
            print b
            b.save()
        except:
            raw = get_template("create_error.html")
            return HttpResponse(raw.render(Context({'wtf':
                                                        'Wrong request or something wrong with response'})))