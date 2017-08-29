from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver
from selenium.webdriver.support.ui import Select

from xptracker.models import Developer, Story, Work, Task, Iteration
from xptracker.tests_unit import create_developer, create_story, create_work, \
    create_iteration, create_task


class IndexTestCase(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(1)
        super(IndexTestCase, self).setUp()

    def tearDown(self):
        self.browser.quit()
        super(IndexTestCase, self).tearDown()

    def create_task_ui(self, name, developer, iteration, estimate, story):
        """
        Helper method for creating a task
        """
        self.browser.get(self.live_server_url+'/xptracker/')
        link = self.browser.find_element_by_link_text('Create new task')
        link.click()

        name_field = self.browser.find_element_by_id('id_name')
        name_field.send_keys(name)
        story_select = Select(self.browser.
                                  find_element_by_id('id_story'))
        story_select.select_by_visible_text(story)
        developer_select = Select(self.browser.
                                  find_element_by_id('id_developer'))
        developer_select.select_by_visible_text(developer)
        iteration_select = Select(self.browser.
                                  find_element_by_id('id_iteration'))
        iteration_select.select_by_visible_text(iteration)
        estimate_field = (self.browser.
                          find_element_by_id('id_time_hours_estimate'))
        estimate_field.send_keys(estimate)
        self.browser.find_element_by_tag_name('form').submit()

    def create_developer_ui(self, name):
        """
        Helper method for adding a new developer
        """
        self.browser.get(self.live_server_url+'/xptracker/')
        link = self.browser.find_element_by_link_text('Add developer')
        link.click()

        name_field = self.browser.find_element_by_id('id_name')
        name_field.send_keys(name)
        self.browser.find_element_by_tag_name('form').submit()

    def create_story_ui(self, name, iteration, estimate):
        """
        Helper method for creating a new story
        """
        self.browser.get(self.live_server_url+'/xptracker/')
        link = self.browser.find_element_by_link_text('Create new story')
        link.click()

        name_field = self.browser.find_element_by_id('id_name')
        name_field.send_keys(name)
        iteration_select = Select(self.browser.
                                  find_element_by_id('id_iteration'))
        iteration_select.select_by_visible_text(iteration)
        estimate_field = (self.browser.
                          find_element_by_id('id_time_hours_estimate'))
        estimate_field.send_keys(estimate)
        self.browser.find_element_by_tag_name('form').submit()

    def create_work_ui(self, name, hours, task, developer):
        """
        Helper method for creating work
        """
        self.browser.get(self.live_server_url+'/xptracker/')
        link = self.browser.find_element_by_link_text('Add work')
        link.click()

        name_field = self.browser.find_element_by_id('id_name')
        name_field.send_keys(name)
        time_field = self.browser.find_element_by_id('id_time_hours')
        time_field.send_keys(hours)
        task_select = Select(self.browser.find_element_by_id('id_task'))
        task_select.select_by_visible_text(task)
        developer_select = Select(self.browser.find_element_by_id('id_developer'))
        developer_select.select_by_visible_text(developer)
        self.browser.find_element_by_tag_name('form').submit()

    def create_iteration_ui(self, name):
        """
        Helper method for creating iterations on a live webpage.
        """
        self.browser.get(self.live_server_url+'/xptracker/')
        link = self.browser.find_element_by_link_text('Create new iteration')
        link.click()

        name_field = self.browser.find_element_by_id('id_name')
        name_field.send_keys(name)

        self.browser.find_element_by_tag_name('form').submit()

    def test_create_iteration(self):
        """
        New iteration is displayed in the index page.
        """

        self.create_iteration_ui('zero')

        element = self.browser.find_element_by_tag_name('ul')
        assert element.text == 'zero'

    def test_create_developer(self):
        """
        New developer is displayed in the index page.
        """

        self.create_developer_ui('Tommy')
        element = self.browser.find_element_by_tag_name('ul')
        assert element.text == 'Tommy'

    def test_create_story(self):
        """
        New story is displayed in the index page.
        """
        self.create_iteration_ui('zero')
        self.create_story_ui('Simple story', 'zero', '10')

        element = self.browser.find_element_by_tag_name('table')
        assert 'Simple story' in element.text

    def test_create_task(self):
        """
        New task is displayed in a table in the index page.
        """
        self.create_iteration_ui('zero')
        self.create_developer_ui('Tommy')
        self.create_story_ui('Best story', 'zero', '20')
        self.create_task_ui('Best task', 'Tommy', 'zero', '10', 'Best story')

        element = self.browser.find_element_by_id('task-table')
        assert 'Best task' in element.text

    def test_create_work(self):
        """
        New work entry is displayed in a table in the index page.
        """
        self.create_iteration_ui('zero')
        self.create_developer_ui('Tommy')
        self.create_story_ui('Best story', 'zero', '10')
        self.create_task_ui('Best task', 'Tommy', 'zero', '10', 'Best story')
        self.create_work_ui('Best work', '5', 'Best task', 'Tommy')

        element = self.browser.find_element_by_id('work-table')
        assert 'Best work' in element.text

    def test_create_work_through_shortcut(self):
        """
        Shortcuts for adding work are generated correctly.
        """
        self.create_iteration_ui('zero')
        self.create_developer_ui('Tommy')
        self.create_story_ui('Best story', 'zero', '10')
        self.create_task_ui('Best task', 'Tommy', 'zero', '10', 'Best story')

        add_work_link = self.browser.find_element_by_link_text('++')
        add_work_link.click()

        name_field = self.browser.find_element_by_id('id_name')
        name_field.send_keys('Best work')
        time_field = self.browser.find_element_by_id('id_time_hours')
        time_field.send_keys('10')
        self.browser.find_element_by_tag_name('form').submit()

        element = self.browser.find_element_by_id('work-table')
        assert 'Best work' in element.text

class IterationTimeSummaryTestCase(StaticLiveServerTestCase):

    def setUp(self):
        """
        Two developers with work split across two iterations.
        """
        dev1 = create_developer('Tommy')
        dev2 = create_developer('Jerry')
        iteration1 = create_iteration('zero')
        story1 = create_story('Best story', iteration1, 10)
        task1 = create_task('Best task', dev1, iteration1, 2, story1)
        task2 = create_task('Another task', dev2, iteration1, 2, story1)
        create_work('Some work from dev1', 1, task1, dev1)
        create_work('More work from dev1', 1, task1, dev1)
        create_work('Some work from dev2', 1, task2, dev2)

        iteration2 = create_iteration('misc')
        story2 = create_story('Worst story',iteration2, 1)
        task3 = create_task('Best task', dev1, iteration2, 2, story2)
        task4 = create_task('Another task', dev2, iteration2, 2, story2)
        create_work('Unrelated work from dev1', 1, task3, dev1)
        create_work('Unrelated work from dev2', 1, task4, dev2)

        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(1)
        super(IterationTimeSummaryTestCase, self).setUp()

    def tearDown(self):
        self.browser.quit()
        super(IterationTimeSummaryTestCase, self).tearDown()

    def test_iteration_time_summary(self):
        """
        Time estimate totals and actual work totals are displayed correctly
        in the iteration detail page based on how much work each developer did
        for this iteration.
        """
        self.browser.get(self.live_server_url+'/xptracker/')

        link = self.browser.find_element_by_link_text('zero')

        link.click()
        element1 = self.browser.find_element_by_id(
            'totals-task-work-estimate-cell')
        assert element1.text == '4.0'
        element2 = self.browser.find_element_by_id(
            'totals-task-work-cell')
        assert element2.text == '3.0'
