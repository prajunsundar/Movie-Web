from django.db import models
from django.contrib.auth.models import User
from bookapp.models import Movie,ShowTime,Seat
import uuid

class Booking(models.Model):
    STATUS_CHOICES = [
        ("Confirmed", "Confirmed"),
        ("Cancelled", "Cancelled"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    showtime = models.ForeignKey(ShowTime, on_delete=models.CASCADE)
    seats = models.ManyToManyField(Seat)
    total_amount = models.DecimalField(max_digits=8, decimal_places=2)
    booking_ref = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    qr_code = models.ImageField(upload_to="qr_codes", blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="Confirmed")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.booking_ref)


    def calculte_total_price(self):
        return self.seats.count() * self.showtime.ticket





class Payment(models.Model):
    PAYMENT_CHOICES = [
        ("UPI", "UPI"),
        ("CARD", "Debit/Credit"),
    ]
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=20,choices=PAYMENT_CHOICES)
    transaction_id = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    paid_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.transaction_id



class Person(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    phone=models.CharField(max_length=10)


    def __str__(self):
        return f"{self.user.username}-{self.phone}"


