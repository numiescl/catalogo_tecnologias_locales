from django.contrib import admin
from catalogo.models import Facilitador, Ilustracion, Tecnologia, Categoria, Localidad, Realizador
from taggit.admin import Tag
from django.contrib.auth.admin import Group


# Register your models here.
class FacilitadorAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'institucion', 'correo']
    list_filter = ['institucion']


class IlustracionAdmin(admin.ModelAdmin):
    list_display = ['image_tag', 'identificador', 'descripcion_corta']
    list_display_links = ('identificador', 'descripcion_corta', 'image_tag')
    readonly_fields = ['image_tag']


class CategoriaAdmin(admin.ModelAdmin):
    pass


class TecnologiaAdmin(admin.ModelAdmin):
    view_on_site = True
    prepopulated_fields = {"slug": ("nombre",)}
    filter_horizontal = ['realizadores', 'categoria_problema']
    list_display = ('identificador', 'nombre', 'realizador', 'localidad', 'categoria', 'etiqueta', 'contacto')
    list_display_links = ('identificador', 'nombre')
    list_filter = ['localidades', 'categoria_problema', 'etiquetas']
    readonly_fields = ['ilustracion']

    def ilustracion(self, obj):
        return Ilustracion.objects.get(identificador=obj.identificador).image_tag()

    # 'localidades', 'categorias', 'etiquetas'
    def realizador(self, obj):
        return "\n".join([r.nombre for r in obj.realizadores.all()])

    def localidad(self, obj):
        return "\n".join([l.nombre for l in obj.localidades.all()])

    def categoria(self, obj):
        return "\n".join([c.nombre for c in obj.categoria_problema.all()])

    def etiqueta(self, obj):
        return "\n".join([t.name for t in obj.etiquetas.all()])


class LocalidadAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'lat', 'long', 'zona', 'territorio']
    list_filter = ['zona', 'territorio']


class RealizadorAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'localidad', 'telefono', 'correo']
    list_filter = ['localidad']


admin.site.register(Facilitador, FacilitadorAdmin)
admin.site.register(Ilustracion, IlustracionAdmin)
admin.site.register(Tecnologia, TecnologiaAdmin)
# admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Localidad, LocalidadAdmin)
admin.site.register(Realizador, RealizadorAdmin)

admin.site.unregister(Tag)
admin.site.unregister(Group)
