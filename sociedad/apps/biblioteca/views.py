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
from sociedad.apps.biblioteca.models import *
from sociedad.apps.biblioteca.forms import *
from sociedad.apps.principal.views import *
from sociedad.apps.blog.views import *
import time
import os

def comentar(request, pk):
    p = request.POST

    if 'mensaje' in p:
        autor = "Anonimo"
        if p["autor"]: autor = p["autor"]
        com = Comentariolib(requerir=Libro.objects.get(pk=int(pk)))
        cf = FormularioComentario(p, instance=com)
        cf.fields["autor"].required = False

        com = cf.save(commit=False)
        com.autor = autor
        com.save()
    return HttpResponseRedirect(reverse("sociedad.apps.biblioteca.views.libro", args=[pk]))

def mkmonth_lst():
    if not Libro.objects.count(): return[]

    year, month = time.localtime()[:2]
    first = Libro.objects.order_by("fecha_subida")[0]
    fyear = first.fecha_subida.year
    fmonth = first.fecha_subida.month
    months = []

    for y in range(year,fyear-1,-1):
        start,end = 12,0
        if y == year:start = month
        if y == fyear: end = fmonth -1

        for m in range(start,end,-1):
            months.append((y,m,month_name[m]))
    return months

def month(request,year,month):
    libro = Libro.objects.filter(fecha__year=year,fecha__month=month)
    return render_to_response("biblioteca.html",dict(libro_list=libro,user=request.user,month=mkmonth_lst(),archive=True))

def libro(request, pk):
    idlibro = Libro.objects.get(pk=int(pk))
    comentaro = Comentariolib.objects.filter(requerir = idlibro)
    if request.user.is_authenticated():
        d = dict(libro= idlibro,comentaro = comentaro,form=FormularioComentario(),entrada_b=blog_pr(request),usuario=request.user, dato = filtro(request), cate=categorias(request))
    else:
        d = dict(libro= idlibro,comentaro = comentaro,form=FormularioComentario(),entrada_b=blog_pr(request),usuario=request.user, cate=categorias(request))
    d.update(csrf(request))
    return render_to_response("libro.html",d,context_instance = RequestContext(request))

def blog_pr(request):
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

def biblioteca(request):

    libro = Libro.objects.all().order_by("-titulo")
    paginator = Paginator(libro,6)
    try: 
    	pagina = int(request.GET.get("page",'1'))
    except ValueError: 
    	pagina = 1

    try:
        libro = paginator.page(pagina)
    except (InvalidPage, EmptyPage):
        libro = paginator.page(paginator.num_pages)
    if request.user.is_authenticated():
        d=dict( libro = libro, usuario=request.user, libro_list = libro.object_list,cate=categorias(request), months = mkmonth_lst(), dato = filtro(request), entrada_b=blog_p(request))
    else:
        d=dict( libro = libro, cate=categorias(request), usuario=request.user,entrada_b=blog_pr(request), libro_list = libro.object_list, months = mkmonth_lst())
    
    return render_to_response("biblioteca.html",d,context_instance = RequestContext(request))

@login_required(login_url='/')
def new_libro(request):
    if request.method == 'POST':
        libros=FormularioLibro(request.POST, request.FILES)
        print libros
        if libros.is_valid():
            libros.user1=request.user
            libros.save()
            return HttpResponseRedirect("/biblioteca")
    else: 
        print request.POST
    libros=FormularioLibro()
    return render_to_response('new_libro.html', {'libro':libros,'dato':filtro(request), 'cate':categorias(request)} ,context_instance=RequestContext(request))

@login_required(login_url='/')
def categoria(request):
    cat=Categoria.objects.all().order_by('tipo')
    if request.method == 'POST':
        cat_lib=FormularioCategoria(request.POST)
        print cat_lib
        if cat_lib.is_valid():
            cat_lib.save()
            return HttpResponseRedirect("/categoria")
    else: 
        print request.POST
    cat_lib=FormularioCategoria()
    return render_to_response('categoria.html', {'categoria':cat_lib,'categorias':cat, 'dato':filtro(request), 'cate':categorias(request)} ,context_instance=RequestContext(request))

@login_required(login_url='/')
def ver_lib_cat(request,pk):
    titulo=Categoria.objects.get(pk=int(pk))
    listaLibCat = Libro.objects.filter(requerir=Categoria.objects.get(pk=int(pk)))
    if request.user.is_authenticated():
        d=dict(categorias=listaLibCat, titulo_cat=titulo,dato=filtro(request),cate=categorias(request))
    else:
        d=dict(categorias=listaLibCat, titulo_cat=titulo,cate=categorias(request))
    return render_to_response('lista_por_categoria.html',d,context_instance=RequestContext(request))

def buscarlibro(request):
    if request.method=='POST':
        form=buscarForm(request.POST)
        if form.is_valid():
            criterio=request.POST["buscar"]
            lista=list(Libro.objects.filter(Q(titulo__contains=criterio)|Q(descripcion__contains=criterio)))
        if request.user.is_authenticated():
            return render_to_response("resultado.html",{'lista':lista, 'dato':filtro(request),'cate':categorias(request),'entrada_b':blog_p(request)},context_instance=RequestContext(request))
        else:
            return render_to_response("resultado.html",{'lista':lista, 'cate':categorias(request),'entrada_b':blog_p(request)},context_instance=RequestContext(request))
    form=buscarForm()
    if request.user.is_authenticated():
        return render_to_response('buscarLibro.html',{'form':form, 'dato':filtro(request),'cate':categorias(request),'entrada_b':blog_p(request)},context_instance=RequestContext(request))
    else:
        return render_to_response('buscarLibro.html',{'form':form, 'cate':categorias(request),'entrada_b':blog_p(request)},context_instance=RequestContext(request))

@login_required(login_url='/')
def mislibros(request):
    mislibros = Libro.objects.filter(user1=request.user)
    return render_to_response('mislibros.html', {'mislibros':mislibros,'dato':filtro(request), 'cate':categorias(request),'entrada_b':blog_p(request)}, context_instance=RequestContext(request))

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

def categorias(request):
    cat=Categoria.objects.all()
    return cat
#===============fin datos================#


