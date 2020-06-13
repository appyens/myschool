from django.http import Http404


def headmaster_required(myfunc):
    def inner(request):
        user = request.user
        if user.profile.role == 'headmaster':
            return myfunc(request)
        raise Http404("You are not allowed to view this page")
    return inner
