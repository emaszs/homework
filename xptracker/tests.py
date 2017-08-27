from django.test import TestCase

from xptracker.models import Developer, Story, Work, Task, Iteration

def create_task(name, developer, iteration, estimate, story):
    return Task.objects.create(name=name, developer=developer,
                               iteration=iteration,
                               time_hours_estimate=estimate, story=story)

def create_developer(name):
    return Developer.objects.create(name=name)

def create_story(name, iteration, estimate):
    return Story.objects.create(name=name, iteration=iteration,
                                time_hours_estimate=estimate)

def create_work(name, hours, task, developer):
    return Work.objects.create(name=name, time_hours=hours, task=task,
                               developer=developer)

def create_iteration(name):
    return Iteration.objects.create(name=name)

class HelperFunctionTests(TestCase):
    def test_create(self):
        """
        Creating a few related model objects
        """
        dev = create_developer('Tommy')
        iteration = create_iteration('zero')
        story = create_story('Comments should look nice', iteration, 20)
        task = create_task('Pylint the comments', dev, iteration, 5, story)
        work = create_work('Pylinted the whole day', 10, task, dev)

        self.assertEqual(str(Developer.objects.all()[0]), 'Tommy')
        self.assertEqual(dev.task_set.all()[0].name, 'Pylint the comments')
        self.assertEqual(task.work_set.all()[0].name, 'Pylinted the whole day')
        self.assertEqual(task.story.name, 'Comments should look nice')
        self.assertEqual(story.iteration.name, 'zero')
        self.assertEqual(work.time_hours, 10)

    def test_delete_story(self):
        """
        Deleting a Story object should delete all of it's tasks and work done
        on those tasks.
        """
        dev = create_developer('Tommy')
        iteration = create_iteration('zero')
        story = create_story('Comments should look nice', iteration, 20)
        task = create_task('Pylint the comments', dev, iteration, 5, story)
        create_work('Pylinted the whole day', 10, task, dev)

        story.delete()

        self.assertEqual(len(Story.objects.all()), 0)
        self.assertEqual(len(Task.objects.all()), 0)
        self.assertEqual(len(Work.objects.all()), 0)


class TaskModelTests(TestCase):
    def test_total_task_work_done_when_work_is_empty(self):
        """
        If a Task object has no related work done, it's total_work property
        should be zero.
        """
        iteration = create_iteration('zero')
        story = create_story('Blue background', iteration, 42)
        task = create_task('Make the background dark blue', None, iteration, 5,
                           story)

        self.assertEqual(task.total_work, 0)

    def test_total_task_work_done_with_one_work_entry(self):
        """
        If a task has one work entry, the total time spent on this task is equal
        to the work entry time
        """
        iteration = create_iteration('zero')
        story = create_story('Kitten banner', iteration, 1)
        dev = create_developer('Tommy')
        task = create_task('Find a kitten to use as a banner', None, iteration,
                           5, story)
        create_work('Google', 2, task, dev)

        self.assertEqual(task.total_work, 2)

    def test_total_work_with_multiple_entries_from_one_dev(self):
        """
        Total work done on a task is equal to the sum of work done on
        all work entries.
        """
        iteration = create_iteration('zero')
        story = create_story('Kitten banner', iteration, 1)
        dev = create_developer('Tommy')
        task = create_task('Find a kitten to use as a banner', dev, iteration,
                           5, story)

        create_work('Google', 2, task, dev)
        create_work('Implement', 3, task, dev)

        self.assertEqual(task.total_work, 5)

    def test_total_work_with_multiple_work_entries_from_different_devs(self):
        """
        Total work done on a task is equal to the sum of work done on
        all work entries from all developers.
        """
        iteration = create_iteration('zero')
        story = create_story('Kitten banner', iteration, 1)
        dev1 = create_developer('Tommy')
        task = create_task('Find a kitten to use as a banner', dev1, iteration,
                           5, story)
        create_work('Google', 2, task, dev1)

        dev2 = create_developer('Jimmy')
        create_work('Google some more', 2, task, dev2)

        self.assertEqual(task.total_work, 4)

class StoryModelTests(TestCase):
    def test_total_work_with_no_tasks(self):
        """
        If a story has no associated tasks, it's total work is equal to zero
        """
        iteration = create_iteration('zero')
        story = create_story('Responsive ads', iteration, 15)

        self.assertEqual(story.total_work, 0)

    def test_total_work_with_no_work_entries(self):
        """
        If a story has some associated tasks but no actual work entries,
        the stories' total work is equal to zero.
        """
        iteration = create_iteration('zero')
        dev = create_developer('Tommy')
        story = create_story('Responsive scrollbars', iteration, 15)
        create_task('Read the docs', dev, iteration, 10, story)
        create_task('Make scrollbars responsive', dev, iteration, 10, story)

        self.assertEqual(story.total_work, 0)

    def test_total_work_with_one_task_and_few_work_entries(self):
        """
        The total work done for a story is equal to the sum of all work done for
        for all related tasks (in this case a single task).
        """
        iteration = create_iteration('zero')
        dev = create_developer('Tommy')
        story = create_story('Stop people stealing the images', iteration, 15)
        t1 = create_task('Disable right click', dev, iteration, 100, story)

        create_work('Google', 5, t1, dev)
        create_work('This is pointless', 5, t1, dev)
        create_work('Disable right click', 5, t1, dev)

        self.assertEqual(story.total_work, 15)

    def test_total_work_with_few_tasks_and_few_work_entries(self):
        """
        The total work done for a story is equal to the sum of all work done for
        all related tasks.
        """
        iteration = create_iteration('zero')
        dev1 = create_developer('Tommy')
        dev2 = create_developer('Jimmy')
        story = create_story('Stop people stealing the images', iteration, 15)
        t1 = create_task('Disable right click', dev1, iteration, 100, story)
        t2 = create_task('Disable hotlinking', dev2, iteration, 100, story)

        create_work('Google', 5, t1, dev1)
        create_work('This is pointless', 5, t1, dev1)
        create_work('Disable right click', 5, t1, dev1)

        create_work('Disable hotlinks', 5, t2, dev2)

        self.assertEqual(story.total_work, 20)

class DeveloperModelTests(TestCase):
    def test_total_work_with_no_work_entries(self):
        """
        Developer's total work done is equal to zero if the developer does not
        have any work entries
        """
        dev = create_developer('Tommy')
        self.assertEqual(dev.total_work, 0)

    def test_total_work_with_few_work_entries(self):
        """
        Developer's total work is equal to the sum of his/hers work entries'
        hours
        """
        iteration = create_iteration('zero')
        dev = create_developer('Tommy')
        story = create_story('Balance the amounts of cat and dog pictures',
                            iteration, 15)
        task = create_task('Add more dog pics', dev, iteration, 1, story)

        create_work('Adding more dog pics', 1, task, dev)
        create_work('Adding more dog pics', 1, task, dev)

        self.assertEqual(dev.total_work, 2)

    def test_total_work_from_multiple_devs(self):
        """
        If two developers work on the same task, their total work is counted
        separately by their work entries.
        """
        iteration = create_iteration('zero')
        dev1 = create_developer('Tommy')
        dev2 = create_developer('Jimmy')
        story = create_story('Balance the amounts of cat and dog pictures',
                             iteration, 15)
        task = create_task('Add more dog pics', dev1, iteration, 1, story)
        create_work('Adding more dog pics', 1, task, dev1)
        create_work('Adding more cat pics', 2, task, dev2)
        create_work('Adding more dog pics', 1, task, dev1)

        self.assertEqual(dev1.total_work, 2)
        self.assertEqual(dev2.total_work, 2)

    def test_total_work_estimate_for_no_tasks(self):
        """
        The developer's total work estimate sum is equal to zero when he/she
        has no tasks assigned.
        """
        dev1 = create_developer('Tommy')

        self.assertEqual(dev1.total_work_estimate, 0)

    def test_total_work_estimate_for_few_tasks(self):
        """
        The developer's total work estimate is equal to the sum of needed time
        estimated to complete the assigned tasks.
        """
        iteration = create_iteration('zero')
        dev = create_developer('Tommy')
        story1 = create_story('Balance the amounts of cat and dog pictures',
                             iteration, 15)
        story2 = create_story('Cats and dogs are not the only animals',
                             iteration, 10)

        t1 = create_task('Add more dog pics', dev, iteration, 1, story1)
        t2 = create_task('Find more animals', dev, iteration, 1, story2)

        create_work('Adding more dog pics', 1, t1, dev)
        create_work('Google', 1, t2, dev)

        self.assertEqual(dev.total_work, 2)
