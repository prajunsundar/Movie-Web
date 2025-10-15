from django.urls import path
from .views import *
app_name='bookapp'

urlpatterns=[
    path('',Index,name='index'),
    path('admin-dash',AdminDash,name='admin-dash'),

    path('all-movies',AllMovies,name='all-movie'),
    path('movie-details/<int:movie_id>/',MovieDetails,name='movie-details'),
    path('add-movie',AddMovie,name='add-movie'),
    path('movie-update/<int:movie_id>/',UpdateMovie,name='movie-update'),
    path('movie-delete/<int:movie_id>/',DeleteMovie,name='movie-delete'),

    path('all-show', AllShows, name='all-show'),
    path('add-show', AddShow, name='add-show'),
    path('shows-details/<int:movie_id>/', ShowDetails, name='shows-details'),
    path('update-show/<int:show_id>/', UpdateShow, name='show-update'),
    path('delete-show/<int:show_id>/', DeleteShow, name='show-delete'),


    path('all-screen',AllScreen,name='all-screen'),
    path('show-seats/<int:screen_id>/', SeatLayout, name='show-seats'),
    path('update-seats/<int:screen_id>/', UpdateSeatStatus, name='update-seats'),

    path('view-booking',Allbooking,name='all-booking'),
    path('booking-details/<int:booking_id>/', BookingDetails, name='booking-details'),
    path('cancel-booking/<int:booking_id>/', CancelBooking, name='cancel-booking'),
]