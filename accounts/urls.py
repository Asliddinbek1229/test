from django.urls import path
from .views import user_login, user_logout, dashboard_view, user_register, SignUpView, edit_user_view, EditUserView
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordChangeDoneView, \
    PasswordResetView, PasswordResetConfirmView, PasswordResetDoneView, PasswordResetCompleteView

urlpatterns = [
    # path('login/', user_login, name='user_login'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', user_logout, name='logout'),
    path('password-change/', PasswordChangeView.as_view(), name='password_change'),
    path('password-change-done/', PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password-reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('password-reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset/complete/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('signup/', user_register, name='register'),
    # path('signup/', SignUpView.as_view(), name='register')
    path('profile/edit/', edit_user_view, name='edit_user'),
    # path('profile/edit/', EditUserView.as_view(), name='edit_user'),
]