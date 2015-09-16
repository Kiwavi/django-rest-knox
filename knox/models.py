from django.conf import settings
from django.db import models

from knox import crypto
from knox.settings import CONSTANTS

User = settings.AUTH_USER_MODEL

class AuthTokenManager(models.Manager):
    def create(self, user):
        token = crypto.create_token_string()
        salt = crypto.create_salt_string()
        digest = crypto.hash_token(token, salt)
        auth_token = super().create(digest=digest, salt=salt, user=user)
        return token # Note only the token - not the AuthToken object - is returned

class AuthToken(models.Model):

    objects = AuthTokenManager()

    digest = models.CharField(max_length=CONSTANTS.DIGEST_LENGTH, primary_key=True)
    salt = models.CharField(max_length=CONSTANTS.SALT_LENGTH, unique=True)
    user = models.ForeignKey(User, null=False, blank=False, related_name="auth_token_set")
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s : %s" % (self.digest, self.user)