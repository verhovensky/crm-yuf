from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

#
# class AccountConfig(AppConfig):
#     name = 'account'

class ProfilesConfig(AppConfig):
    name = 'account'
    verbose_name = _('UserProfiles')

    def ready(self):
        import crmdev.account.signals  # noqa
