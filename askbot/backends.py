import logging
from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend
from django.core.validators import email_re

LOG = logging.getLogger(__name__)

class EquaBackend(ModelBackend):
    def authenticate(
                self,
                equa_id=None,
                password=None
            ):


        if equa_id is None or password is None:
            return None

        equa_id = int(equa_id)

        try:
            user = User.objects.get(equa_id=equa_id)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            LOG.error("User with equa_id == %d not found" % equa_id)
            return None

class EmailBackend(ModelBackend):
    def authenticate(self, username=None, password=None):
        print username, password
        if email_re.search(username):
            try:
                users = User.objects.filter(email=username)
                for user in users:
                    if user.check_password(password):
                        return user
            except User.DoesNotExist:
                return None
        return None
