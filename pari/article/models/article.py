from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.template.defaultfilters import truncatewords

from mezzanine.core.managers import DisplayableManager
from mezzanine.core.fields import FileField
from mezzanine.core.models import Displayable, Ownable, RichText, Orderable
from mezzanine.generic.fields import CommentsField
from mezzanine.utils.models import upload_to

from pari.article.managers import ArticleManager, TopicManager
from pari.article.mixins import AdminThumbMixin

from .category import Category
from .location import Location
from .type import Type


class Article(Displayable, Ownable, RichText, AdminThumbMixin):
    strap = models.CharField(max_length=600, blank=True, null=True)
    locations = models.ManyToManyField(Location, verbose_name=_("Locations"), blank=True)
    is_topic = models.BooleanField(verbose_name=_("Is a topic?"), default=False)
    category_list = models.ManyToManyField(Category, verbose_name=_("Categories"),
                                           blank=False, null=False, related_name="articles")
    allow_comments = models.BooleanField(verbose_name=_("Allow comments"),
                                         default=False)
    comments = CommentsField(verbose_name=_("Comments"))

    allow_featured_image = models.BooleanField(verbose_name=_("Show Featured Image for the Article"), default=False)

    featured_image = FileField(verbose_name=_("Featured Image"),
                               format="Image", max_length=255, null=True, blank=True)

    featured_image_caption = models.CharField(max_length=1000, blank=True, null=True)

    pin_to_home = models.BooleanField(verbose_name=_("Pin to home?"), default=False)

    carousel_order = models.SmallIntegerField(verbose_name=_("Carousel order"), null=True, blank=True)

    author = models.ForeignKey("Author", related_name='articles', verbose_name="Author")

    capsule_video = models.CharField(max_length=100, null=True, blank=True)

    featured_video = models.CharField(max_length=100, null=True, blank=True)

    featured_audio = models.CharField(max_length=100, null=True, blank=True)

    date_of_publication = models.DateField(verbose_name=_("Original date of publication"), null=True, blank=True)

    related_posts = models.ManyToManyField("self",
                                           verbose_name=_("Related Articles"), blank=True)
    types = models.ManyToManyField(Type, related_name="articles", verbose_name="Article Type")

    admin_thumb_field = "featured_image"

    type_filter_order = 4

    objects = DisplayableManager()
    articles = ArticleManager()
    topics = TopicManager()

    class Meta:
        verbose_name = _("Article")
        verbose_name_plural = _("Articles")
        ordering = ("-publish_date",)
        app_label = "article"

    @models.permalink
    def get_absolute_url(self):
        name = "article-detail"
        if self.is_topic:
            name = "topic-detail"
        return name, (), {"slug": self.slug}

    @property
    def get_location_titles(self):
        return ','.join([location.title for location in self.locations.all()])

    @property
    def is_video_article(self):
        return self.types.filter(title__iexact='Video').exists()

    @property
    def thumbnail_image_text(self):
        if self.types.filter(title__iexact='Text').exists():
            return "TEXT ARTICLE"
        category_list = self.category_list.filter()
        return category_list[0].title if category_list else "ARTICLE"

    @property
    def get_thumbnail(self):
        return self.featured_image

    @property
    def short_description(self):
        return truncatewords(self.description, 20)

    def save(self, *args, **kwargs):
        self.gen_description = False
        super(Article, self).save(*args, **kwargs)


class ArticleCarouselImage(Orderable, Displayable):
    article = models.ForeignKey("article", related_name="carousel_images")
    file = FileField(_("File"), max_length=200, format="Image",
                     upload_to=upload_to("article.ArticleCarouselImage.file", "carousel"))

    is_searchable = False

    def __init__(self, *args, **kwargs):
        super(ArticleCarouselImage, self).__init__(*args, **kwargs)
        self._meta.get_field("title").blank = True

    class Meta:
        verbose_name = _("CarouselImage")
        verbose_name_plural = _("CarouselImages")
        app_label = "article"

    def __unicode__(self):
        return self.description

    @models.permalink
    def get_absolute_url(self):
        name = "article-image-detail"
        return name, (), {"slug": self.article.slug, "order": self._order + 1}

    @property
    def get_thumbnail(self):
        return self.file


def get_all_articles():
    return Article.articles.all()


def get_category_articles(category):
    return Article.articles.filter(category_list__pk=category.pk)


def get_location_articles(location):
    return Article.articles.filter(locations__location=location.location)


def get_keyword_articles(keyword):
    return Article.articles.filter(keywords__keyword=keyword)


def get_author_articles(author):
    return Article.articles.filter(author=author)


def get_archive_articles(month, year):
    return Article.articles.filter(publish_date__year=year, publish_date__month=month)
