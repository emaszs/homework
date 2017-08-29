# xptracker 

### Project files description:
   * `homework/xptracker/templates/xptracker/` contains the Django templates that are compiled into HTML as needed.
   * `homework/xptracker/templates/xptracker/` contains some less than interesting static files such as a primitive style.css stylesheet as well as a favicon.
   * `homework/xptracker/tests_unit.py` contains unit tests, `/homework/xptracker/tests_selenium.py` contains  some functional tests that rely on Selenium.
   * `homework/xptracker/urls.py` contains the main routing rules. (On top of `homework/homework/urls.py` of course.)
   * `homework/xptracker/views.py` contains all of the view descriptions.
   
### Pre-requisites to run
   * Have Python 2.7-3.6 installed.
   * Have Django installed (code written on Django 1.11.4, Python 3.6), can be done with `pip install Django` either system-wide or in a [virtualenv](https://virtualenv.pypa.io/en/stable/).
   * (Optional) Have Selenium installed in order to run the functional test suite, tests written on Selenium 3.5.0
   * (Optional) Can also be imported as an Eclipse Pydev project
   
### To run:
   * `git clone https://github.com/emaszs/homework.git` in a local directory, ex `/home/Tommy/repos/`.
   * run `python homework/manage.py migrate --run-syncdb` to create an empty sqlite database
   * run `python /home/Tommy/repos/homework/manage.py runserver`.
   * Navigate to http://127.0.0.1:8000/xptracker in your web browser.
   
### Usage:
   * Click 'Add developer' and create a new developer
   * Click 'Create new iteration' to create a new iteration which can have stories and tasks assigned to it.
   * Click 'Create new story' and add a new story, you should set which iteration it belongs to and provide a time estimate needed to complete the story requirements.
   * Click 'Create new task' to add a new task, you should assign it to an existing developer and set which story and iteration the task is a part of. The task should also have an estimate of time needed to complete it by the assigned developer.
   * Click 'Add work' or the '++' shortcut near one of the tasks to create a work entry, which shows that a certain developer has contributed a certain amount of time to the set task.
   * The developer names listed at the top of the page link to the developer detail page. The developer detail page lists the developer's assigned tasks, how much work the developer has estimated is needed to be done as well has how much work the developer has actually done on each task.
   * The iteration names listed at the bottom of the page link to the iteration detail page. The iteration detail page lists the developers that have participated in the iteration (developers that have tasks assigned in the iteration), how much work they have estimated needs to be done as well as how much work they have actually done.


### Screenshot:
![screenshot](https://i.imgur.com/tn0O4ta.png)
