from .models import (
    Adventure,
    Song,
    Code,
    Factory,
    Fence,
    Inhabitant,
    Guard,
    Day,
)
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from django.views import View
from django.shortcuts import render
from django.views.generic import TemplateView
from io import BytesIO
from django.core.files import File
from django.conf import settings
import os
import time
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from rest_framework import status
from rest_framework.exceptions import APIException
from django.core import serializers


from .functions.algorithm_graham import calculate_hull
from .functions.factory import generate_factory
from .functions.bearers import generate_bearers
from .functions.generate_fence import visualize_fence
from .functions.generate_song import generate_song
from .functions.algorithm_dinic import calculate_cost
from .functions.algorithm_rabinkarp import rabinkarp
from .functions.algorithm_huffman import code_song
from .functions.algorithm_guards import generate_flat_schedule


class IndexView(TemplateView):
    def get(self, request):
        adventure_exists = Adventure.objects.filter(id=1).exists()
        return render(
            request,
            "flatworld/index.html",
            {"adventure_exists": adventure_exists},
        )


class ContinueView(View):
    def get(self, request):
        try:
            adventure = Adventure.objects.get(id=1)
        except Adventure.DoesNotExist:
            return render(request, "flatworld/error.html")
        if not adventure.bearers or not adventure.factory:
            return FactoryView.get(self, request)
        if not adventure.fence:
            return FenceView.get(self, request)
        return FenceView.get(self, request)


class ResetView(APIView):
    def post(self, request):
        try:
            adventure = Adventure.objects.get(id=1)
            fence  = Fence.objects.get(id=1)
            days = Day.objects.all()

            if adventure.world and default_storage.exists(
                adventure.world.name
            ):
                default_storage.delete(adventure.world.name)
                adventure.world = None
                adventure.save()

            if fence.fence:
                if fence.fence:
                    if default_storage.exists(fence.fence.name):
                        default_storage.delete(fence.fence.name)
                    fence.fence = None
                    fence.save()

                adventure.fence.set([])
            for day in days:
                if day.image:
                    if default_storage.exists(day.image.name):
                        default_storage.delete(day.image.name)
                    day.image = None
                    day.save()
                day.delete()

            adventure.delete()
            return Response({"message": "Przygoda została zresetowana."})
        except Adventure.DoesNotExist:
            return Response({"message": "No adventure to reset."})

    def get(self, request):
        adventure_exists = Adventure.objects.filter(id=1).exists()
        return Response({"adventure_exists": adventure_exists})

    def get_plot_path(self, filename):
        return os.path.join(settings.MEDIA_ROOT, "images", filename)


class GenerateWorldView(APIView):
    def get(self, request):
        try:
            adventure = Adventure.objects.get(id=1)
            return render(
                request,
                "flatworld/world.html",
                {
                    "world": adventure.world,
                    "world_points": len(adventure.world_points),
                    "hull_points": len(adventure.hull_points) - 1,
                },
            )
        except Adventure.DoesNotExist:
            return render(
                request, "flatworld/world.html", {"world_exists": False}
            )

    def post(self, request):
        input_points = request.data.get("inputPoints")
        if not input_points:
            return Response({"error": "inputPoints is required"}, status=400)
        try:
            input_points = int(input_points)
        except ValueError:
            return Response(
                {"error": "inputPoints must be an integer"}, status=400
            )

        image_data, world_points, hull_points = calculate_hull(input_points)
        hull = BytesIO(image_data)
        hull.seek(0)
        world_points = [tuple(point) for point in world_points]
        hull_points = [tuple(point) for point in hull_points]

        adventure, created = Adventure.objects.get_or_create(
            id=1,
            defaults={
                "world_points": world_points,
                "hull_points": hull_points,
            },
        )
        if not created:
            adventure.world_points = world_points
            adventure.hull_points = hull_points
            adventure.save()

        filename = "plot_{}.png".format(int(time.time()))
        adventure.world.save(filename, File(hull))
        world_url = adventure.world.url
        return JsonResponse({"world_url": world_url})


class SongView(APIView):
    def get(self, request):
        try:
            adventure = Adventure.objects.get(id=1)
            song, created = Song.objects.get_or_create(
                id=1, adventure=adventure
            )
            song.adventure = adventure
            print(song.song == None)
            if song.song is None:
                melody = generate_song()
                print(melody)
                song.song = melody
                song.save()
            song_words = song.song.split()
            indexes = (
                [str(index + 1) for index in song.song_index]
                if song.song_index
                else []
            )
            changed_song = (
                song.changed_song.split() if song.changed_song else []
            )
            return render(
                request,
                "flatworld/song.html",
                {
                    "song_words": song_words,
                    "changed_song": changed_song,
                    "indexes": indexes,
                },
            )
        except Adventure.DoesNotExist:
            return render(request, "flatworld/error.html")

    def post(self, request):
        to_change = self.request.data.get("word_to_change")
        adventure = Adventure.objects.get(id=1)
        song, created = Song.objects.get_or_create(id=1, adventure=adventure)
        song.adventure = adventure
        indexes, changed_song, word_indexes, changed_word = rabinkarp(
            to_change, song.song
        )
        song.changed_song = changed_song
        song.song_index = word_indexes
        song.save()
        return JsonResponse(
            {
                "indexes": indexes,
                "changed_song": changed_song,
                "word_indexes": word_indexes,
                "changed_word": changed_word,
            }
        )


class CodingView(APIView):
    def get(self, request):
        try:
            adventure = Adventure.objects.get(id=1)
            song, created = Song.objects.get_or_create(
                id=1, adventure=adventure
            )
            code, created = Code.objects.get_or_create(
                id=1, adventure=adventure
            )
            if not song.song:
                return render(request, "flatworld/error.html")
            if "code" in request.GET:
                song_to_code = song.song
                code_dict, coded_song, uncoded_song = code_song(song_to_code)
                code.code = code_dict
                code.coded_song = coded_song
                code.uncoded_song = uncoded_song
                code.save()
                return JsonResponse(
                    {
                        "coded_song": coded_song,
                        "code": code_dict,
                        "uncoded_song": uncoded_song,
                    }
                )
            else:
                if not adventure.song:
                    return render(request, "flatworld/error.html")
                return render(
                    request,
                    "flatworld/coding.html",
                    {
                        "uncoded_song": code.uncoded_song,
                        "code": code.code,
                        "newline": "\n",
                        "coded_song": code.coded_song,
                    },
                )
        except Adventure.DoesNotExist:
            return render(request, "flatworld/error.html")

    def post(self, request):
        adventure = Adventure.objects.get(id=1)
        code, created = Code.objects.get_or_create(id=1, adventure=adventure)
        song_to_code = request.data.get("song_to_code")
        code_dict, coded_song, uncoded_song = code_song(song_to_code)
        code.code = code_dict
        code.coded_song = coded_song
        code.uncoded_song = uncoded_song
        code.save()
        return JsonResponse(
            {
                "coded_song": coded_song,
                "code": code_dict,
                "uncoded_song": uncoded_song,
            }
        )


class FactoryView(APIView):
    def get(self, request):
        try:
            adventure = Adventure.objects.get(id=1)
            factory, created = Factory.objects.get_or_create(
                id=1, adventure=adventure
            )
            inhabitants, created = Inhabitant.objects.get_or_create(
                id=1, adventure=adventure
            )
            return render(
                request,
                "flatworld/bearersAndFactory.html",
                {
                    "factory": factory.factory,
                    "bearers": inhabitants.bearers,
                },
            )
        except Adventure.DoesNotExist:
            return render(request, "flatworld/error.html")

    def post(self, request):
        adventure = Adventure.objects.get(id=1)
        factory, created = Factory.objects.get_or_create(
            id=1, adventure=adventure
        )
        hull_points = adventure.hull_points
        factory_point = generate_factory(hull_points)
        factory.factory = [factory_point.x, factory_point.y]
        factory.save()
        print(factory_point)
        return JsonResponse({"factory": [factory_point.x, factory_point.y]})


class BearersView(APIView):
    def post(self, request):
        inputPoints = request.data.get("inputPoints")
        if not inputPoints:
            raise Response({"error": "inputPoints is required"}, status=400)
        try:
            inputPoints = int(inputPoints)
        except ValueError:
            raise Response(
                {"error": "inputPoints must be an integer"}, status=400
            )
        adventure = Adventure.objects.get(id=1)
        inhabitants, created = Inhabitant.objects.get_or_create(
            id=1, adventure=adventure
        )
        pairs, people = generate_bearers(inputPoints)
        people = [person.to_dict() for person in people]

        inhabitants.bearers = pairs
        inhabitants.inhabitants = people
        inhabitants.save()
        return JsonResponse({"pairs": pairs})


class FenceView(APIView):
    def get(self, request):
        try:
            adventure = Adventure.objects.get(id=1)
            fence, created = Fence.objects.get_or_create(
                id=1, adventure=adventure
            )
            inhabitants, created = Inhabitant.objects.get_or_create(
                id=1, adventure=adventure
            )
            factory, created = Factory.objects.get_or_create(
                id=1, adventure=adventure
            )
            if "fence" in request.GET:
                world_points = adventure.world_points
                hull_points = adventure.hull_points
                pairs = inhabitants.bearers
                neighbors = fence.fence_neighbors
                cost = calculate_cost(
                    hull_points, world_points, pairs, neighbors
                )
                return JsonResponse({"cost": cost})

            else:
                if not inhabitants.bearers or not factory.factory:
                    return render(request, "flatworld/error.html")
                if not fence.fence:
                    world_points = adventure.world_points
                    hull_points = adventure.hull_points
                    factory = factory.factory

                    image_data, neighbors, matrix = visualize_fence(
                        world_points, factory, hull_points
                    )
                    neighbors = {
                        int(key): [int(i) for i in value]
                        for key, value in neighbors.items()
                    }
                    matrix = [
                        [int(element) for element in row] for row in matrix
                    ]
                    filename = "fence_{}.png".format(int(time.time()))
                    fence.fence.save(filename, ContentFile(image_data))
                    fence.fence_neighbors = neighbors
                    fence.neighbors_matrix = matrix
                    fence.save()
                fence_url = fence.fence
                return render(
                    request,
                    "flatworld/fence.html",
                    {
                        "fence_cost": fence.fence_cost,
                        "fence": fence_url,
                        "neighbors": fence.fence_neighbors,
                    },
                )
        except Adventure.DoesNotExist:
            return render(request, "flatworld/error.html")

    def post(self, request):
        pass


class GuardsView(APIView):
    def get(self, request):
        try:
            if not Inhabitant.objects.get(id=1).inhabitants or not Fence.objects.get(id=1).fence:
                return render(request, "flatworld/error.html")
            return render(
                request,
                "flatworld/guards.html",
                {
                    "steps": Guard.objects.values_list('steps', flat=True).first(),
                    "days": Day.objects.all(),
                },
            )
        except (Adventure.DoesNotExist, Inhabitant.DoesNotExist, Fence.DoesNotExist):
            return render(request, "flatworld/error.html")

    def post(self, request):
        adventure = Adventure.objects.get(id=1)
        guards, created = Guard.objects.get_or_create(
            id=1, adventure=adventure
        )
        inhabitants, created = Inhabitant.objects.get_or_create(
            id=1, adventure=adventure
        )
        inputPoints = request.data.get("inputPoints")
        if not inputPoints:
            raise Response(
                {"error": "inputPoints is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            inputPoints = int(inputPoints)
        except ValueError:
            raise Response(
                {"error": "inputPoints must be an integer"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        guard_data, images_data = generate_flat_schedule(
            int(len(inhabitants.inhabitants)),
            int(len(adventure.hull_points) - 1),
            int(inputPoints),
            adventure.hull_points,
        )
        guards.steps = inputPoints
        guards.save()
        last_day_id = Day.objects.all().order_by('-id').first().id if Day.objects.all().exists() else 0
        day_data = []

        for i, image in enumerate(images_data, start=1):
            day = Day.objects.create(
                id=last_day_id + i, 
                guard=guards, 
                day=i, 
                person_id=guard_data[i - 1]["id"], 
                stop_points=guard_data[i - 1]["stop_points"], 
                songs=guard_data[i - 1]["songs"]
            )
            filename = "fence_{i}.png".format(i=i)
            day.image.save(filename, ContentFile(image))
            day_data.append({
                "day_id": day.id,
                "person_id": day.person_id,
                "stop_points": day.stop_points,
                "songs": day.songs,
                "image": day.image.url if day.image else None,
            })

        return JsonResponse(day_data, safe=False)
