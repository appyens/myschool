from django.urls import path
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views
from . import views

app_name = 'account'

urlpatterns = [
    # manage
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/<str:username>', views.show_profile, name='show_profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    # auth views
    path('register/', views.staff_register, name='register'),
    path('login/', views.staff_login, name='login'),
    path('logout/', views.staff_logout, name='logout'),
    path('logout-then-login/', auth_views.logout_then_login, name='logout_then_login'),
    # change password urls
    path('password-change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    # reset password views
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset/confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

]
