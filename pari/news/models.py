from django.db import models
from django.utils.translation import ugettext_lazy as _

from mezzanine.core.managers import DisplayableManager
from mezzanine.core.models import Slugged, Displayable, Ownable, RichText
from mezzanine.generic.fields import CommentsField

from pari.article.models import Article


class NewsPost(Displayable, Ownable, RichText):
    categories = models.ManyToManyField("NewsCategory", verbose_name=_("News Category"),
                                        blank=True, related_name="news_posts")
    allow_comments = models.BooleanField(verbose_name=_("Allow comments"), default=False)
    comments = CommentsField(verbose_name=_("Comments"))

    objects = DisplayableManager()

    thumbnail_image_text = 'News'

    class Meta:
        verbose_name = _("News post")
        verbose_name_plural = _("News posts")
        ordering = ("-publish_date",)
        app_label = 'news'

    @models.permalink
    def get_absolute_url(self):
        return "news-detail", (), {"slug": self.slug}


class NewsCategory(Slugged):
    class Meta:
        verbose_name = _("News Category")
        verbose_name_plural = _("News Categories")
        ordering = ("title",)
        app_label = 'news'


class LatestArticle(models.Model):
    new_current_articles = models.ManyToManyField(Article, limit_choices_to={'id__in': Article.articles.all()},
                                                  blank=True,
                                                  verbose_name=_("New current articles"),
                                                  related_name='new_current_articles')
    new_archive_articles = models.ManyToManyField(Article, limit_choices_to={'id__in': Article.articles.all()},
                                                  blank=True,
                                                  verbose_name=_("New archive articles"),
                                                  related_name='new_archive_articles')

    class Meta:
        verbose_name = _("Latest article")
        verbose_name_plural = _("Latest articles")
        app_label = 'news'


def get_latest_news_post():
    return NewsPost.objects.first()


def get_chosen_archive_articles():
    latest_article = LatestArticle.objects.first()
    return latest_article and latest_article.new_archive_articles.all() or []


def get_chosen_current_articles():
    latest_article = LatestArticle.objects.first()
    return latest_article and latest_article.new_current_articles.all() or []
