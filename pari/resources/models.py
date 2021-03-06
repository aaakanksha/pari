from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.db import models

from mezzanine.core.managers import DisplayableManager
from mezzanine.core.models import Displayable
from mezzanine.core.fields import FileField
from pari.article.mixins import AdminThumbMixin


class Resource(Displayable):
    embed_source = models.CharField(max_length=100)
    date = models.DateField(max_length=100, blank=True, null=True)
    authors = models.TextField(verbose_name=_("Author"), max_length=200, blank=True, null=True)
    focus = models.TextField(verbose_name=_("Focus"), max_length=1000, blank=True, null=True)
    copyright = models.TextField(verbose_name=_("Copyright"), max_length=200, blank=True, null=True)
    objects = DisplayableManager()
    search_fields = {"title": 10, "description": 5}
    thumbnail_url = models.TextField(blank=True, null=True,
                                     help_text="Non editable field which will be auto-populated based on embed source")
    type_filter_order = 2

    @models.permalink
    def get_absolute_url(self):
        return ("resource-detail", (), {"slug": self.slug})

    @property
    def get_thumbnail(self):
        return self.thumbnail_url

    class Meta:
        verbose_name = _("Resource")
        verbose_name_plural = _("Resources")
        ordering = ("title",)
        app_label = "resources"


class Factoid(Displayable, AdminThumbMixin):
    resource = models.ForeignKey("Resource", related_name="factoids", null=True, blank=True)
    image = FileField(verbose_name=_("Image"),
                      format="Image", max_length=255, null=True, blank=True)

    admin_thumb_field = "image"
    external_link = models.CharField(max_length=100, blank=True)

    def get_absolute_url(self):
        if self.resource:
            return reverse("resource-detail", kwargs={"slug": self.resource.slug})
        else:
            return self.external_link

    @property
    def get_thumbnail(self):
        return ""

    class Meta:
        verbose_name = _("Factoid")
        verbose_name_plural = _("Factoids")
        app_label = "resources"
