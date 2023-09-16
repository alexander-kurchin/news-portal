from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group


class BasicSignupForm(SignupForm):
    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        default_group = Group.objects.get(name='common')
        default_group.user_set.add(user)
        return user

# TODO: Автодобавление в группу при регистрации через социальные медиа
