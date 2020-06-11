from account.models import StaffProfile


def headmaster_required(myfunc):
    def inner(request):
        user = request.user
        profile = StaffProfile.objects.get(user=user)
        if profile.role == 'Headmaster':
            return myfunc()
        return inner
