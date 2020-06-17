from django.db import models


class ProfileManager(models.Manager):

    def active(self):
        queryset = super(ProfileManager, self).get_queryset().filter(is_active=True)
        return queryset

    def teachers(self):
        queryset = super(ProfileManager, self).get_queryset().filter(is_teacher=True, is_active=True)
        return queryset
