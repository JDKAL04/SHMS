
from django.db import models
from django.contrib.auth.models import User




class Hostel(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    organisation = models.CharField(max_length=100, default='Default Organisation')
    branch = models.CharField(max_length=100, default='Default Branch')
    total_floors = models.IntegerField(null=True, blank=True)
    total_rooms = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=20, default='active')
    # total_rooms_per_floor = models.IntegerField(null=True, blank=True)
    # number_of_beds_per_room = models.IntegerField(null=True, blank=True)
    # occupancy_rate_per_room = models.FloatField(null=True, blank=True)
    # occupied_rooms = models.IntegerField(default=0)
    # occupied_beds = models.IntegerField(default=0)

    def get_total_floors(self):  # Renamed the method
        return self.floor_set.count()


    def get_total_rooms(self):
         return Room.objects.filter(floor__hostel=self).count()
    
    def get_total_beds(self):
        return Bed.objects.filter(room__floor__hostel=self).count()
    


    def __str__(self):
        return f"{self.name} - {self.branch} - {self.status}"


class Floor(models.Model):
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE)
    floor_number = models.IntegerField()
    number_of_rooms = models.IntegerField(null=True)
    status = models.CharField(max_length=20, default='active')

    def get_total_rooms(self):
        return self.room_set.aggregate(total_rooms=models.Sum('number_of_beds'))['total_rooms'] or 0

    def __str__(self):  
        return f"Floor {self.floor_number} in {self.hostel}"

class Room(models.Model):
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE)
    room_number = models.CharField(max_length=10)
    capacity = models.IntegerField(null=True)
    max_occupancy = models.IntegerField(null=True)
    number_of_beds = models.IntegerField(null=True, default=0)
    status = models.CharField(max_length=20, default='active')


    def __str__(self):
        return f"Room {self.room_number} on Floor {self.floor.floor_number} in {self.floor.hostel}"

class HostelStats(models.Model):
    hostel = models.OneToOneField(Hostel, on_delete=models.CASCADE)
    total_floors = models.IntegerField()
    total_rooms = models.IntegerField()
    

    def __str__(self):
        return f"Stats for {self.hostel}"

class UserProfile(models.Model):
    name = models.CharField(max_length=100)
    organisation = models.CharField(max_length=100)
    branch = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    

class UserRegistration(models.Model):
    user_profile = models.ForeignKey('UserProfile', on_delete=models.CASCADE, null=True, blank=True)
    hostel = models.ForeignKey('Hostel', on_delete=models.CASCADE)
    floor = models.ForeignKey('Floor', on_delete=models.CASCADE)
    room = models.ForeignKey('Room', on_delete=models.CASCADE)
    bed = models.ForeignKey('Bed', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, default='active')
    admission_date = models.DateField(null=True, blank=True)


    def __str__(self):
        return f"{self.name} - {self.organisation} - {self.branch} - {self.hostel} - Floor {self.floor.floor_number} - Room {self.room.room_number} - Bed {self.bed.bed_number} - {self.status}"

    
class Bed(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    bed_number = models.IntegerField()
    is_occupied = models.BooleanField(default=False)
    status = models.CharField(max_length=20, default='active')

    def __str__(self):
        return f"Bed {self.bed_number} in {self.room}"


       





