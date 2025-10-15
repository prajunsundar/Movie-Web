import os.path

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse, FileResponse
from .models import Person,Booking
from bookapp.models import Movie,ShowTime,Screen,Seat
from django.contrib.auth.decorators import login_required
from datetime import datetime
from datetime import timedelta
import io
import qrcode
from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from django.core.files import File
from django.conf import settings


def Registration(request):
    if request.method == 'POST':
        email = request.POST['email']
        phone = request.POST['phone']
        pwd1 = request.POST['password1']
        pwd2 = request.POST['password2']

        name=email.split('@')[0]


        if pwd1 == pwd2:
            if User.objects.filter(email=email).exists():
                messages.warning(request,'Email Already Exists')
                return redirect('userapp:register')

            user=User.objects.create_user(username=name,email=email,password=pwd1)
            if user:
                person,create=Person.objects.get_or_create(user=user)
                person.phone=phone
                person.save()
                messages.success(request, 'User created successfully')
                return redirect('userapp:login')

        else:
            messages.warning(request,'Password Is Not matching')
            return redirect('userapp:register')

        return redirect('bookapp:index')

    return render(request,'register.html')



def LoginUser(request):
    if request.method == 'POST':
        email = request.POST.get('username')
        pwd = request.POST.get('password')

        user=authenticate(username=email,password=pwd)
        if user is not None:
            login(request, user)
            if user.is_superuser or user.is_staff:
                messages.info(request,'admin logged in ')
                return redirect('bookapp:admin-dash')

            messages.info(request, 'user logged in ')
            return redirect('userapp:user-dash')
        else:
            messages.error(request, 'Something Went Wrong')
            return redirect('userapp:login')

    return render(request,'login.html')


def Logout(request):
    logout(request)
    messages.success(request,'successfully logged out')
    return redirect('bookapp:index')



@login_required
def UserDash(request):
    movies = Movie.objects.all()
    language_filter = request.GET.get('language', '')
    date_filter = request.GET.get('release_date', '')
    genre_filter = request.GET.get('genre')

    if language_filter:
        movies = Movie.objects.filter(language=language_filter)
    if date_filter:
        movies = Movie.objects.filter(release_date=date_filter)
    if genre_filter:
        movies = Movie.objects.filter(genre=genre_filter)

    context={
        'movie': movies,
        'lan':Movie.LAN_CHOICES,
        'genre':Movie.GENRE_CHOICES
    }
    return render(request,'user dash.html',context)




@login_required
def DetailsOfMoview(request,movie_id):
    movie=get_object_or_404(Movie,id=movie_id)
    show=ShowTime.objects.filter(movie=movie_id).exists()
    shows = ShowTime.objects.filter(movie=movie_id)

    context = {
        'show':show,
        'movie': movie,
        'shows':shows
    }

    return render(request,'details of movie.html',context)




@login_required
def SeatLayout(request,screen_id):
    screen = get_object_or_404(Screen, pk=screen_id)
    seats = Seat.objects.filter(screen=screen).order_by('row', 'number')
    show=ShowTime.objects.get(screen=screen_id)


    seat_layout_grid = []
    current_row_seats = []
    current_row_label = None

    for seat in seats:
        if current_row_label is None:
            current_row_label = seat.row

        if seat.row != current_row_label:
            seat_layout_grid.append(current_row_seats)
            current_row_seats = []
            current_row_label = seat.row
        current_row_seats.append(seat)


    if current_row_seats:
        seat_layout_grid.append(current_row_seats)

    context = {
        'screen': screen,
        'seat_layout_grid': seat_layout_grid,
        'show':show
    }
    return render(request,'user seat.html',context)


@login_required
def BookMovie(request,show_id):
    show=get_object_or_404(ShowTime,id=show_id)
    screen=show.screen
    if request.method == 'POST':
        seat_id=request.POST.getlist('selected_seats')

        seat=Seat.objects.filter(id__in=seat_id)

        booking=Booking.objects.create(user=request.user,showtime=show,total_amount=0)
        booking.seats.set(seat)
        booking.total_amount=booking.calculte_total_price()
        booking.save()
        Seat.objects.filter(id__in=seat_id, screen=screen).update(status='Booked')

        booking_ref = f"BK-{booking.id:06d}"


        qr_data = f"BookingRef:{booking_ref}\nMovie:{show.movie.title}\nSeats:{', '.join(seat.seat_number for seat in seat)}\nTheater:{show.screen.theater.name}"
        qr_img = qrcode.make(qr_data)
        qr_buffer = io.BytesIO()
        qr_img.save(qr_buffer, format="PNG")
        qr_buffer.seek(0)
        qr_pil=Image.open(qr_buffer)

        filename=f"qr_{booking.booking_ref}.png"

        booking.qr_code.save(filename,File(qr_buffer),save=True)

        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)


        p.setFont("Helvetica-Bold", 18)
        p.drawString(200, 750, "🎬 Movie Ticket")


        p.setFont("Helvetica", 12)
        p.drawString(50, 710, f"Booking Reference: {booking.booking_ref}")
        p.drawString(50, 690, f"Movie: {show.movie.title}")
        p.drawString(50, 670, f"Showtime: {show.start_time.strftime('%d %b %Y %I:%M %p')}")
        p.drawString(50, 650, f"Seats: {', '.join(seat.seat_number for seat in seat)}")
        p.drawString(50, 630, f"Theater: {show.screen.theater.name} - {show.screen.screen}")
        p.drawString(50, 610, f"Location: {show.screen.theater.city}")
        p.drawString(50, 590, f"Total Price: Rs.{booking.total_amount}")


        qr_buffer.seek(0)
        p.drawInlineImage(qr_pil, 400, 600, width=120, height=120)

        p.showPage()
        p.save()

        buffer.seek(0)

        temp_dir=os.path.join(settings.MEDIA_ROOT,'temp')
        os.makedirs(temp_dir,exist_ok=True)

        pdf_filename=f"{booking.booking_ref}.pdf"
        pdf_path=os.path.join(temp_dir,pdf_filename)
        with open(pdf_path,'wb') as f:
            f.write(buffer.getvalue())

        download_link=f"{settings.MEDIA_URL}temp/{pdf_filename}"

        messages.success(request,download_link)
        return redirect('userapp:booking-history')

@login_required
def BookingHistory(request):
    booking=Booking.objects.filter(user=request.user).order_by('-created_at')
    return render(request,'booking history.html',{'booking':booking})


@login_required
def CancelBooking(request,booking_id):
    booking=Booking.objects.get(user=request.user,id=booking_id)
    now=datetime.now()
    show_time=datetime.combine(booking.showtime.date,booking.showtime.start_time)
    if now < show_time:
        booking.delete()
        messages.success(request, 'Booking cancelled successfully')

    else:
        messages.info(request, 'you cant cancel the booking')
    return redirect('userapp:booking-history')




