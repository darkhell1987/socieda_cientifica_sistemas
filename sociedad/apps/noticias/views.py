from django.shortcuts import render, render_to_response, HttpResponseRedirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth.models import User
from sociedad.settings import RUTA_PROYECTO
from django.core.context_processors import csrf
from django.http import HttpResponseRedirect
from django.forms import ModelForm
from django.db.models import Q
from datetime import datetime
from calendar import month_name
from sociedad.apps.noticias.models import *
from sociedad.apps.noticias.forms import *
from sociedad.apps.principal.views import *
from sociedad.apps.biblioteca.views import *
from sociedad.apps.blog.views import *
import time
import os

def poncomentarionoticia(request, pk):
    p = request.POST
    if 'mensaje' in p:
        autor = "Anonimo"
        if p["autor"]: autor = p["autor"]
        comentario = ComentarNoticia(requerir=Noticia.objects.get(pk=int(pk)))
        cf = FormularioComentario(p, instance=comentario)
        cf.fields["autor"].required = False

        comentario = cf.save(commit=False)
        comentario.autor = autor
        comentario.save()
    return HttpResponseRedirect(reverse("sociedad.apps.noticias.views.nentrada", args=[pk]))

def nentrada(request, pk):
    idnoticia = Noticia.objects.get(pk=int(pk))
    comentario = ComentarNoticia.objects.filter(requerir = idnoticia)
    if request.user.is_authenticated():
        d = dict(entrada= idnoticia,comentario = comentario,form=FormularioComentario(),usuario=request.user,dato=filtro(request),cate=categ(request),entrada_b=blog_p(request))
    else:
        d = dict(entrada= idnoticia,comentario = comentario,form=FormularioComentario(),usuario=request.user,cate=categ(request),entrada_b=blog_p(request))
    d.update(csrf(request))
    return render_to_response("nentrada.html",d,context_instance = RequestContext(request))


def noticia(request):
    noticia = Noticia.objects.all().order_by("-fecha_entrada")
    paginator = Paginator(noticia,5)
    try: 
    	pagina = int(request.GET.get("page",'1'))
    except ValueError: 
    	pagina = 1

    try:
        noticia = paginator.page(pagina)
    except (InvalidPage, EmptyPage):
        noticia = paginator.page(paginator.num_pages)

    if request.user.is_authenticated():
        d=dict( noticia = noticia, usuario=request.user, noticia_list = noticia.object_list,dato=filtro(request),cate=categ(request),entrada_b=blog_p(request))
    else:
        d=dict( noticia = noticia, usuario=request.user, noticia_list = noticia.object_list,cate=categ(request),entrada_b=blog_p(request))
    return render_to_response("noticia.html",d,context_instance = RequestContext(request))

@login_required(login_url='/')
def entrada_noticia(request):
    if request.method == 'POST':
        noticias=FormularioNoticia(request.POST, request.FILES)
        print noticias
        if noticias.is_valid():
            noticias.save()
            return HttpResponseRedirect("/noticia")
    else:
        print request.POST
        noticias=FormularioNoticia()
    return render_to_response('entrada-noticia.html',{"noticias":noticias,'dato':filtro(request),'cate':categ(request),'entrada_b':blog_p(request)},context_instance=RequestContext(request))


#================datos=============#
def filtro(request):
    usuario=request.user
    m = User.objects.get(username=usuario)
    #request.session['id']=m.id
    perfils = Perfil.objects.get(usuario=User.objects.get(pk=int(m.id)))
    return perfils

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

def categ(request):
    cat=Categoria.objects.all()
    return cat
#===============fin datos================#
