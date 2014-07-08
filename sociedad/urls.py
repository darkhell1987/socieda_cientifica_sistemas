from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
from sociedad.apps.principal.views import *
from sociedad.apps.blog.views import *
from sociedad.apps.biblioteca.views import *
from sociedad.apps.noticias.views import *
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'sociedad.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^archivos/(?P<path>.*)$', 'django.views.static.serve', {'document_root':settings.MEDIA_ROOT,}),

    #parte del principal
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', index),
    url(r'^index/$', index),
    url(r'^registro/$',registro),
    url(r'^cerrar/$', cerrar),
    url(r'^privado/$', privado),
    url(r'^completar/(?P<user_id>\d+)/$', 'sociedad.apps.principal.views.completar'),    
    url(r'^verificar/$', verificar),

    #Parte del blog
	url(r'^blog/$', blog),
    url(r"^blog/(\d+)/(\d+)/$","sociedad.apps.blog.views.month"),
    url(r'^entrada/(?P<pk>\d+)/$','sociedad.apps.blog.views.entrada'),
    url(r"^poncomentario/(\d+)/$","sociedad.apps.blog.views.poncomentario"),

    #Biblioteca
    url(r'^biblioteca/$', biblioteca),
    url(r"^biblioteca/(\d+)/(\d+)/$","sociedad.apps.biblioteca.views.month"),
    url(r'^libro/(?P<pk>\d+)/$','sociedad.apps.biblioteca.views.libro'),
    url(r"^comentar/(\d+)/$","sociedad.apps.biblioteca.views.comentar"),
    url(r"^buscar/$","sociedad.apps.biblioteca.views.buscarlibro"),

    #Para perfil
    url(r'^perfil/$', perfil),
    url(r'^entrada-blog/$', entrada_blog),
    url(r"^new_libro/$","sociedad.apps.biblioteca.views.new_libro"),
    url(r"^categoria/$","sociedad.apps.biblioteca.views.categoria"),
    url(r'^lista_por_categoria/(?P<pk>\d+)/$','sociedad.apps.biblioteca.views.ver_lib_cat'),
    url(r'^mislibros/$','sociedad.apps.biblioteca.views.mislibros'),
    url(r'^imagenes/$','sociedad.apps.blog.views.imagenes'),
    url(r'^mispublicaion/$','sociedad.apps.blog.views.mispublicacion'),
    url(r'^entrada_noticia/$','sociedad.apps.noticias.views.entrada_noticia'),

    #Para Noticias
    url(r'^noticia/$',noticia),
    url(r'^noticia/(?P<pk>\d+)/$','sociedad.apps.noticias.views.nentrada'),
    url(r"^poncomentarionoticia/(\d+)/$","sociedad.apps.noticias.views.poncomentarionoticia"),

)
