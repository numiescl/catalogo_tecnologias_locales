from django.urls import path
from . import views


urlpatterns = [
    path('', views.InicioView.as_view(), name='inicio'),
    path('iniciativa/', views.IniciativaView.as_view(), name='iniciativa'),
    path('equipo/', views.EquipoView.as_view(), name='equipo'),
    path('documentacion/', views.DocumentacionView.as_view(), name='documentacion'),
    path('contacto/', views.ContactoView.as_view(), name='contacto'),
    path('enviado/', views.EnviadoView.as_view(), name='enviado'),
    path('tecnologias/', views.InicioView.as_view(), name='inicio_redireccion'),
    path('tecnologias/<slug>', views.FichaWebView.as_view(), name='detalles_tecnologia'),
    path('t/<slug>', views.FichaWebViewShortUrl.as_view(), name='tecnologia_url_corto'),
    path('tecnologias/<slug:slug>/imprimible', views.FichaImprimibleView.as_view(), name='tecnologia_imprimible'),
    path('buscar-tecnologias', views.TecnologiasAPI.as_view(), name='buscar_tecnologias'),
    path('politica_privacidad/', views.PoliticaPrivacidadView.as_view(), name='politica_privacidad'),
]
