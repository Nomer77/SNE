rooms = {5678: (733,), 'Что-то': (89,), 'фыфв 9:00': (32400,), 'sdq 10:23': (37380,)}
sorted_rooms = dict(sorted(rooms.items(), key=lambda item: item[1]))
print(sorted_rooms)