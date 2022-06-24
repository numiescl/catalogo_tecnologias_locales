from django import template

register = template.Library()


@register.simple_tag()
def lista_de_zonas(tecnologia):
    zonas = ""
    for localidad in tecnologia.localidades.all():
        zona = localidad.get_zona_display()
        if len(zonas) == 0:
            zonas = zona
        elif zona not in zonas:
            zonas += ", {0}".format(zona)
    return zonas


@register.simple_tag()
def lista_de_territorios(tecnologia):
    territorios = ""
    for localidad in tecnologia.localidades.all():
        territorio = localidad.get_territorio_display()
        if len(territorios) == 0:
            territorios = territorio
        elif territorio not in territorios:
            territorios += ", {0}".format(territorio)
    return territorios
