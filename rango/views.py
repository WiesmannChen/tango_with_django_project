from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from rango.models import Category
from rango.models import Page
from django.http import HttpResponse


def index(request):
    # query the database for a list

    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]

    context_dict = {}
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['categories'] = category_list
    context_dict['pages'] = page_list

    # return the response and send it back
    return render(request, 'rango/index.html', context=context_dict)


def about(request):
    context_dict = {'boldmessage': 'This tutorial has been put together by Qisen'}

    return render(request, 'rango/about.html', context=context_dict)
    # return HttpResponse("Rango says here is the about page. <a href='/rango/'>Index</a>")


def show_category(request, category_name_slug):
    # Create a context dictionary which we can
    # pass to the template rendering engine
    context_dict = {}

    try:
        # The get() method returns one model instance
        # or raises an exception
        category = Category.objects.get(slug=category_name_slug)

        # The filter() will returns a list of page
        # or an empty list
        pages = Page.objects.filter(category=category)

        # Adds our results list to the template context
        # under name pages
        context_dict['pages'] = pages
        context_dict['category'] = category
    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['pages'] = None

    return render(request, 'rango/category.html', context=context_dict)
