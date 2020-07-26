from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Report:
    downloaded_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    downloaded_on = models.DateTimeField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.id)