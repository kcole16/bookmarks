from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from bookmarks.models import List, Link, User
from bookmarks.forms import ListForm, LinkForm, UserForm, DeleteForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required


def encode_url(str):
    return str.replace(' ', '_')

def decode_url(str):
    return str.replace('_', ' ')

@login_required
def restricted(request):
    return HttpResponse("You can see this file if logged in")

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/bookmarks/')


def index(request): 
    context = RequestContext(request)
    list_order = List.objects.order_by('name')
    context_dict = {'lists': list_order}
    
    for lists in list_order:
      #  lists.url = lists.name
        name = lists.name
    
    list_to_get = List.objects.get(name=name)
    links = Link.objects.filter(lists=list_to_get)

    context_dict['links'] = links

    return render_to_response('bookmarks/index.html', context_dict, context)

def list(request, list_name_url):
	context = RequestContext(request)
	list_name = list_name_url 
	context_dict = {'list_name': list_name, 'list_name_url':list_name_url}

	try:
		lists = List.objects.get(name=list_name)
		links = Link.objects.filter(lists=lists)
		context_dict['lists'] = lists
		context_dict['links'] = links
	except List.DoesNotExist:
		pass

	return render_to_response('bookmarks/list.html', context_dict, context)

@login_required
def add_list(request):
    context = RequestContext(request)
    if request.method == 'POST':
        form = ListForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
            print form.errors
    else:
        form = ListForm()
    return render_to_response('bookmarks/add_list.html', {'form': form}, context)


@login_required
def add_link(request, list_name_url):
    context = RequestContext(request)
    list_name = decode_url(list_name_url)
    if request.method == 'POST':
        form = LinkForm(request.POST)

        if form.is_valid():
            link = form.save(commit=False)

            try:
                lis = List.objects.get(name=list_name)
                link.lists = lis
            except List.DoesNotExist:
                return render_to_response('bookmarks/add_link.html', {}, context)

            link.save()
            return list(request, list_name_url)
        else:
            print form.errors
    else:
        form = LinkForm()
    return render_to_response( 'bookmarks/add_link.html',
            {'list_name_url': list_name_url,
             'list_name': list_name, 'form': form},
             context)

def register(request):
    context = RequestContext(request)
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)

        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            registered = True

        else:
            print user_form.errors
    else:
        user_form = UserForm()

    return render_to_response(
        'bookmarks/register.html',
        {'user_form': user_form, 'registered': registered},
        context)

def user_login(request):
    context = RequestContext(request)

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/bookmarks/')
            else:
                return HttpResponse("Your account is inactive.")
        else:
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    else:
        return render_to_response('bookmarks/login.html', {}, context)

@login_required
def delete_link(request, link_id):
    link_to_delete = get_object_or_404(Link, id=link_id)
    context = RequestContext(request)
    link_to_delete.delete()
    return HttpResponseRedirect('/bookmarks/')

@login_required
def delete_list(request, list_id):
    list_to_delete = get_object_or_404(List, id=list_id)
    context = RequestContext(request)
    list_to_delete.delete()
    return HttpResponseRedirect('/bookmarks')









