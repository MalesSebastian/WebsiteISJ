# Copyright 2017 Adrian-Ioan Garovat, Emanuel Covaci, Sebastian-Valeriu Males
#
# This file is part of WebsiteISJ
#
# WebsiteISJ is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# WebsiteISJ is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with WebsiteISJ.   If not, see <http://www.gnu.org/licenses/>.
import json

from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.core.paginator import Paginator
from django.http.response import HttpResponse
from django.http.response import HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.utils.html import escape

from gallery.models import GalleryPhoto
from models import Gallery
from utility.utility import clean_file


def gallery(request):
    images = Gallery.objects.order_by("-date")
    paginator = Paginator(images, 6)

    page = request.GET.get('page')
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        images = paginator.page(1)
    except EmptyPage:
        images = paginator.page(paginator.num_pages)

    index = images.number - 1
    max_index = len(paginator.page_range)
    start_index = index - 3 if index >= 3 else 0
    end_index = index + 3 if index <= max_index - 3 else max_index
    page_range = list(paginator.page_range)[start_index:end_index]

    return render(request, 'gallery/gallery.html', {
        'gallery': images,
        'page_range': page_range
    })


@staff_member_required
def remove_gallery_photo(request):
    if request.method == "POST":
        photo = get_object_or_404(GalleryPhoto, id=request.POST["id"])
        photo.delete()
        return HttpResponse()
    else:
        return HttpResponseForbidden()


@staff_member_required
def add_gallery(request):
    if request.method == "POST":
        json_dict = {}
        if request.POST["name"] == "":
            json_dict["name"] = "This field is required."
        file = None
        if request.FILES.get("file"):
            file = request.FILES["file"]

        if request.POST["change"] == "0" and not file:
            json_dict["file"] = "This field is required. Please select a file."

        elif request.POST["change"] == "0" and clean_file(
                file, image=True) != "":
            json_dict["file"] = clean_file(file, image=True)

        for i in range(0, int(request.POST["nr"])):
            file = None
            if request.FILES.get("form-" + str(i) + "-file"):
                file = request.FILES["form-" + str(i) + "-file"]

            if file:
                error = clean_file(file, image=True)
                if error != "":
                    json_dict[i] = error

        if json_dict != {}:
            response = HttpResponse(json.dumps(json_dict),
                                    content_type='application/json')
            response.status_code = 400
            return response

        if request.POST["change"] == "1":
            obj = get_object_or_404(Gallery, id=request.POST["id"])
            obj.name = escape(request.POST["name"])
            if request.FILES.get("file"):
                obj.file = request.FILES["file"]
            obj.save()

            for i in range(0, int(request.POST["delete_nr"])):
                id = int(request.POST["delete-" + str(i) + "-id"])
                photo = GalleryPhoto.objects.get(pk=id)
                photo.delete()
        else:
            obj = Gallery(name=escape(request.POST["name"]),
                          file=request.FILES["file"], author=request.user)
            obj.save()

        for i in range(0, int(request.POST["nr"])):
            id = None
            if request.POST.get("form-" + str(i) + "-id"):
                id = request.POST["form-" + str(i) + "-id"]

            file = None
            if request.FILES.get("form-" + str(i) + "-file"):
                file = request.FILES["form-" + str(i) + "-file"]

            name = request.POST["form-" + str(i) + "-name"]
            if not id:
                photo = GalleryPhoto(gallery=obj, name=name, file=file,
                                     author=request.user,
                                     location="gallery/" + str(obj.slug))
                photo.save()
            else:
                photo = GalleryPhoto.objects.get(pk=id)
                photo.name = name
                photo.save()
        return redirect("/admin/gallery/gallery/")

    else:
        return HttpResponseForbidden()


def gallery_img(request, slug):
    instance = Gallery.objects.get(slug=slug)
    photos = GalleryPhoto.objects.filter(gallery=instance).extra(
        select={'order': 'CAST(name AS INTEGER)'}
    ).order_by('order')
    return render(request, 'gallery/imagini.html', {
        'photos': photos,
        'album_name': instance.name,
    })
