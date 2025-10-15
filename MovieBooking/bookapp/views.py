from django.shortcuts import render,get_object_or_404,redirect
from .models import *
from django.contrib import messages
from datetime import timedelta
from datetime import datetime
from userapp.models import Booking,Payment,Person
from django.db.models import Count, Sum
from django.contrib.auth.decorators import login_required




def Index(request):
    return render(request,'index.html')

@login_required
def AdminDash(request):
    total_bookings = Booking.objects.count()

    revenue = Booking.objects.aggregate(total_revenue=Sum('total_amount'))['total_revenue'] or 0

    top_movies = (
        Booking.objects.values('showtime__movie__title').annotate(count=Count('id')).order_by('-count')[:5])

    recent_activity = (
        Booking.objects.select_related('user', 'showtime').order_by('-created_at')[:10]
    )

    context = {
        'total_bookings': total_bookings,
        'revenue': revenue,
        'top_movies': list(top_movies),
        'recent_activity': recent_activity,
    }
    return render(request,'admin dash.html',context)


@login_required
def AllMovies(request):
    movies=Movie.objects.all()
    return render(request,'all movies.html',{'movie':movies})

@login_required
def MovieDetails(request,movie_id):
    movie=get_object_or_404(Movie,id=movie_id)
    return render(request,'movie details.html',{'movie':movie})


@login_required
def AddMovie(request):

    if request.method == 'POST':
        title = request.POST.get('title')
        poster = request.FILES.get('poster')
        description= request.POST.get('description')
        genre = request.POST.get('genre')
        language = request.POST.get('language')
        hour = int(request.POST.get('hour'))
        minute = int(request.POST.get('minute'))
        release_date = request.POST.get('release_date')

        duration=timedelta(hours=hour,minutes=minute)
        release_date=datetime.strptime(release_date,"%Y-%m-%d").date()


        movie=Movie.objects.filter(title=title).exists()
        if not movie:
            Movie.objects.create(title=title,poster=poster,description=description,genre=genre,
                                 language=language,duration=duration,release_date=release_date)
            messages.success(request, 'Movie successfully added')

            return redirect('bookapp:all-movie')
        else:
            messages.info(request,'Movie already added')
            return redirect('bookapp:add-movie')
    return render(request,'add movie.html',{'genres':Movie.GENRE_CHOICES,'languages':Movie.LAN_CHOICES})

@login_required
def UpdateMovie(request,movie_id):
    movie=get_object_or_404(Movie,id=movie_id)
    if request.method == 'POST':
        title = request.POST.get('title')
        poster = request.FILES.get('poster')
        description= request.POST.get('description')
        genre = request.POST.get('genre')
        language = request.POST.get('language')
        hour = int(request.POST.get('hour'))
        minute = int(request.POST.get('minute'))
        release_date = request.POST.get('release_date')

        duration=timedelta(hours=hour,minutes=minute)
        release_date = datetime.strptime(release_date, "%Y-%m-%d").date()

        movie.title=title
        movie.description=description
        movie.poster=poster
        movie.genre=genre
        movie.language=language
        movie.duration=duration
        movie.release_date=release_date
        movie.save()
        messages.success(request, 'Movie successfully updated')
        return redirect('bookapp:movie-details',movie_id=movie_id)
    return render(request,'update movie.html',{'movie':movie})

@login_required
def DeleteMovie(request,movie_id):
    movie=get_object_or_404(Movie,id=movie_id)
    movie.delete()
    messages.success(request, 'Movie  deleted successfully')
    return redirect('bookapp:all-movie')






@login_required
def AllShows(request):
    movie=Movie.objects.filter(showtime__isnull=False).distinct()
    return render(request, 'all shows.html', {'movie': movie})



@login_required
def AddShow(request):
    movies=Movie.objects.all()
    screens=Screen.objects.all()

    if request.method == 'POST':
        movie_id = request.POST.get('movie')
        screen_id = request.POST.get('screen')
        date = request.POST.get('date')
        start = request.POST.get('start_time')
        end = request.POST.get('end_time')
        language =request.POST.get('language')
        ticket =float(request.POST.get('ticket'))

        movie=Movie.objects.get(id=movie_id)
        screen = Screen.objects.get(id=int(screen_id))


        date = datetime.strptime(date, "%Y-%m-%d").date()
        start_time = datetime.strptime(start, "%H:%M").time()
        end_time = datetime.strptime(end, "%H:%M").time()

        if movie.release_date <= date:
            ShowTime.objects.create(movie=movie,screen=screen,
                                date=date,start_time=start_time,end_time=end_time,language=language,ticket=ticket)
            messages.success(request, 'Show  added successfully')
            return redirect('bookapp:all-show')
        else:
            messages.info(request,'movie didnt released')
            return redirect('bookapp:add-show')

    return render(request,'add show.html',{'movies':movies,'screens':screens})





@login_required
def ShowDetails(request,movie_id):
    show=ShowTime.objects.filter(movie_id=movie_id)
    return render(request,'show details.html',{'show':show})


@login_required
def UpdateShow(request,show_id):
    movies = Movie.objects.all()
    screens = Screen.objects.all()
    show=get_object_or_404(ShowTime,id=show_id)


    if request.method == 'POST':
        movie_id = request.POST.get('movie')
        screen_id = request.POST.get('screen')
        date = request.POST.get('date')
        start = request.POST.get('start_time')
        end = request.POST.get('end_time')
        language =request.POST.get('language')
        ticket =float(request.POST.get('ticket'))

        movie=Movie.objects.get(id=movie_id)
        screen = Screen.objects.get(id=screen_id)


        date = datetime.strptime(date, "%Y-%m-%d").date()
        start_time = datetime.strptime(start, "%H:%M").time()
        end_time = datetime.strptime(end, "%H:%M").time()



        show.movie=movie
        show.screen=screen
        show.date=date
        show.start_time=start_time
        show.end_time=end_time
        show.language=language
        show.ticket=ticket
        show.save()
        messages.success(request, 'Show  updated successfully')
        return redirect('bookapp:shows-details',movie_id=show.movie_id)


    return render(request,'update show.html',{'movies':movies,'screens':screens})


@login_required
def DeleteShow(request,show_id):
    show=get_object_or_404(ShowTime,id=show_id)
    show.delete()
    messages.success(request, 'Show  deleted successfully')
    return redirect('bookapp:all-show')


@login_required
def AllScreen(request):
    screen=Screen.objects.all()
    show=ShowTime.objects.filter(screen__isnull=False)
    return render(request,'all screen.html',{'screen':screen,'show':show})




@login_required
def SeatLayout(request, screen_id):
    screen = get_object_or_404(Screen, pk=screen_id)
    seats = Seat.objects.filter(screen=screen).order_by('row', 'number')


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
        'status':Seat.SEAT_CHOICES
    }

    return render(request, 'screen seating.html',context)


@login_required
def UpdateSeatStatus(request,screen_id):
    screen=get_object_or_404(Screen,id=screen_id)
    if request.method == 'POST' :
        seat_id=request.POST.getlist('selected_seats')
        status = request.POST.get('status')
        if seat_id and status:
            Seat.objects.filter(id__in=seat_id,screen=screen).update(status=status)

        messages.success(request, 'Seat  status updated successfully')
        return redirect('bookapp:show-seats',screen_id=screen_id)



@login_required
def Allbooking(request):
    booking=Booking.objects.all().order_by('-created_at')
    return render(request,'all booking.html',{'booking':booking})


@login_required
def BookingDetails(request,booking_id):
    booking=get_object_or_404(Booking,id=booking_id)
    return render(request,'booking details.html',{'booking':booking})


@login_required
def CancelBooking(request,booking_id):
    booking=get_object_or_404(Booking,id=booking_id)
    booking.status="Cancelled"
    booking.save()
    messages.success(request, 'Booking  cancelled successfully')
    return redirect('bookapp:booking-details',booking_id=booking_id)


