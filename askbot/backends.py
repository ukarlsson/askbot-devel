import logging
from sqlalchemy.ext.sqlsoup import SqlSoup
from sqlalchemy import create_engine
from django.conf import settings
from django.contrib.auth.models import User

LOG = logging.getLogger(__name__)

uri = 'postgresql://%s:%s@%s/%s' % (
        settings.EQUA_AUTH_USER,
        settings.EQUA_AUTH_PASSWORD,
        settings.EQUA_AUTH_HOST,
        settings.EQUA_AUTH_NAME
    )

engine = create_engine(uri)

class EquaBackend(object):
    def authenticate(
                self,
                password=None,
                email=None,
                equa_id=None
            ):

        try:
            db = SqlSoup(engine)

            equa_user = db.db_user.get(equa_id)

        except Exception, e:
            LOG.error("Unexpected Exception Occurred")
            LOG.exception(e)
            return None

        if equa_user.password != password:
            LOG.error("Invalid password for user with id '%s'" % equa_id)
            return None

        try:
            user = User.objects.get(equa_id = equa_id)
        except User.DoesNotExist:
            user = User()
            user.equa_id = equa_id
            user.username = (
                    equa_user.first_name.strip() + ' ' +
                    equa_user.last_name.strip()
                )
            user.set_unusable_password()
            user.first_name = equa_user.first_name
            user.last_name = equa_user.last_name
            user.email = equa_user.email
            user.is_staff = False
            user.is_superuser = False
            user.is_active = True
            user.save()

        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
