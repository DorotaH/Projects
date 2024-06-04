from django.db import models


class Adventure(models.Model):
    world = models.ImageField(upload_to="images/", default="")
    hull_points = models.JSONField(null=True, blank=True)
    world_points = models.JSONField(null=True, blank=True)


class Song(models.Model):
    adventure = models.ForeignKey(
        Adventure, on_delete=models.CASCADE, related_name="song"
    )
    song = models.CharField(max_length=1255, null=True)
    song_index = models.JSONField(null=True, blank=True)
    changed_song = models.CharField(max_length=100, null=True)


class Code(models.Model):
    adventure = models.ForeignKey(
        Adventure, on_delete=models.CASCADE, related_name="code"
    )
    code = models.JSONField(null=True, blank=True)
    coded_song = models.CharField(max_length=100, null=True)
    uncoded_song = models.CharField(max_length=100, null=True)


class Inhabitant(models.Model):
    adventure = models.ForeignKey(
        Adventure, on_delete=models.CASCADE, related_name="inhabitant"
    )
    inhabitants = models.JSONField(null=True, blank=True)
    bearers = models.IntegerField(null=True)


class Factory(models.Model):
    adventure = models.ForeignKey(
        Adventure, on_delete=models.CASCADE, related_name="factory"
    )
    factory = models.JSONField(null=True, blank=True)


class Fence(models.Model):
    adventure = models.ForeignKey(
        Adventure, on_delete=models.CASCADE, related_name="fence"
    )
    fence = models.ImageField(upload_to="images/", default="")
    fence_neighbors = models.JSONField(null=True, blank=True)
    neighbors_matrix = models.JSONField(null=True, blank=True)
    fence_cost = models.DecimalField(
        max_digits=10, decimal_places=2, null=True
    )


class Guard(models.Model):
    adventure = models.ForeignKey(
        Adventure, on_delete=models.CASCADE, related_name="guard"
    )
    steps = models.IntegerField(null=True)


class Day(models.Model):
    guard = models.ForeignKey(
        Guard, on_delete=models.CASCADE, related_name="days"
    )
    day = models.IntegerField(null=True, blank=True)
    person_id = models.IntegerField(null=True, blank=True)
    stop_points = models.JSONField(null=True, blank=True)
    songs = models.JSONField(null=True, blank=True)
    image = models.ImageField(upload_to="images/", default="")
