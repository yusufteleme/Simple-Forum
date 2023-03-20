from django.urls import path

from . import views

app_name = "main"
urlpatterns = [
	path("", views.IndexView.as_view(), name="index"),
	path("post-create/", views.post_create, name='post-create'),
	path("<int:pk>/", views.PostView.as_view(), name="post-detail"),
	path("entry-create/", views.entry_create, name="entry-create"),
	path("signup/", views.SignUpView.as_view(), name="signup"),
	path("login/", views.LoginView.as_view(), name="login"),
	path('logout/', views.my_logout, name='logout'),
	path('change-password/', views.PasswordChangeView.as_view(), name='change-password'),
	path('account/<int:pk>/', views.AccountView.as_view(), name='account'),
	path('account/<int:pk>/email-update/', views.email_update, name='email-update'),
]
