"""hotelManagement URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls,),
    path('',views.viewHome,name='home'),
    path('search',views.showAvailableRooms,name='search'),
    path('reserve/<str:pk>',views.reserve,name='reserve'),
    path('check-ins',views.upcomingReservations,name='check-ins'),
    path('room/<str:pk>',views.viewRoom,name='room_detail'),
    path('available',views.showAvailableRooms,name='available'),
    path('employee',views.employeePage,name='employee'),
    path('payment/<str:pk>',views.recordPayment,name='payment'),
    path('addRoom',views.addRoom,name='addRoom'),
     path('addRoomType',views.addRoomType,name='addRoomType'),
     path('addRoomImage',views.addRoomImage,name='addRoomImage'),
     path('addRoomFeatures',views.addRoomFeature,name='addRoomFeature'),
     path('rooms',views.viewAllRooms,name='allRooms'),
     path('customer',views.customerPage,name='customer'),
     path('hotelRating',views.hotelRatingRecord,name='hotel-rating'),
     path('room-review',views.recordRoomReview,name='room-review'),
      path('room-reviews/<str:pk>',views.showReviews,name='room-reviews'),
      path('signUp',views.signUp,name='signUp'),
      path('signIn',views.signIn,name='signIn'),
      path('logout',views.logoutUser,name='logout'),
      path('ratings',views.allHotelRatings,name='ratings'),
      path('newPricePolicy',views.UpdateRoomPricing,name='newPricePolicy'),
      path('newTax',views.newTax,name='newTax'),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
