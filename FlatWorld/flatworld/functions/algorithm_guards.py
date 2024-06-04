from random import randint
from .models import Guard, Point
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import io


def get_images(hull_points, hull_points_energy, guard_data):
    hull_points = [Point(x, y) for x, y in hull_points]
    images_data = []
    for day_data in guard_data:
        # Zbieramy punkty stop i song dla danego dnia
        stop_points = day_data["stop_points"]
        song_points = day_data["songs"] 
        print(f"stop_points: {stop_points}, song_points: {song_points}") 
        
        for i in range(len(hull_points) - 1):
            plt.plot(
                [hull_points[i].x, hull_points[i + 1].x],
                [hull_points[i].y, hull_points[i + 1].y],
                "c-",
            )
            plt.text(hull_points[i].x, hull_points[i].y, str(i + 1))

        hull_points.pop(len(hull_points) - 1)
        for i, point in enumerate(hull_points, start=1):
            if i in song_points:
                plt.plot(point.x, point.y, "ro")
            elif i in stop_points:
                plt.plot(point.x, point.y, "go")
            else:
                plt.plot(point.x, point.y, "ko")
        hull_points.append(Point(hull_points[0].x, hull_points[0].y))


        buf = io.BytesIO()
        plt.savefig(buf, format="png")
        plt.close()

        image_data = buf.getvalue()
        images_data.append(image_data)

    return images_data


def find_stop_points(max_steps, hull_points_energy):
    steps = 0
    songs = []
    stop_points = []
    for i in range(len(hull_points_energy)):
        if steps == max_steps or (
            i > 0 and hull_points_energy[i] < hull_points_energy[i - 1]
        ):
            stop_points.append(i + 1)
            if i > 0 and hull_points_energy[i] > hull_points_energy[i - 1]:
                songs.append(i + 1)
            steps = 0
        steps += 1
    if hull_points_energy[0] > hull_points_energy[-1]:
        songs.append(1)
    stop_points.append(1)
    return stop_points, songs


def generate_flat_schedule(people, hull_points_number, max_steps, hull_points):
    guards = [
        Guard(i, randint(1, 100), max_steps) for i in range(1, people + 1)
    ]
    sorted_guards = sorted(guards, key=lambda x: x.energy, reverse=True)
    # jak nie bedzie tych 7 straznikow to nie bedzie mial kto tam patrolowac brak danych jakis case dorobic
    chosen_guards = [guard for guard in sorted_guards][:7] # if guard.energy > 50
    guard_data = []
    for day, guard in enumerate(chosen_guards, start=1):
        guard.set_patrol_day(day)
        max_steps = guard.max_steps
        hull_points_energy = [
            randint(1, 100) for _ in range(hull_points_number)
        ]
        stop_points, songs = find_stop_points(max_steps, hull_points_energy)
        print(
            f"Strażnik {guard.id} zatrzymuje się na punktach {stop_points}, melodie: {songs} w dniu {day}"
        )
        guard_data.append(
            {
                "id": guard.id,
                "stop_points": stop_points,
                "songs": songs,
                "energy_points": hull_points_energy,
                "day": day,
            }
        )
    images_data = get_images(hull_points, hull_points_energy, guard_data)
    # id strraznika liste punktow i cos tam
    return guard_data, images_data
