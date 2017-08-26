from django.db import models


class Iteration(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Story(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    time_hours_estimate = models.IntegerField(default=0)
    iteration = models.ForeignKey(Iteration, on_delete=models.SET_NULL,
                                  null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def time_hours_actual(self):
        return sum(task.total_work for task in self.task_set.all())
    def is_completed(self):
        # TODO
        # Check if it has at least one task and if all tasks it has are
        # completed.
        pass

class Developer(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    @property
    def total_work_done(self):
        return sum(task.total_work for task in self.task_set.all())

    @property
    def total_work_estimated(self):
        return sum(task.time_hours_estimate for task in self.task_set.all())

class Task(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    completed = models.BooleanField(default=False)
    developer = models.ForeignKey(Developer, null=True, blank=True,
                                  on_delete=models.SET_NULL)
    iteration = models.ForeignKey(Iteration, null=True, blank=True,
                                  on_delete=models.SET_NULL)
    time_hours_estimate = models.IntegerField(null=False, blank=False)
    # TODO: test this behavior
    # A task cannot exist without a corresponding story
    story = models.ForeignKey(Story, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    @property
    def total_work(self):
        if self.work_set.all():
            return self.work_set.all().aggregate(
                models.Sum('time_hours'))['time_hours__sum']
        else:
            return 0

class Work(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    time_hours = models.IntegerField(null=False, blank=False)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    developer = models.ForeignKey(Developer, null=True, blank=True,
                                  on_delete=models.SET_NULL)

    def __str__(self):
        msg = "Work name: %s Hours: %d For task: %s By developer: %s." % (
            self.name, self.time_hours, self.task.name, self.developer.name
        )
        return msg
