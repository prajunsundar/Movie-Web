from django.db import models
from django.contrib.auth.models import User

class Theater(models.Model):
    name=models.CharField(max_length=50)
    city=models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Screen(models.Model):
    theater=models.ForeignKey(Theater,on_delete=models.CASCADE,related_name='screen')
    screen=models.CharField(max_length=10)
    rows=models.PositiveIntegerField(default=10)
    columns=models.PositiveIntegerField(default=15)


    def __str__(self):
        return f"{self.theater.name}-{self.screen}"



class Seat(models.Model):
    SEAT_CHOICES = [('Available', 'Available'),
                    ('Booked', 'Booked'),
                     ('Premium', 'Premium'),
                     ('Blocked', 'Blocked')
                     ]

    screen=models.ForeignKey(Screen,on_delete=models.CASCADE,related_name='seat')
    seat_number=models.CharField(max_length=50)
    row=models.CharField(max_length=10)
    number=models.PositiveIntegerField()
    status=models.CharField(max_length=20,choices=SEAT_CHOICES)

    def __str__(self):
        return self.seat_number



class Movie(models.Model):


    GENRE_CHOICES = [('Action', 'Action'),
                     ('Comedy', 'Comedy'),
                     ('Drama', 'Drama'),
                     ('Horror', 'Horror'),
                     ('Science fiction ', 'Science fiction '),
                     ('Romance', 'Romance')
                     ]

    LAN_CHOICES = [('English', 'English'),
                   ('Malayalam', 'Malayalam'),
                   ('Tamil', 'Tamil'),
                   ('Korean', 'Korean'),
                   ]

    title=models.CharField(max_length=100)
    poster=models.ImageField(upload_to='movie poster')
    description=models.TextField()
    genre=models.CharField(max_length=100,choices=GENRE_CHOICES)
    language=models.CharField(max_length=50,choices=LAN_CHOICES)
    duration=models.DurationField()
    release_date=models.DateField()

    def __str__(self):
        return self.title


class ShowTime(models.Model):
    movie=models.ForeignKey(Movie,on_delete=models.CASCADE,related_name='showtime')
    screen = models.ForeignKey(Screen, on_delete=models.CASCADE)
    date=models.DateField()
    start_time=models.TimeField()
    end_time = models.TimeField()
    language=models.CharField(max_length=50)
    ticket=models.DecimalField(max_digits=8,decimal_places=2)





