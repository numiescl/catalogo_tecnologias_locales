from django.views.generic import TemplateView, FormView, ListView, DetailView
from .forms import ContactForm
from .models import Tecnologia
from tcc_catalogo.local_settings import CORREO_ADMIN

from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response

from django.core.mail import send_mail

from django.db.models import Q


class TecnologiasAPI(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'catalogo/elementos/lista_tecnologias.html'

    def get(self, request):
        tecnologias_list = Tecnologia.objects.all()
        return Response({'tecnologias': tecnologias_list})

    def post(self, request):
        search_query = request.POST.get('query')
        tecnologias_list = Tecnologia.objects.filter(
            Q(nombre__icontains=search_query) |
            Q(resumen__icontains=search_query) |
            Q(descripcion__icontains=search_query) |
            Q(realizadores__nombre__icontains=search_query) |
            Q(localidades__nombre__icontains=search_query) |
            Q(objetivo__icontains=search_query) |
            Q(etiquetas__name__icontains=search_query) |
            Q(problema_descripcion__icontains=search_query) |
            Q(materiales__icontains=search_query) |
            Q(aspectos_tecnicos__icontains=search_query) |
            Q(dificultad_costo__icontains=search_query) |
            Q(descripcion_historia__icontains=search_query)
        )

        if request.POST.get('zona'):
            zonas = request.POST.get('zona').split(',')
            filtro_zonas = Q()
            for zona in zonas:
                filtro_zonas = filtro_zonas | Q(localidades__zona__iexact=zona)
            tecnologias_list = tecnologias_list.filter(filtro_zonas)

        if request.POST.get('categoria'):
            categorias = request.POST.get('categoria').split(',')
            filtro_categorias = Q()
            for categoria in categorias:
                filtro_categorias = filtro_categorias | Q(categoria_problema__nombre__iexact=categoria)
            tecnologias_list = tecnologias_list.filter(filtro_categorias)

        if request.POST.get('territorio'):
            territorios = request.POST.get('territorio').split(',')
            filtro_territorios = Q()
            for territorio in territorios:
                filtro_territorios = filtro_territorios | Q(localidades__territorio__iexact=territorio)
            tecnologias_list = tecnologias_list.filter(filtro_territorios)

        return Response({'tecnologias': tecnologias_list.distinct()})


class InicioView(ListView):
    template_name = 'catalogo/inicio.html'
    model = Tecnologia

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tecnologia_cabecera'] = Tecnologia.objects.order_by('?')[0]
        context['ilustracion_cabecera'] = Tecnologia.objects.order_by('?')[0]
        return context


class EnviadoView(TemplateView):
    template_name = 'catalogo/enviado.html'


class IniciativaView(TemplateView):
    template_name = 'catalogo/iniciativa.html'


class DocumentacionView(TemplateView):
    template_name = 'catalogo/documentacion.html'


class EquipoView(TemplateView):
    template_name = 'catalogo/equipo.html'


class PoliticaPrivacidadView(TemplateView):
    template_name = 'catalogo/politica_privacidad.html'


class ContactoView(FormView):
    template_name = 'catalogo/contacto.html'
    form_class = ContactForm
    success_url = '/enviado'

    def get_context_data(self, **kwargs):
        context = super(ContactoView, self).get_context_data(**kwargs)
        if self.request.GET.get('tecnologia'):
            tecnologia_id = self.request.GET.get('tecnologia')
            context['tecnologia'] = Tecnologia.objects.get(id=tecnologia_id)
        return context

    def get_initial(self):
        initial = super().get_initial()
        if self.request.GET.get('tecnologia'):
            tecnologia_id = self.request.GET.get('tecnologia')
            tecnologia = Tecnologia.objects.get(id=tecnologia_id)
            initial['asunto'] = "Tecnología: {0}\n\n".format(tecnologia.nombre)
        return initial

    def form_valid(self, form):
        if not self.request.GET.get('tecnologia'):
            nombre = form.cleaned_data.get('nombre')
            correo = form.cleaned_data.get('correo')
            mensaje = form.cleaned_data.get('mensaje')
            asunto = "Tecnologías Locales - {0}".format(form.cleaned_data.get('asunto'))
            cuerpo = 'Hola: \n El siguiente correo ha sido enviado por {usuario} <{email}>:\n\n{cuerpo}\n\nImportante: ' \
                     'Este correo es enviado automáticamente, favor no responder.'.format(usuario=nombre, email=correo,
                                                                                          cuerpo=mensaje)

            send_mail(
                subject=asunto,
                message=cuerpo,
                from_email='noreply@tecnologiaslocales.cl',
                recipient_list=[CORREO_ADMIN]
            )

            send_mail(
                subject=asunto,
                from_email='noreply@tecnologiaslocales.cl',
                recipient_list=[correo],
                message='Estimado {0},\n\nHemos recibido su correo exitosamente. Nuestro equipo se pondrá en contacto '
                        'próntamente para responder sus consultas.\n\nGracias,\nEquipo Catálogo Tecnologías '
                        'Locales\nhttps://www.tecnologiaslocales.cl\n\nImportante: Este correo es enviado '
                        'automáticamente, favor no responder.'.format(nombre)
            )

        else:
            context = self.get_context_data()
            tecnologia = context['tecnologia']
            tecnologia_nombre = tecnologia.nombre
            facilitador_nombre = tecnologia.contacto.nombre
            facilitador_correo = tecnologia.contacto.correo
            nombre = form.cleaned_data.get('nombre')
            correo = form.cleaned_data.get('correo')
            mensaje = form.cleaned_data.get('mensaje')
            asunto = "Tecnologías Locales - {0}".format(form.cleaned_data.get('asunto'))

            cuerpo_administrador = '''
                                    ¡Hola!\n\n
                                    La tecnología "{tecnologia}" tiene una nueva solicitud de contacto por parte de 
                                    {nombre} <{correo}>.Esta fue enviada al facilitador {facilitador_nombre} 
                                    <{facilitador_correo}> para que realice el contacto.\n\n

                                    Mensaje original:\n\n

                                    {mensaje}

                                    '''.format(tecnologia=tecnologia_nombre, nombre=nombre, correo=correo,
                                               facilitador_nombre=facilitador_nombre,
                                               facilitador_correo=facilitador_correo,
                                               mensaje=mensaje)

            cuerpo_facilitador = '''
                                   ¡Hola!\n\n

                                   La persona {nombre} <{correo}> quiere saber más de la tecnología "{tecnologia}". Ver 
                                   detalles abajo.\n\n

                                   {mensaje}\n\n

                                   Cualquier duda o comentario sobre esta solicitud por favor escríbenos a 
                                   {correo_admin}.
                                    '''.format(nombre=nombre, correo=correo, tecnologia=tecnologia_nombre,
                                               mensaje=mensaje, correo_admin=CORREO_ADMIN)

            cuerpo_emisor = '''
                                    ¡Hola!\n
                                    Muchas gracias por tu interés en saber más de la tecnología "{tecnologia}".\n\n

                                    Te escribiremos prontamente para ponerte en contacto con el realizador.\n\n

                                    Saludos,\n
                                    Equipo Catálogo Tecnologías Locales\n
                                    https://www.tecnologiaslocales.cl
                                    '''.format(tecnologia=tecnologia_nombre)

            # MAIL ADMIN
            send_mail(
                subject=asunto,
                message=cuerpo_administrador,
                from_email='noreply@tecnologiaslocales.cl',
                recipient_list=[CORREO_ADMIN]
            )

            # MAIL FACILITADOR
            send_mail(
                subject=asunto,
                message=cuerpo_facilitador,
                from_email='noreply@tecnologiaslocales.cl',
                recipient_list=[facilitador_correo]
            )

            # MAIL EMISOR
            send_mail(
                subject=asunto,
                message=cuerpo_emisor,
                from_email='noreply@tecnologiaslocales.cl',
                recipient_list=[correo]
            )

        return super(ContactoView, self).form_valid(form)


class FichaWebView(DetailView):
    model = Tecnologia


class FichaWebViewShortUrl(DetailView):
    model = Tecnologia
    slug_field = 'url_corto'


class FichaImprimibleView(DetailView):
    model = Tecnologia
    template_name = 'catalogo/tecnologia_imprimible.html'
