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
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.shortcuts import render

from models import Article
from models import Category
from models import SimplePage
from models import Subcategory


def category(request, slug):
    category_name = get_object_or_404(Category, slug=slug)
    subcat = Subcategory.objects.all().filter(category=category_name)
    simple_page = SimplePage.objects.all().filter(category=category_name)
    return render(request, 'page/category.html',
                  {
                      'name': category_name,
                      'subcategories': subcat,
                      'simple_pages': simple_page,
                  })


def category_all(request):
    categories = Category.objects.all().order_by("order")
    return render(request, 'page/category_all.html',
                  {
                      'categories_all': categories,
                  })


def subcategory_article(request, name, slug):
    article = list(
        Article.objects.values('name', 'text', 'subcategory', 'file', 'date',
                               'slug').filter(slug=slug,
                                              subcategory=name))
    return render(request, 'subject/subject_news.html', {

        'name': article[0].get('name'),
        'text': article[0].get('text'),
        'thumbnail': "/media/" + article[0].get('file'),

    })


def subcategory(request, slug):
    subcat = get_object_or_404(Subcategory, slug_sub=slug)
    articles = Article.objects.all().filter(subcategory=subcat)
    paginator = Paginator(articles, 4)

    page = request.GET.get('page')
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)

    index = articles.number - 1
    max_index = len(paginator.page_range)
    start_index = index - 3 if index >= 3 else 0
    end_index = index + 3 if index <= max_index - 3 else max_index
    page_range = list(paginator.page_range)[start_index:end_index]

    return render(request, 'page/subcategory.html',
                  {'name': subcat.name,
                   'articole': articles,
                   'page_range': page_range
                   })


def article_post(request, slug):
    article = list(
        Article.objects.values('subcategory', 'name', 'text', 'file',
                               'date').filter(slug=slug))
    return render(request, 'page/article.html', {

        'name': article[0].get('name'),
        'text': article[0].get('text'),
        'date': article[0].get('date'),
        'thumbnail': "/media/" + article[0].get('file'),

    })


def simple_page_article(request, slug):
    article = list(
        SimplePage.objects.values('category', 'name', 'text', 'file',
                                  'date').filter(slug=slug))
    return render(request, 'page/article.html', {

        'name': article[0].get('name'),
        'text': article[0].get('text'),
        'date': article[0].get('date'),
        'thumbnail': "/media/" + article[0].get('file'),

    })
