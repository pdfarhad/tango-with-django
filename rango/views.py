from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response, render
from .models import Category, Page
from .forms import CategoryForm, UserForm, UserProfileForm
from django.contrib.auth.decorators import login_required
from datetime import datetime

def user_logout(request):
    logout(request)

    return HttpResponseRedirect('/rango/')


@login_required()
def restricted(request):
    return HttpResponse("Since you're logged in, you can see the text!")


def user_login(request):
    context = RequestContext(request)

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username= username, password=password)

        if user is not None:
            if user.is_active:

                login(request, user)
                return HttpResponseRedirect('/rango/')
            else:
                return HttpResponse('Your Rango account is disabled')

        else:
            print("Invalid Login details:{}, {}".format(username, password))

            return HttpResponse("Invalid Login details supplied")

    else:
        return render(request, 'rango/login.html', {}, context)


@csrf_protect
def add_category(request):

    context = RequestContext(request)
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save(commit=True)

            return index(request)
        else:
            print(form.errors)

    else:
        form = CategoryForm()

    return render(request, 'rango/add_category.html', {'form': form}, context)


    # return render_to_response('rango/add_category.html', {'form': form}, context)

@csrf_protect
def register(request):
    context = RequestContext(request)
    if request.session.set_test_cookie():
        print("Test Cookie Worked! ")
        request.session.delete_test_cookie()
    registered = False

    if request.method == 'POST':

        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

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
            print(user_form.errors, profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'rango/register.html',
                  {'user_form': user_form, 'profile_form':profile_form,
                   'registered': registered},
                  context)


def index(request):
    context = RequestContext(request)
    request.session.set_test_cookie()

    category_list = Category.objects.all()#order_by('-likes')[:5]
    context_dict = {'categories': category_list}
    for category in category_list:
        category.url = category.name.replace(' ', '_')

    response =  render(request, 'rango/index.html', context_dict, context)

    visits = int(request.COOKIES.get('visits', '0'))

    if 'last_visit' in request.COOKIES.keys():
        last_visit = request.COOKIES['last_visit']

        last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")

        if (datetime.now() - last_visit_time).days > 0:
            response.set_cookie('visits', visits+1)

            response.set_cookie('last_visit', datetime.now())

    else:
        response.set_cookie('last_visit', datetime.now())

    return response


def about(request):
    context = RequestContext(request)
    context_dict = {'boldmessage':"About"}

    return render(request, 'rango/about.html', context_dict, context)


def category(request, category_name_url):

    context = RequestContext(request)
    category_name = category_name_url.replace('_', ' ')
    context_dict = {'category_name': category_name}

    try:
        category = Category.objects.get(name=category_name)
        pages = Page.objects.filter(category=category)

        context_dict['pages'] = pages
        context_dict['category'] = category
    except Category.DoesNotExist:
        pass

    return render(request, 'rango/category.html', context_dict, context)