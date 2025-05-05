from django.shortcuts import render, redirect, get_object_or_404
from .models import Hall, Room
from .forms import HallForm, RoomForm
from accounts.decorators import role_required
from students.models      import Admission
from .models import Hall, ActionTakenReport
from .forms import ActionTakenReportForm
from django.contrib import messages

# Halls
def hall_list(request):
    halls = Hall.objects.all()
    return render(request, 'halls/hall_list.html', {'halls': halls})

def hall_create(request):
    if request.method == 'POST':
        form = HallForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('hall_list')
    else:
        form = HallForm()
    return render(request, 'halls/hall_form.html', {'form': form})

# Rooms
def room_list(request, hall_id=None):
    if hall_id:
        hall = get_object_or_404(Hall, pk=hall_id)
        rooms = Room.objects.filter(hall=hall)
    else:
        rooms = Room.objects.select_related('hall').all()
    return render(request, 'halls/room_list.html', {'rooms': rooms})

def room_create(request):
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('room_list')
    else:
        form = RoomForm()
    return render(request, 'halls/room_form.html', {'form': form})

@role_required('hall_clerk')
def hall_create(request):
    form = HallForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('hall_list')
    return render(request, 'halls/hall_form.html', {'form': form})

@role_required('hall_clerk')
def hall_list(request):
    halls = Hall.objects.all()
    return render(request, 'halls/hall_list.html', {'halls': halls})

@role_required('warden')
def hall_occupancy(request, pk):
    hall = get_object_or_404(Hall, pk=pk)
    rooms = Room.objects.filter(hall=hall)
    return render(request, 'halls/occupancy.html', {'hall': hall, 'rooms': rooms})

@role_required('warden')
def overall_occupancy(request):
    from .models         import Hall
    from students.models import Admission

    halls       = Hall.objects.all()
    total_rooms = sum(h.room_set.count() for h in halls)
    occupied    = Admission.objects.count()
    vacant      = total_rooms - occupied

    # Build a list of (hall, occupied_count) tuples
    @role_required('warden')
    def overall_occupancy(request):
     from .models         import Hall
     from students.models import Admission

    halls       = Hall.objects.all()
    total_rooms = sum(h.room_set.count() for h in halls)
    occupied    = Admission.objects.count()
    vacant      = total_rooms - occupied

    hall_stats = []
    for hall in halls:
        occ_count = Admission.objects.filter(hall=hall).count()
        hall_stats.append({
            'hall':     hall,
            'occupied': occ_count,
            'vacant':   hall.room_set.count() - occ_count,
        })

    return render(request, 'halls/overall_occupancy.html', {
        'total_rooms': total_rooms,
        'occupied':    occupied,
        'vacant':      vacant,
        'hall_stats':  hall_stats,
    })


@role_required('warden')
def atr_create(request, hall_id):
    hall = get_object_or_404(Hall, id=hall_id)
    if request.method == 'POST':
        form = ActionTakenReportForm(request.POST)
        if form.is_valid():
            atr = form.save(commit=False)
            atr.hall = hall
            atr.created_by = request.user
            atr.save()
            messages.success(request, 'ATR submitted successfully.')
            return redirect('hall_occupancy', hall.id)
    else:
        form = ActionTakenReportForm()
    return render(request, 'halls/atr_form.html', {'form': form, 'hall': hall})


@role_required('warden')
def atr_create(request, hall_id):
    hall = get_object_or_404(Hall, id=hall_id)
    if request.method == 'POST':
        form = ActionTakenReportForm(request.POST)
        if form.is_valid():
            atr = form.save(commit=False)
            atr.hall = hall
            atr.created_by = request.user
            atr.save()
            messages.success(request, "ATR submitted successfully.")
            return redirect("halls:atr_list", hall_id=hall.id)
    else:
        form = ActionTakenReportForm()
    return render(request, "halls/atr_form.html", {
        "form": form,
        "hall": hall,
    })

@role_required('warden')
def atr_list(request, hall_id):
    hall = get_object_or_404(Hall, id=hall_id)
    atrs = hall.atrs.order_by("-date")
    return render(request, "halls/atr_list.html", {
        "hall": hall,
        "atrs": atrs,
    })
    
@role_required('warden','finance_officer','staff_admin')
def hall_occupancy(request, hall_id):
    hall = get_object_or_404(Hall, id=hall_id)
    # Assuming Room has a FK `hall` and a nullable FK `student`
    rooms    = Room.objects.filter(hall=hall)
    total    = rooms.count()
    occupied = rooms.filter(admission__isnull=False).count()
    vacant   = rooms.filter(admission__isnull=True).count()

    return render(request, "halls/hall_occupancy.html", {
        "hall":        hall,
        "total_rooms": total,
        "occupied":    occupied,
        "vacant":      vacant,
    })