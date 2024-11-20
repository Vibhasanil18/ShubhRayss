# myapp/urls.py (App-level)

from django.urls import path
from myapp import views  # Import views from the same app
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.home, name='home'),  # Route for home page (relative to myapp/)
    path('home1/', views.home1, name='home1'),  # Route for home page (relative to myapp/)
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('festival_database/', views.festival_database, name='festival_database'),
    path('event/<int:event_id>/', views.event_details, name='event_details'),  
    path('sweet_shop/', views.sweet_shop, name='sweet_shop'),
    path('download-sales-report/', views.download_sales_report, name='download_sales_report'),
    path('diwali_wishes/', views.create_wish, name='create_wish'),
    path('light_diyas/', views.light_diyas, name='light_diyas'),
    path('light_diya/<int:diya_id>/', views.toggle_diya, name='toggle_diya'),
    path('quiz/', views.quiz_view, name='quiz'),
]

urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
