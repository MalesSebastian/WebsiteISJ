import config.settings
import json
import os

from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q
from django.http import HttpResponse, HttpResponseForbidden
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.static import serve

from models import Post
from post.forms import PostFormSet
from post.models import Page


def show_page(request, slug):
    page = get_object_or_404(Page, slug=slug)
    return HttpResponse(
        "<head><title>" + page.name + '</title><link rel="stylesheet" type="text/css" '
                                      'href="/static/prism/prism.css"><script '
                                      'src="/static/prism/prism.js"></script></head><body>' + page.text + "</body>")


def files_filter(request):
    return JsonResponse({'results': list(Post.objects.filter(Q(name__contains=request.GET["query"]) |
                                                             Q(author__first_name__contains=request.GET["query"]) |
                                                             Q(author__last_name__contains=request.GET["query"]),
                                                             location="exterior")
                                         .values('name', 'author__first_name', 'author__last_name', 'file'))})


@staff_member_required
def add_multiple_files(request):
    if request.method == "POST":
        visibility = request.POST["visibility"]
        request.POST.pop("visibility", None)
        formset = PostFormSet(data=request.POST or None, files=request.FILES or None)
        if formset.is_valid():
            instances = formset.save(commit=False)
            for instance in instances:
                instance.author = request.user
                instance.location = visibility
                instance.save()
            formset.save_m2m()
            return redirect("/admin/post/post/")
        else:
            response = HttpResponse(json.dumps({"errors": formset.errors}),
                                    content_type='application/json')
            response.status_code = 400
            return response
    else:
        return HttpResponseForbidden()


@staff_member_required
def page_preview(request):
    if request.method == "GET":
        return HttpResponse(
            "<head><title>" + "{0}" + '</title><link rel="stylesheet" type="text/css" '
                                      'href="/static/prism/prism.css"><script '
                                      'src="/static/prism/prism.js"></script></head><body>' + "{0}<br>" +
            request.user.get_full_name() + "<br>{1}" + "</body>")
    else:
        return HttpResponseForbidden()


def exterior_files(request, location, path):
    if location is not "interior":
        return serve(request, os.path.join("documents", location, path), document_root=config.settings.MEDIA_ROOT)
