from django.db import models
from django.template.defaultfilters import slugify
from django.utils.crypto import get_random_string
from taggit.managers import TaggableManager
from django.utils.safestring import mark_safe
from django.urls import reverse


class Localidad(models.Model):
    nombre = models.CharField(max_length=200)
    lat = models.DecimalField(max_digits=9, decimal_places=6, verbose_name="Latitud", help_text="Usar 6 decimales")
    long = models.DecimalField(max_digits=9, decimal_places=6, verbose_name="Longitud", help_text="Usar 6 decimales")

    class Zona(models.TextChoices):
        NORTE = 'N'
        CENTRO = 'C'
        SUR = 'S'
    zona = models.CharField(max_length=1, choices=Zona.choices)

    class Territorio(models.TextChoices):
        CORDILLERA = 'COR'
        VALLE = 'VAL'
        COSTA = 'COS'
    territorio = models.CharField(max_length=4, choices=Territorio.choices)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = "localidades"


class Facilitador(models.Model):
    nombre = models.CharField(max_length=200)
    telefono = models.CharField(max_length=55, blank=True)
    correo = models.EmailField()
    institucion = models.TextField(blank=True)
    comentarios = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = "facilitadores"


class Categoria(models.Model):
    nombre = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = "categorias"


class Ilustracion(models.Model):
    identificador = models.PositiveIntegerField(unique=True, help_text="Debe ser el mismo identificador de la "
                                                                       "tecnología")
    imagen = models.ImageField(upload_to='tecnologias/ilustraciones/', help_text="Tamaño default de las "
                                                                                 "ilustraciones: 397x397 px")
    descripcion_corta = models.CharField(max_length=200,
                                         help_text="Descripción de la imagen para visitantes no videntes")

    def __str__(self):
        return self.descripcion_corta

    def image_tag(self):
        if self.imagen:
            return mark_safe('<a href="{0}" target="_blank"> <img src="{0}" style="width: 55px; height:55px;" /> </a>'
                             .format(self.imagen.url))
        else:
            return 'No Image Found'
    image_tag.short_description = 'Ilustración'

    class Meta:
        verbose_name_plural = "ilustraciones"


class Realizador(models.Model):
    nombre = models.CharField(max_length=200)
    localidad = models.ForeignKey(Localidad, on_delete=models.PROTECT)
    telefono = models.CharField(max_length=55, blank=True)
    correo = models.EmailField(blank=True)
    comentarios = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = "realizadores"


class Tecnologia(models.Model):
    identificador = models.PositiveIntegerField(unique=True, help_text="Debe ser el mismo identificador de la "
                                                                       "ilustración")

    nombre = models.CharField(max_length=200)

    resumen = models.TextField()
    descripcion = models.TextField()

    realizadores = models.ManyToManyField(Realizador)

    localidades = models.ManyToManyField(Localidad)

    objetivo = models.TextField(verbose_name='En qué consiste')

    categoria_problema = models.ManyToManyField(Categoria)

    etiquetas = TaggableManager()

    problema_descripcion = models.TextField(verbose_name="Problema que busca resolver")

    materiales = models.TextField()

    aspectos_tecnicos = models.TextField()

    dificultad_costo = models.TextField(verbose_name="Costo y dificultad")

    contacto = models.ForeignKey(Facilitador, on_delete=models.PROTECT)

    descripcion_historia = models.TextField(verbose_name="Trayectoria y Futuro")

    slug = models.SlugField(max_length=255)
    url_corto = models.SlugField(max_length=5, blank=True, editable=False)

    def ilustracion(self):
        try:
            ilustracion = Ilustracion.objects.get(identificador=self.identificador)
        except:
            ilustracion = None
        return ilustracion

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        self.slug = slugify(self.nombre)
        generar_url_corto(self)

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('detalles_tecnologia', kwargs={'slug': self.slug})


    class Meta:
        verbose_name_plural = "tecnologias"


def generar_url_corto(obj):
    if not obj.url_corto:
        obj.url_corto = get_random_string(5)
        url_corto_malo = True

        while url_corto_malo:
            url_corto_malo = False
            otros_obj_con_url_corto = type(obj).objects.filter(url_corto=obj.url_corto)
            if len(otros_obj_con_url_corto) > 0:
                url_corto_malo = True
            if url_corto_malo:
                obj.url_corto = get_random_string(5)
