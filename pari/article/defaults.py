from django.utils.translation import ugettext_lazy as _

from mezzanine.conf import register_setting


register_setting(
    name="SITE_FULL_TITLE",
    label=_("Full Site Title"),
    description="Expanded title",
    editable=True,
    default="People's Archive of Rural India",
)
register_setting(
    name="SOCIAL_FACEBOOK",
    label=_("Facebook Page Url"),
    description="Facebook Page Url for PARI",
    editable=True,
    default="http://facebook.com",
)
register_setting(
    name="SOCIAL_TWITTER",
    label=_("Twitter Account"),
    description="Url to Twitter account",
    editable=True,
    default="http://twitter.com",
)
register_setting(
    name="SOCIAL_GOOGLE_PLUS",
    label=_("Google Plus Page Url"),
    description="Google Page Url for PARI",
    editable=True,
    default="http://plus.google.com",
)
register_setting(
    name="SOCIAL_GITHUB_REPO",
    label=_("Github Repo Url"),
    description="Github Url for PARI",
    editable=True,
    default="https://github.com/ruralindia/pari",
)
register_setting(
    name="TEMPLATE_ACCESSIBLE_SETTINGS",
    description=_("Sequence of setting names available within templates."),
    editable=False,
    default=(
        "SITE_FULL_TITLE",
    ),
    append=True,
)
register_setting(
    name="ALLOW_COMMENTS_IN_TALKING_ALBUM",
    label=_("Allow comments in talking albums"),
    description="Check to enable comments section for talking albums",
    editable=True,
    default=False
)
