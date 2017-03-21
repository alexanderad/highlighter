import uuid
import hashlib
from datetime import datetime

from app.app import app


class User(BaseModel):
    """User."""
    #: User first/last name or nickname
    name = peewee.CharField()
    #: Picture
    picture = peewee.CharField(null=True)
    #: "Local" side access token
    access_token = peewee.CharField(null=True)

    #: OAuth provider access token
    provider_user_id = peewee.CharField(null=True)
    #: OAuth provider refresh token
    provider_access_token = peewee.CharField(null=True)
    #: OAuth provider refresh token
    provider_refresh_token = peewee.CharField(null=True)

    class Meta:
        db_table = 'users'

    def generate_access_token(self):
        """Generates local access token based on provider's one."""
        return hashlib.sha1('{}-{}'.format(
            self.provider_access_token, self.provider_refresh_token
        ).encode()).hexdigest()

    @classmethod
    def authenticate(cls, provider_profile, provider_token):
        """Authenticate user against provider's profile."""
        provider_user_id = provider_profile['id']
        provider_name = provider_profile['name']

        user, is_created = cls.get_or_create(
            provider_user_id=provider_user_id,
            defaults={
                'name': provider_name,
                'picture': provider_profile['picture']
            }
        )
        user.provider_access_token = provider_token['access_token']
        user.provider_refresh_token = provider_token['refresh_token']
        user.access_token = cls.generate_access_token(user)
        user.save()

        return user
