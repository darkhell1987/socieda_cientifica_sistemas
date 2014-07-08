from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404,render,HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.forms import AdminPasswordChangeForm, AuthenticationForm, authenticate, UserCreationForm
from django.contrib.auth import login, authenticate, logout
from sociedad.apps.principal.form import *
from django.contrib.auth.models import User
from sociedad.settings import RUTA_PROYECTO
from django.db.models import Q
import os
from datetime import datetime
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
import time
from django.forms import ModelForm
from django.core.context_processors import csrf
from django.contrib.sessions.models import Session
from sociedad.apps.blog.models import *
from sociedad.apps.principal.models import *
from sociedad.apps.biblioteca.views import *
import json
from django.core.paginator import Paginator, InvalidPage, EmptyPage

def index(request):
	if not request.user.is_anonymous():
		return HttpResponseRedirect('/privado')
	if request.method == 'POST':
		formulario = AuthenticationForm(request.POST)
		if formulario.is_valid:
			usuario = request.POST['username']
			clave = request.POST['password']
			acceso = authenticate(username=usuario, password=clave)
			if acceso is not None:
				if acceso.is_active:
					login(request, acceso)
					return render_to_response('base.html',{'entrada_b':blog_p(request),'dato':filtro(request), 'cate':categorias(request)},context_instance=RequestContext(request))
				else:
					return render_to_response ('user/noactivo.html',context_instance = RequestContext(request))
			else:
				return render_to_response ('user/nousuario.html',context_instance = RequestContext(request))
	else:
		formulario = AuthenticationForm()
	return render_to_response('base.html',{'logeo':formulario, 'entrada_b':blog_p(request), 'cate':categorias(request)},context_instance=RequestContext(request))

def verificar(request):
	if request.method=='POST':
		usuario=request.POST['username']
		try:
			u=User.objects.get(username=usuario)
			return HttpResponse("El usuario ya existe")
		except User.DoesNotExist:
			return HttpResponse("Puede usar ese nombre")
	else:
		return HttpResponse()

def cerrar(request):
	logout(request)
	return HttpResponseRedirect('/')

def privado(request) :
	if request.user.is_authenticated():
		usuario=request.user
		if  usuario.is_active:
			return render_to_response('privado.html',{'dato':filtro(request),'entrada_b':blog_p(request),'cate':categorias(request)} , context_instance=RequestContext(request))
		else:
			return HttpResponseRedirect("/")
	else:
		return HttpResponseRedirect("/")	

def cambiar_pass(request):
	if request.method == 'POST' :
		formulario = AdminPasswordChangeForm(user=request.user, data=request.POST)
		if formulario.is_valid():
			formulario.save()
			return HttpResponseRedirect('/login')
	else:
		formulario = AdminPasswordChangeForm(user=request.user)
	return  render_to_response('cambiar_clave.html', {'formulario' :formulario}, context_instance=RequestContext(request))

def registro(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			usuario = form.save()
			return HttpResponseRedirect("/completar/"+str(usuario.id)+"/")
	else:
		form = UserCreationForm()
	return render_to_response('registro.html', {'form':form,'entrada_b':blog_p(request),'cate':categorias(request)}, context_instance=RequestContext(request))

def completar(request, user_id):
	if not request.user.is_anonymous():
		return HttpResponseRedirect('/privado')
	user = User.objects.get(pk=user_id)
	if request.method == 'POST' :
		formularioperfil = PerfilForm(request.POST, request.FILES)
		formulariousuario = UsuarioForm(request.POST, request.FILES)
		if formularioperfil.is_valid() and formulariousuario.is_valid():
			perfil = formularioperfil.save()
			perfil.usuario_id = user_id
			perfil.save()
			user.first_name = formulariousuario.cleaned_data['first_name']
			user.last_name = formulariousuario.cleaned_data['last_name']
			user.email = formulariousuario.cleaned_data['email']
			user.save()
			return HttpResponseRedirect("/")
	else:
		formularioperfil = PerfilForm()
		formulariousuario = UsuarioForm()
	return render_to_response('completar.html', {'formularioperfil':formularioperfil, 'formulariousuario':formulariousuario,'entrada_b':blog_p(request),'cate':categorias(request)}, context_instance=RequestContext(request))

def blog_p(request):
    entrada = Entrada.objects.all().order_by("-fecha_entrada")
    paginator = Paginator(entrada,3)
    try: 
    	pagina = int(request.GET.get("page",'1'))
    except ValueError: 
    	pagina = 1

    try:
        entrada = paginator.page(pagina)
    except (InvalidPage, EmptyPage):
        entrada = paginator.page(paginator.num_pages)
    
    return entrada

def filtro(request):
	usuario=request.user
	m = User.objects.get(username=usuario)
	#request.session['id']=m.id
	if m.first_name == "":
		return render_to_response('completar.html',{'pk':request.user},context_instance=RequestContext(request))
	perfils = Perfil.objects.get(usuario=User.objects.get(pk=int(m.id)))
	return perfils