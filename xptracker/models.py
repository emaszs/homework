from django.db import models

class Iteration(models.Model):
    name = models.CharField(max_length=100)

    @property
    def total_work(self):
        return sum(task.total_work for task in self.task_set.all())

    @property
    def total_work_estimate(self):
        return sum(task.time_hours_estimate for task in self.task_set.all())

    def participating_developers(self):
        """
        Get all developers with tasks this iteration
        """
        return [task.developer for task in self.task_set.all()]

    def __str__(self):
        return self.name


class Story(models.Model):
    name = models.CharField(max_length=100)
    time_hours_estimate = models.FloatField(default=0)
    iteration = models.ForeignKey(Iteration, on_delete=models.SET_NULL,
                                  null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def total_work(self):
        return sum(task.total_work for task in self.task_set.all())

class Developer(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    @property
    def total_work(self):
        return sum(work.time_hours for work in self.work_set.all())

    @property
    def total_work_estimate(self):
        return sum(task.time_hours_estimate for task in self.task_set.all())

class Task(models.Model):
    name = models.CharField(max_length=100)
    developer = models.ForeignKey(Developer, null=True, blank=True,
                                  on_delete=models.SET_NULL)
    iteration = models.ForeignKey(Iteration, null=True, blank=True,
                                  on_delete=models.SET_NULL)
    time_hours_estimate = models.FloatField(null=False, blank=False)
    story = models.ForeignKey(Story, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    @property
    def total_work(self):
        return sum(work.time_hours for work in self.work_set.all())

class Work(models.Model):
    name = models.CharField(max_length=100)
    create_time = models.DateTimeField(auto_now=True, blank=True)
    time_hours = models.FloatField(null=False, blank=False)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    developer = models.ForeignKey(Developer, null=True, blank=True,
                                  on_delete=models.CASCADE)

    def __str__(self):
        return self.name
