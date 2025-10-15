from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Screen, Seat


@receiver(post_save, sender=Screen)
def create_seats_for_screen(sender, instance, created, **kwargs):
    if created:
        rows = instance.rows
        columns = instance.columns

        for row_num in range(1, rows + 1):

            row_label = chr(64 + row_num)
            for col_num in range(1, columns + 1):
                seat_number = f"{row_label}{col_num}"
                Seat.objects.create(
                    screen=instance,
                    seat_number=seat_number,
                    row=row_label,
                    number=col_num,
                    status='Available'
                )

