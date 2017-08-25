from django.db import models


class Iteration(models.Model):
    # TODO: Maybe iteration names should be ints?
    name = models.CharField(max_length=20)
    date_start = models.DateField('start date')
    date_end = models.DateField('end date')

    def __str__(self):
        return self.name


class Story(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=10000)
    time_hours_estimate = models.IntegerField(default=0)
    time_hours_actual = models.IntegerField(default=0)
    # Can check if completed by existence of subtasks
    #completed = models.BooleanField(default=False)
    iteration = models.ForeignKey(Iteration, on_delete=models.SET_NULL,
                                  null=True, blank=True)

    def __str__(self):
        return self.name


class Developer(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Task(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=10000)
    completed = models.BooleanField(default=False)
    developer = models.ForeignKey(Developer, null=True, blank=True)
    story = models.ForeignKey(Story)

    def __str__(self):
        return self.name

