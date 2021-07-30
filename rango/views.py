from django.contrib.auth.decorators import login_required

# Create your views here.

from django.shortcuts import render
from django.urls import reverse

from rango.models import Category
from rango.models import Page
from django.http import HttpResponse
from rango.forms import CategoryForm
from rango.forms import PageForm
from django.shortcuts import redirect

# for register
from rango.forms import UserForm,UserProfileForm

# for login in
from django.contrib.auth import authenticate, login, logout


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

@login_required()
def add_category(request):
    form = CategoryForm()

    # A http post
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        # Have we been provide with a valid form?
        if form.is_valid():
            # Save the new category to the database
            form.save(commit=True)

            # Confirm the category
            return redirect(reverse('rango:index'))
        else:
            # The supplied form contained erros
            # Just print them to then terminal
            print(form.errors)

    # will handle the bad form, new form, or no form supplied cases
    # Render the form with error messages (if any)
    return render(request,'rango/add_category.html',{'form':form})

@login_required()
def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except:
        category = None

    # You cannot add a page to a Category that does not exist... DM
    if category is None:
        return redirect(reverse('rango:index'))

    form = PageForm()

    if request.method == 'POST':
        form = PageForm(request.POST)

        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()

                return redirect(reverse('rango:show_category',
                                        kwargs={'category_name_slug': category_name_slug}))
        else:
            print(form.errors)

    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context=context_dict)

def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()

            registered = True
        else:
            print(user_form.errors,profile_form.errors)
    else:
        # Not a HTTP POST
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request,
                  'rango/register.html',
                  context={'user_form':user_form,
                           'profile_form':profile_form,
                           'registered':registered})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('rango:index'))
            else:
                return HttpResponse("Your Rango account is disabled.")
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'rango/login.html')


@login_required
def restricted(request):
    return render(request, 'rango/restricted.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('rango:index'))