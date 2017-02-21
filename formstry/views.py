import json
import ast
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404, render
from django.template import Context
from django.template.loader import get_template
from django.template.defaulttags import register
from pip._vendor import requests
# from functions import send_one
from formsapp.models import req, res, proj
from formsapp.forms import RequestForm
from django.template.context_processors import csrf


def welcome(request):
    if request.method == 'GET':
        all = proj.objects.all()
        wtf = {'wtf': all}
        c = {}
        c.update(csrf(request))
        return HttpResponse(render(request, 'Welcome.html', wtf))
    if request.method == 'POST':
        if request.POST.get('exist') == None and request.POST.get('pro') != '':
            try:
                b = proj.objects.create(project=request.POST.get('pro'))
                b.save()
                c = {}
                c.update(csrf(request))
                wtf = {'pro': request.POST.get('pro'), 'wtf': request.POST.get('pro')}
                return HttpResponse(render(request, 'newproject.html', wtf, c))
            except:
                raw = get_template("create_error.html")
                return HttpResponse(raw.render(Context({'wtf': 'This project already exist'})))
        elif request.POST.get('exist') != None and request.POST.get('pro') == '':
            cur_proj = req.objects.filter(project_id=request.POST.get('exist'))
            if cur_proj.count() == 0:
                c = {}
                c.update(csrf(request))
                wtf = {'pro': request.POST.get('exist'), 'wtf': request.POST.get('exist')}
                return HttpResponse(render(request, 'newproject.html', wtf, c))
            else:
                c = {}
                c.update(csrf(request))
                tags = req.objects.filter(project_id=request.POST.get('exist'))
                data = {'pro': request.POST.get('exist'), 'wtf': request.POST.get('exist'), 'ftw': tags}
                return HttpResponse(render(request, 'decision.html', data, c))
        else:
            raw = get_template("create_error.html")
            return HttpResponse(raw.render(Context({'wtf': 'Please use only one case'})))
    else:
        raw = get_template("create_error.html")
        return HttpResponse(raw.render(Context({'wtf': 'Unsupported method'})))


def create_req(request):
    form = RequestForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return HttpResponseRedirect(instance.get_absolute_url())
    else:
        form = RequestForm()

    args = {}
    args.update(csrf(request))
    args['form'] = form
    return render_to_response('create_article.html', args)


def show_req(request, tag=None):
    instance = get_object_or_404(req, tag=tag)
    print type(instance.body)
    form = RequestForm(request.POST or None, instance=instance)
    if form.is_valid():
        url = request.POST.get('url')
        method = request.POST.get('method')
        data_form = request.POST.get('data_form')
        header = request.POST.get('header')
        body = request.POST.get('body')
        tag = request.POST.get('tag')
        project = request.POST.get('project')
        try:
            instance = req.objects.create(url=url, method=method, data_form=data_form, header=header, body=body, tag=tag, project_id=project)
            instance.save()
            all = req.objects.get(tag=tag)
            context = {
                'obj': all
            }
            return render_to_response('current.html', context)
        except:
            return HttpResponse('Nothing to change')

    args = {}
    args.update(csrf(request))
    args['form'] = form
    return render_to_response('create_article.html', args)


def show_all(request):
    all = req.objects.all()
    context = {
        'obj_list': all
    }
    return render_to_response('index.html', context)


def show_detail(request, tag=None):
    instance = get_object_or_404(req, tag=tag)
    print type(instance.body)
    json.dumps(instance.header)
    context = {
        'obj': instance,
        'head': json.dumps(instance.header),
        'body': json.dumps(instance.body)
    }
    return render_to_response('current.html', context)


def create_negative(request):
    defin = req.objects.get(tag=request.POST.get('tag'))
    pro = request.POST.get('pro')
    if 'negative' in request.POST:
        all = req.objects.get(tag=request.POST.get('tag'))
        if type(all.body) == unicode:
            wtf = {'wtf': json.loads(all.body), 'pro': request.POST.get('pro'), 'tag': request.POST.get('tag')}
        if type(all.body) == dict:
            wtf = {'wtf': all.body, 'pro': request.POST.get('pro'), 'tag': request.POST.get('tag')}

        c = {}
        c.update(csrf(request))
        return HttpResponse(render(request, 'negative.html', wtf, c))

    if 'definite' in request.POST:
        if defin.method == 'GET':
            try:
                r = requests.get(defin.url)
                b = res.objects.create(status=r.status_code, body=r.json(),
                                       project_id=pro, tag_id=defin.tag)
                b.save()
            except:
                raw = get_template("create_error.html")
                return HttpResponse(raw.render(Context({'wtf': 'Something wrong'})))

        elif defin.method == 'POST':
            try:
                r = requests.post(defin.url, headers=defin.header, json=defin.body)
                b = res.objects.create(status=r.status_code, body=r.json(),
                                       project_id=pro, tag_id=defin.tag)
                print b
                b.save()
            except:
                raw = get_template("create_error.html")
                return HttpResponse(raw.render(Context({'wtf': 'Something wrong'})))
        context = {
            'obj': r,
            # 'head': json.dumps(defin.header),
            'body': json.dumps(r.json()),
        }
        print r.status_code
        print json.dumps(r.json())
        return render_to_response('defin.html', context)


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


def negative(request):
    all = req.objects.get(tag=request.POST.get('tag'))
    print request.POST.get('tag')
    print all
    body = {}
    if request.method == 'POST':
        if 'value' in request.POST:
            u = 0
            keys = request.POST.getlist('key')
            values = request.POST.getlist('value')
            while u < len(keys):
                body[keys[u]] = values[u]
                u += 1
            u = 1
            # while True:
            # try:
            req.objects.create(url=all.url, method=all.method,
                               header=all.header, body=body, tag=(all.tag) + str(5),
                               project_id=request.POST.get('pro'))
                # break
            # except:
            #     return HttpResponse('error')
                # u += 1
                # continue
    wtf = req.objects.filter(project_id=request.POST.get('pro'))
    print wtf
    raw = get_template("index.html")
    return HttpResponse(raw.render(Context({'obj_list': wtf})))
