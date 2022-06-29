from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend
from django_auth_ldap.backend import LDAPBackend


class ModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        """ Overrides LDAPBackend.authenticate to save user password in django """
        tmp = LDAPBackend()
        try:
            user = User.objects.get(username=username)
            password_checked = user.check_password(password)
            if not password_checked:
                user = tmp.authenticate(request, username, password)
                if not user:
                    messages.error(request, 'Usuario o contraseña incorrectos', extra_tags='danger')

        except User.DoesNotExist:
            user = tmp.authenticate(request, username, password)
            if not user:
                messages.error(request, 'Usuario o contraseña incorrectos', extra_tags='danger')
        except Exception as e:
            pass
            #logger.error(e)

        return user