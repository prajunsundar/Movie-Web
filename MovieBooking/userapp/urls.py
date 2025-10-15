from django.urls import path
from .views import *

app_name = 'userapp'

urlpatterns = [
    path('register/', Registration, name='register'),
    path('login/', LoginUser, name='login'),
    path('logout/', Logout, name='logout'),


    path('user-dash',UserDash,name='user-dash'),
    path('movie-details-view/<int:movie_id>/',DetailsOfMoview,name='movie-details-view'),
    path('seat-layout/<int:screen_id>/', SeatLayout, name='seat-layout'),
    path('book-movie/<int:show_id>/', BookMovie, name='book-movie'),
    path('booking-history', BookingHistory, name='booking-history'),
    path('cancel-booking/<int:booking_id>/', CancelBooking, name='cancel-booking'),

]