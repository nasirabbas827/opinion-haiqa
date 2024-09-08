from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.home, name='home'),
    path('comment/<int:post_id>/', views.comment_on_post, name='comment_on_post'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('update_profile/', views.update_profile, name='update_profile'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
