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
from sociedad.apps.blog.models import *
from sociedad.apps.blog.forms import *
from sociedad.apps.principal.views import *
from sociedad.apps.biblioteca.views import *
import time
import os

def poncomentario(request, pk):
    m = Votacion()
    m.date = datetime.now()
    m.rvoto = Entrada.objects.get(pk=int(pk))
    m.uvoto = request.user
    m.save()
    if request.method == 'GET':
        print 'GET mostro.'
    elif request.method == 'POST':
        print 'POST oculto.'
    else:
        print '..'
    p = request.POST
    if 'mensaje' in p:
        autor = "Anonimo"
        if p["autor"]: autor = p["autor"]
        comentario = Comentario(requerir=Entrada.objects.get(pk=int(pk)))
        cf = FormularioComentario(p, instance=comentario)
        cf.fields["autor"].required = False

        comentario = cf.save(commit=False)
        comentario.autor = autor
        comentario.save()
    return HttpResponseRedirect(reverse("sociedad.apps.blog.views.entrada", args=[pk]))

def mkmonth_lst():
    if not Entrada.objects.count(): return[]

    year, month = time.localtime()[:2]
    first = Entrada.objects.order_by("fecha_entrada")[0]
    fyear = first.fecha_entrada.year
    fmonth = first.fecha_entrada.month
    months = []

    for y in range(year,fyear-1,-1):
        start,end = 12,0
        if y == year:start = month
        if y == fyear: end = fmonth -1

        for m in range(start,end,-1):
            months.append((y,m,month_name[m]))
    return months

def month(request,year,month):
    entrada = Entrada.objects.filter(fecha__year=year,fecha__month=month)
    return render_to_response("blog.html",dict(entrada_list=entrada,user=request.user,month=mkmonth_lst(),archive=True))

def entrada(request, pk):
    identrada = Entrada.objects.get(pk=int(pk))
    comentario = Comentario.objects.filter(requerir = identrada)
    if request.user.is_authenticated():
        d = dict(entrada= identrada,comentario = comentario,form=FormularioComentario(),usuario=request.user,dato=filtro(request),cate=categ(request),entrada_b=blog_p(request))
    else:
        d = dict(entrada= identrada,comentario = comentario,form=FormularioComentario(),usuario=request.user,cate=categ(request),entrada_b=blog_p(request))
    d.update(csrf(request))
    return render_to_response("entrada.html",d,context_instance = RequestContext(request))


def blog(request):
    entrada = Entrada.objects.all().order_by("-fecha_entrada")
    paginator = Paginator(entrada,5)
    try: 
    	pagina = int(request.GET.get("page",'1'))
    except ValueError: 
    	pagina = 1

    try:
        entrada = paginator.page(pagina)
    except (InvalidPage, EmptyPage):
        entrada = paginator.page(paginator.num_pages)

    if request.user.is_authenticated():
        d=dict( entrada = entrada, usuario=request.user, entrada_list = entrada.object_list, months = mkmonth_lst(),dato=filtro(request),cate=categ(request),entrada_b=blog_p(request))
    else:
        d=dict( entrada = entrada, usuario=request.user, entrada_list = entrada.object_list, months = mkmonth_lst(),cate=categ(request),entrada_b=blog_p(request))
    return render_to_response("blog.html",d,context_instance = RequestContext(request))

@login_required(login_url='/')
def perfil(request):
    return render_to_response("perfil.html",{'dato':filtro(request),'medalla':medallas(request), 'cate':categ(request),'entrada_b':blog_p(request)},context_instance = RequestContext(request)) 

def medallas(request):
    medalla='alfa'
    mislibros = Libro.objects.filter(user1=request.user).count()
    if mislibros<10:
        return medalla
    else:
        if mislibros<20:
            medalla='beta'
            return medalla
        else:
            if mislibros<30:
                medalla='gama'
                return medalla
            else:
                medalla='delta'
                return medalla
    return medalla

@login_required(login_url='/')
def entrada_blog(request):
    if request.method == 'POST':
        entradas=FormularioEntrada(request.POST, request.FILES)
        print entradas
        if entradas.is_valid():
            entradas.save()
            return HttpResponseRedirect("/blog")
    else:
        print request.POST
        entradas=FormularioEntrada()
    return render_to_response('entrada-blog.html',{"entradas":entradas,'dato':filtro(request),'cate':categ(request),'entrada_b':blog_p(request)},context_instance=RequestContext(request))

@login_required(login_url='/')
def mispublicacion(request):
    mispublicaciones = Entrada.objects.filter(usuario=request.user)
    return render_to_response('mispublicaciones.html', {'mispublicaiones':mispublicaciones,'dato':filtro(request), 'cate':categ(request),'entrada_b':blog_p(request)}, context_instance=RequestContext(request))


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

def imagenes(request):
    img=Entrada.objects.all()
    return render_to_response('imagenes.html',{'img':img},context_instance=RequestContext(request))


from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template.response import TemplateResponse
import urllib2
from datetime import datetime

def temp_page( request):
    if 'q' in request.GET:
        print request.GET['q']
        voto = Votacion.objects.get(id=1)
        total = voto.total_point + int(request.GET['q'])
        print 'Total: ', total
        voto.total_point = total
        voto.total_vote += 1
        voto.save()
        m = 'Input: %r' % request.GET['q']
    else:
        m = 'I dont know what it is'
    return HttpResponse( "The current average is %.2f" % voted_meal.average_point())
