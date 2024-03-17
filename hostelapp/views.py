from datetime import datetime
import json
from django.shortcuts import get_object_or_404, redirect, render
from django.http import Http404, HttpResponse, JsonResponse
from hostelapp.forms import AddHostelForm
from hostelapp.models import Floor, Hostel, Room, Bed, UserProfile, UserRegistration
from django.contrib import messages
from django.db.models import F, Max, Count
from django.db import transaction
  # Import pandas for DataFrame creation




def dashboard(request):
    # Annotate hostels with the count of floors
    hostels = Hostel.objects.annotate(
        num_floors=Count('floor__id', distinct=True)
    ).all()

    # Other data retrieval
    rooms = Room.objects.all()
    users = UserRegistration.objects.all()
    total_students = users.count()
    beds = Bed.objects.all()
    total_rooms = rooms.count()
    active_hostel_count = Hostel.objects.filter(status='active').count()

    total_floors = 0
    total_beds = beds.count()

    for hostel in hostels:
        total_floors += hostel.num_floors or 0
        total_beds += sum(room.capacity for room in Room.objects.filter(floor__hostel=hostel) if room.capacity is not None)

    hostel_occupancy_data = []

    for hostel in hostels:
        occupied_beds = Bed.objects.filter(room__floor__hostel=hostel, is_occupied=True).count()
        vacant_beds = Bed.objects.filter(room__floor__hostel=hostel, is_occupied=False).count()

        hostel_occupancy_data.append({
            'hostel': hostel,
            'occupied_beds': occupied_beds,
            'vacant_beds': vacant_beds,
        })

    context = {
        'total_floors': total_floors,
        'total_rooms': total_rooms,
        'total_beds': total_beds,
        'hostels': hostels,
        'active_hostel_count': active_hostel_count,
        'total_students': total_students,  # Assuming total_students represents occupied beds
        'hostel_occupancy_data': hostel_occupancy_data,
    }

    return render(request, 'hostelapp/dashboard.html', context)

def hostel_page(request):
    hostels = Hostel.objects.all()
    total_rooms = Floor.number_of_rooms
    hostel_data = []

    for hostel in hostels:
        total_floors = Floor.objects.filter(hostel=hostel).count()
        

        hostel_data.append({
            'hostel': hostel,
            'total_floors': total_floors,
            'total_rooms':total_rooms

             
        })

    context = {
        'hostel_data': hostel_data,
        
    }
    return render(request, 'hostelapp/hostel.html', {'hostels': hostels})

def hostel_detail(request, hostel_id):
    hostel = get_object_or_404(Hostel, pk=hostel_id)
    total_rooms = hostel.get_total_rooms() 
    total_beds = hostel.get_total_beds() 
    

    context = {
        'hostel': hostel,
        'totalRooms': total_rooms,
        'totalBeds':total_beds,
    }

    return render(request, 'hostelapp/hostel_detail.html', context)


def add_hostel_form(request):
    if request.method == 'POST':
        # Form submission logic

        # Get data from the form
        name = request.POST.get('name')
        address = request.POST.get('address')
        organisation = request.POST.get('organisation')
        branch = request.POST.get('branch')
        total_floors = int(request.POST.get('total_floors'))

        # Create Hostel instance
        hostel = Hostel(name=name, address=address, organisation=organisation, branch=branch, total_floors=total_floors)
        hostel.save()

        for floor_number in range(1, total_floors + 1):
            total_rooms_str = request.POST.get(f'total_rooms_floor_{floor_number}')
          
            total_rooms = int(total_rooms_str) if total_rooms_str is not None else 0
            floor = Floor(hostel=hostel, floor_number=floor_number, number_of_rooms=total_rooms)
            floor.save()

        return redirect('hostel_page')

    return render(request, 'hostelapp/add_hostel.html')


def edit_hostel(request, hostel_id):
    hostel = get_object_or_404(Hostel, id=hostel_id)

    if request.method == 'POST':
        # Update the hostel fields directly
        hostel.name = request.POST.get('name')
        hostel.branch = request.POST.get('branch')
        hostel.organisation = request.POST.get('organisation')
        
        hostel.save()

        # Redirect to the hostel detail page or wherever you want
        return redirect('hostel_detail', hostel_id=hostel_id)

    return render(request, 'hostelapp/edit_hostel.html', {'hostel': hostel})


def add_floor(request, hostel_id):
    hostel = get_object_or_404(Hostel, id=hostel_id)

    if request.method == 'POST':
        total_floors_to_add = int(request.POST.get('floor_number'))

        hostel.total_floors += total_floors_to_add
        hostel.save()

        # Get the highest existing floor number
        highest_existing_floor = Floor.objects.filter(hostel=hostel).order_by('-floor_number').first()

        # If there are existing floors, start the new floor numbers from the next number
        start_floor_number = 1 if highest_existing_floor is None else highest_existing_floor.floor_number + 1

        for floor_number in range(start_floor_number, start_floor_number + total_floors_to_add):
            floor = Floor(hostel=hostel, floor_number=floor_number)
            floor.save()
        messages.success(request, 'Success')

        return redirect('hostel_page')
    
def add_room(request, hostel_id):
    hostel = get_object_or_404(Hostel, id=hostel_id)
   
    floors = Floor.objects.filter(hostel_id=hostel_id)

    if request.method == 'POST':
        floor_number = request.POST['floor_number']
        room_number = request.POST['room_number']
        

        # Check if the room already exists
        if Room.objects.filter(floor__hostel=hostel, floor__floor_number=floor_number, room_number=room_number).exists():
            messages.error(request, 'Room already exists for the specified floor.')
        else:
            floor = Floor.objects.get(hostel=hostel, floor_number=floor_number)
            Room.objects.create(floor=floor, room_number=room_number)
            messages.success(request, 'Room added successfully.')

        return redirect('hostel_detail', hostel_id=hostel_id)

    return render(request, 'hostelapp/add_room.html', {'hostel': hostel, 'floors': floors})

def add_bed(request, hostel_id):
    hostel = get_object_or_404(Hostel, id=hostel_id)
    floors = hostel.floor_set.all()

    if request.method == 'POST':
        floor_number = request.POST.get('floor')
        room_number = request.POST.get('room')
        num_beds = int(request.POST.get('num_beds'))

        room = get_object_or_404(Room, floor__hostel=hostel, floor__floor_number=floor_number, room_number=room_number)
        
        max_bed_number = Bed.objects.filter(room=room).aggregate(Max('bed_number'))['bed_number__max'] or 0

        for bed_number in range(max_bed_number + 1, max_bed_number + 1 + num_beds):
            Bed.objects.create(room=room, bed_number=bed_number)

        Room.objects.filter(pk=room.pk).update(number_of_beds=F('number_of_beds') + num_beds)

        messages.success(request, 'Success')
        return redirect('hostel_detail', hostel_id=hostel_id)

    return render(request, 'hostelapp/add_bed.html', {'hostel': hostel, 'floors': floors})

  
def get_rooms(request):
    hostel_id = request.GET.get('hostel_id')
    floor_number = request.GET.get('floor_number')
    floor = get_object_or_404(Floor, hostel_id=hostel_id, floor_number=floor_number)
    rooms = floor.room_set.values_list('room_number', flat=True)
    return JsonResponse({'rooms': list(rooms)})


def update_hostel_status(request):
    if request.method == 'POST':
        hostel_id = request.POST.get('hostel_id')
        new_status = request.POST.get('status')

        hostel = Hostel.objects.get(id=hostel_id)
        hostel.status = new_status
        hostel.save()

        messages.success(request, 'Success')
        
    return redirect('hostel_page') 

def get_floors(request):
    hostel_id = request.GET.get('hostel_id')
    floors = Floor.objects.filter(hostel_id=hostel_id).values('floor_number')
    return JsonResponse({'floors': list(floors)})


def get_beds(request):
    hostel_id = request.GET.get('hostel_id')
    floor_number = request.GET.get('floor_number')
    room_number = request.GET.get('room_number')
    beds = Bed.objects.filter(
        room__floor__hostel_id=hostel_id, 
        room__floor__floor_number=floor_number, 
        room__room_number=room_number, 
        is_occupied=False
    ).values('bed_number')
    return JsonResponse({'beds': list(beds)})

def user_registration(request):
    hostels = Hostel.objects.filter(status='active')
    floors = Room.objects.filter(floor__hostel__status='active').values('floor__floor_number').distinct()
    rooms = Room.objects.filter(floor__hostel__status='active').values('room_number').distinct()
    beds = Bed.objects.filter(room__floor__hostel__status='active').values('bed_number').distinct()
    user_profiles = UserProfile.objects.all()
    
    if request.method == 'POST':
        user_profile_id = request.POST.get('user')
        hostel_id = request.POST.get('hostel')
        floor_number = request.POST.get('floor')
        room_number = request.POST.get('room')
        bed_number = request.POST.get('bed')
        admission_date = request.POST.get('admission_date')

        user_profile = get_object_or_404(UserProfile, id=user_profile_id)

        with transaction.atomic():
            selected_bed = Bed.objects.select_for_update().get(
                room__floor__hostel__id=hostel_id,
                room__floor__floor_number=floor_number,
                room__room_number=room_number,
                bed_number=bed_number,
            )

            if selected_bed.is_occupied:
                messages.error(request, 'Selected bed is already occupied.')
            else:
                selected_room = get_object_or_404(Room, floor__hostel__id=hostel_id, floor__floor_number=floor_number, room_number=room_number)

                # Update the Room instance to mark it as occupied
                Room.objects.filter(pk=selected_room.pk).update(number_of_beds=F('number_of_beds') + 1)

                # Create UserRegistration instance using actual objects
                user_registration = UserRegistration.objects.create(
                    user_profile=user_profile,
                    hostel=selected_bed.room.floor.hostel,
                    floor=selected_room.floor,
                    room=selected_room,
                    bed=selected_bed,  # Pass the Bed object, not just the bed_number
                    admission_date=datetime.strptime(admission_date, "%Y-%m-%d").date(),
                    status='active'
                )

                # Update the Bed instance to mark it as occupied
                Bed.objects.filter(pk=selected_bed.pk).update(is_occupied=True, status='inactive')

                messages.success(request, 'Student added successfully.')
                return redirect('dashboard')

    context = {
        'hostels': hostels,
        'floors': floors,
        'rooms': rooms,
        'beds': beds,
        'user_profiles': user_profiles,
    }

    return render(request, 'hostelapp/user_registration.html', context)


def view_users(request):
    user_registrations = UserRegistration.objects.all()

    context = {
        'user_registrations': user_registrations
    }

    return render(request, 'hostelapp/view_users.html', context)


def update_user_status(request, user_id):
    user_registration = get_object_or_404(UserRegistration, id=user_id)

    if request.method == 'POST':
        new_status = request.POST.get('status')

        # Update user status
        user_registration.status = new_status
        user_registration.save()

        # Update associated beds if the user is assigned a bed
        if user_registration.bed:
            user_bed = user_registration.bed

            # Update is_occupied based on user status
            user_bed.is_occupied = new_status == 'active'
            user_bed.save()

            # Update bed status opposite to user status
            user_bed.status = 'inactive' if new_status == 'active' else 'active'
            user_bed.save()

        messages.success(request, 'User status updated successfully')
    return redirect('view_users')


def get_user_details(request, user_id):
    user_profile = get_object_or_404(UserProfile, id=user_id)
    data = {
        'organisation': user_profile.organisation,
        'branch': user_profile.branch,
    }
    return JsonResponse(data)


def hostel_analytics(request):
    # Hostel-wise Bed Utilization
    hostels = Hostel.objects.all()
    bed_utilization_data = []

    for hostel in hostels:
        occupied_beds = Bed.objects.filter(room__floor__hostel=hostel, is_occupied=True).count()
        total_beds = Bed.objects.filter(room__floor__hostel=hostel).count()

        utilization_percentage = (occupied_beds / total_beds) * 100 if total_beds != 0 else 0

        bed_utilization_data.append({
            'Hostel': hostel.name,
            'Occupied Beds': occupied_beds,
            'Total Beds': total_beds,
            'Utilization Percentage': utilization_percentage
        })


    bed_utilization_fig = px.bar(bed_utilization_data, x='Hostel', y='Utilization Percentage',
                                color='Hostel', labels={'Utilization Percentage': 'Bed Utilization (%)'},
                                title='Hostel-wise Bed Utilization',
                                color_discrete_sequence=px.colors.qualitative.Set2)
    
    occupied_beds = Bed.objects.filter(is_occupied=True).count()
    vacant_beds = Bed.objects.filter(is_occupied=False).count()

    room_occupancy_data = {
        'Occupied Beds': occupied_beds,
        'Vacant Beds': vacant_beds,
    }


    room_occupancy_fig = px.pie(names=room_occupancy_data.keys(),
                                values=room_occupancy_data.values(), title='Room Occupancy Status',
                                color_discrete_sequence=px.colors.qualitative.Set2)

    # User Distribution by Organisation/Branch
    users = UserProfile.objects.all()
    user_distribution_data = {
        'Organisation': [user.organisation for user in users],
        'Branch': [user.branch for user in users],
    }

    user_distribution_fig = px.bar(user_distribution_data, x='Organisation', color='Branch',
                                   labels={'Organisation': 'Organization', 'count': 'Number of Users'},
                                   title='User Distribution by Organisation/Branch',
                                color_discrete_sequence=px.colors.qualitative.Set2_r)  
    
    

    return render(request, 'hostelapp/hostel_analytics.html', {
        'bed_utilization_plot': bed_utilization_fig.to_html(),
        'room_occupancy_plot': room_occupancy_fig.to_html(),
        'user_distribution_plot': user_distribution_fig.to_html(),
        
    })
