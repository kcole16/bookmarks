from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from bookmarks.models import List
from bookmarks.models import Link
from bookmarks.models import User
from bookmarks.forms import ListForm
from bookmarks.forms import LinkForm
from bookmarks.forms import UserForm
from bookmarks.forms import DeleteForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse


def encode_url(str):
    return str.replace(' ', '_')

def decode_url(str):
    return str.replace('_', ' ')


def index(request): 
	context = RequestContext(request)
	list_order = List.objects.order_by('name')
	context_dict = {'lists': list_order}

	for lists in list_order:
		lists.url = lists.name #.replace(' ', '_')

	return render_to_response('bookmarks/index.html', context_dict, context)

def list(request, list_name_url):
	context = RequestContext(request)
	list_name = list_name_url #.replace('_',' ')
	context_dict = {'list_name': list_name, 'list_name_url':list_name_url}

	try:
		lists = List.objects.get(name=list_name)
		links = Link.objects.filter(lists=lists)
		context_dict['lists'] = lists
		context_dict['links'] = links
	except List.DoesNotExist:
		pass

	return render_to_response('bookmarks/list.html', context_dict, context)

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

def delete_link(request, link_id):
    link_to_delete = get_object_or_404(Link, id=link_id)
    context_dict = {'link+id': link_id}

    if request.method == 'POST':
        form = DeleteForm(request.POST, instance=link_to_delete)

        if form.is_valid():
            link_to_delete.delete()
            return HttpResponseRedirect('bookmarks/list')
    else:
        form = DeleteForm(instance = link_to_delete)
    template_vars = {'form': form}
    return render_to_response(request, 'bookmarks/delete_link.html', template_vars)







