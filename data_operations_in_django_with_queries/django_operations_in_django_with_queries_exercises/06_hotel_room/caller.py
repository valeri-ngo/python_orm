import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import HotelRoom

# Create queries within functions

HotelRoom.objects.create(
    room_number = 401,
    room_type = 'Standard',
    capacity = 2,
    amenities = 'Tv',
    price_per_night = 100.00
)

HotelRoom.objects.create(
    room_number = 501,
    room_type = 'Deluxe',
    capacity = 3,
    amenities = 'Wi-Fi',
    price_per_night = 200.00
)

HotelRoom.objects.create(
    room_number = 601,
    room_type = 'Deluxe',
    capacity = 6,
    amenities = 'Jacuzzi',
    price_per_night = 400.00
)

def get_deluxe_rooms():
    deluxe_rooms = HotelRoom.objects.filter(room_type = 'Deluxe')

    deluxe_rooms_as_even = []

    for rooms in deluxe_rooms:
        if rooms.id % 2 == 0:
            deluxe_rooms_as_even.append(
                f"Deluxe room with number {rooms.room_number} "
                f"costs {rooms.price_per_night}$ per night!")
    
    return '\n'.join(deluxe_rooms_as_even)

def increase_room_capacity():
    sorted_rooms = HotelRoom.objects.order_by('id')

    rooms = list(sorted_rooms)

    if rooms:
        first_room = rooms[0]

        if first_room.is_reserved:
            first_room.capaicity = first_room.id
        
    for i in range(1, len(rooms)):
        curr_room = rooms[i]
        prev_room = rooms[i - 1]

        if curr_room.is_reserved:
            curr_room.capacity += prev_room.capacity
            curr_room.save()

def reserve_first_room():
    first_room = HotelRoom.objects.first()

    if first_room:
        first_room.is_reserved = True
        first_room.save()

def delete_last_room():
    last_room = HotelRoom.objects.last()

    if last_room and not last_room.is_reserved:
        last_room.delete()

print(get_deluxe_rooms())
reserve_first_room()
print(HotelRoom.objects.get(room_number=401).is_reserved())
