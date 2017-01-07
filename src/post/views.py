from pprint import pprint

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.encoding import smart_str
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse, HttpResponseForbidden, Http404

from haystack.forms import SearchForm

from forms import CreatePostForm
from models import Post

import magic


@login_required
def upload_file_form(request):
    form = CreatePostForm(request.POST or None, request.FILES or None, user=request.user)
    if request.method == 'POST':
        if form.is_valid():
            post = form.instance
            post.author = request.user
            post.save()
            return redirect("/files/1")
    return render(request, "post/form.html", {
        "form": form
    })


@login_required
def uploaded_files(request, page_id):
    form = SearchForm(request.GET or None)
    query = ""
    if "q" in form.data and form.data['q'] and form.is_valid():
        results = form.search()
        query += "?q=" + form.data['q']
        files = [i.pk for i in results]
        files = Post.objects.filter(pk__in=files).order_by('-date')
    else:
        files = Post.objects.all().order_by('-date')
    pages = Paginator(files, 10)
    try:
        files = pages.page(page_id)
    except EmptyPage:
        files = pages.page(pages.num_pages)
    return render(request, "post/posts.html", {
        "files": files,
        "query": query
    })


@login_required
def download_file(request, slug):
    post = get_object_or_404(Post, slug=slug)
    mime = magic.Magic(mime=True)
    response = HttpResponse(post.file, content_type=mime.from_file(post.file.path))
    response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(post.filename)
    return response


@login_required
def delete_file(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if post.author == request.user:
        post.delete()
        return redirect("/files/1")


@login_required
def edit_file(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if post.author == request.user:
        form = CreatePostForm(request.POST or None, request.FILES or None, instance=post, user=request.user)
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                return redirect("/files/1")
        return render(request, "post/edit.html", {
            "form": form
        })
    else:
        return HttpResponseForbidden()