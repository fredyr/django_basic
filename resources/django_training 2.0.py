
"""
DJANGO TRAINING

``Django - The Web Framework for perfectionists with deadlines``

Introduction

-   What is DJANGO
-   Framework vs Library

-   Background, Lawrence Journal etc
-   Adrian Holovaty and Jacob Kaplan-Moss

From the Django site:
-   Django was designed to handle two challenges:
    1. the intensive deadlines of a newsroom and
    2. the stringent requirements of the experienced Web developers who wrote
    it.

    It lets you build high-performing, elegant Web applications quickly.

-   Automate as much as possible
-   DRY, Don't Repeat Yourself

DJANGO PARTS

-   Object-relational mapper, define your models in Python
-   Elegant URL design
-   Template System
-   Model, View, Template

-   Automatic admin interface
-   Users and authentication module

-   Lightweight development/test web server
-   Middleware library, hooks into Django's request/response processing
-   Internationalization System
-   Caching framework

"""

# django-admin.py startproject demo
# tree
# .
# └── demo
#     ├── demo
#     │   ├── __init__.py
#     │   ├── settings.py
#     │   ├── urls.py
#     │   └── wsgi.py
#     └── manage.py

"""
MANAGEMENT COMMANDS

-   manage.py lets you interact with the Django project

    ./manage.py shell - starts an Python shell and imports your settings
        so you can access everything inside the Django project

    ./manage.py runserver - start the development server

    ./manage.py startapp - Django apps are “pluggable”: You can use an app in
        multiple projects, and you can distribute apps, because they don’t have
        to be tied to a given Django installation.



"""

# chmod +x manage.py
# ./manage startapp polls
# tree

# └── polls
#     ├── __init__.py
#     ├── models.py
#     ├── tests.py
#     └── views.py

# Add polls to INSTALLED_APPS in settings.py


"""
TIME FOR SOME MV.. erhm MTV
    - Model
    - Template
    - View


Browser => 1. URL dispatcher => 2. View => 3. Model => Database

1.  The url dispatcher (urls.py) maps the requested url to a View class (or
    function)
2.  The view (views.py) performs the requested action for example reading or
    writing to the database
3.  The model (models.py) defines the data in Python and interacts with it.
    Typically a relational database


Model => 4. View => 5. Template => Browser

4.  After performing any requested tasks the view returns an HTTP response
    object after passing the data through a template
5.  A template typically returns Html

"""


"""
ORM - models.py
"""


class Poll:
    pass
# - question, CharField
# - pub_date, DateTimeField


class Choice:
    pass
# - poll, ForeignKey
# - choice_text, CharField
# - votes, IntegerField


# ./manage.py sql polls

# Add required parameters to models
# Add a database connection in settings.py

"""
ORM - Things to note here

    - Table names are generated from the app and class name
    - Primary keys are added
    - The SQL is tailored to the database you're using

"""

# Create a new database with our models!
# ./manage.py syncdb

"""
LEARNING THE BASICS OF THE ORM
"""

from polls.models import *
from django.utils import timezone

# Queryset with all Poll objects in the database
Poll.objects.all()

p = Poll(question="What up?", pub_date=timezone.now())
p.save()

# Let's see the id
p.id
# There's also an alias
p.pk
# if you override the primary key name which by default is id
# you can still access it by pk.


from django.utils import timezone
p = Poll(question="What up?", pub_date=timezone.now())

Poll(question="What's not?", pub_date=timezone.now()).save()
Poll(question="How's it going?", pub_date=timezone.now()).save()
Poll(question="Wasaaappp?", pub_date=timezone.now()).save()


def __unicode__(self):
    """Similar to toString in Java will make our objects display
    a lot more nicely"""
    pass

# Have to restart the shell in order to reload the model defs.

# No match returns an empty list
Poll.objects.filter(question="What up?")

# No match throws DoesNotExist error
Poll.objects.get(id=1)

# Same as question="What up?"
Poll.objects.filter(question__exact="What up?")

# Case insensitive matches
Poll.objects.filter(question__iexact="WHAT UP?")

Poll.objects.filter(question__contains="at")

# icontains, startswith, endswith and so on
# For a full reference, look at the docs
# https://docs.djangoproject.com/en/1.4/ref/models/querysets/#field-lookups


# Remember that named parameters are just keys and valus in
# the kwargs dictionary

# List all names in the p namespace
dir(p)

# Note the question, pub_save as we would expect
# But also the foreign key relation gives us a
p.choice_set
p.choice_set.all()

# Since the foreign key is from Choice to Poll, we have
# a one-to-many relation from Poll

p = Poll(question="What up?", pub_date=timezone.now())
p.save()

# Create is a helper that makes a new instance, and
# saves it
p.choice_set.create(choice_text="Cool!", votes=0)
p.choice_set.create(choice_text="Not cool!", votes=0)

p.choice_set.all()


# Let's follow the relations and do some joins!!!
Choice.objects.filter(poll__question__startswith="W")


# And the reverse lookup is also possible!!
Poll.objects.filter(choice__choice_text__startswith="Co")

# SLICING

# LIMIT 1
Poll.objects.all()[:1]

# OFFSET 5 LIMIT 5
Poll.objects.all()[5:10]


# If you want to see which SQL query the qs is generating
qs = Poll.objects.all()
str(qs.query)

"""
WHEN ARE THE QUERYSETS EVALUATED?

    - A QuerySet can be constructed, filtered, sliced, and generally passed
    around without actually hitting the database. No database activity actually
    occurs until you do something to evaluate the queryset.


    These actions will evaluate the queryset:
    - Iteration
    - Some slicing, such as step
    - len()
    - list(), forcing a list of the queryset
    - boolean testing of the queryset

"""

# User count() to find the number of objects in a QuerySet
# Since that will give you a SELECT COUNT(yada)
Poll.objects.count()


"""



VIEWS - THE REAL STUFF BEGINS




"""
# ./manage.py runserver


# The url dispatchers gets accessed first, let's add an url
url(r'^$', 'polls.views.home')


# And let's create our first view function
from django.http import HttpResponse


def home(request):
    return HttpResponse("Hello world")


# Wohoo, magic.


# Why don't we actually add something from our database with the ORM?
from models import Poll


def home2(request):
    questions = [q.question for q in Poll.objects.all()]
    return HttpResponse(", ".join(questions))


# Let's even try it with a template
from django.shortcuts import render_to_response


def home3(request):
    polls = Poll.objects.all().order_by('-pub_date')
    return render_to_response('polls/poll_list.html', {'polls': polls})


# The render function is just a convinience function, this is what's really
# going on
from django.template import Context, loader
t = loader.get_template('polls/poll_list.html')
c = Context({'polls': polls})
return HttpResponse(t.render(c))


# No such template found
"""
TEMPLATES

    Folder conventions
    - Separate app specific templates and site specific templates
    - Inside app dir, make a folder called ``templates``
    - In all templates folder, organize templates by application!
    - This way all template folders can be combined


Simplest template {{ polls }}

Extending an html base template
{% extends "base.html" %}

Blocks

{% block title %}This is cool{% endblock %}
{% block body %}
 ...
{% endblock %}


{% for p in polls %}
    <h1>{{ p.question }}</h1>
    <ul>
    {% for c in p.choice_set.all %}
        <li>{{ c.choice_text }}</li>
    {% endfor %}
    </ul>
{% endfor %}



VARIABLES
    {{ variable }}, When the template engine encounters a variable, it
    evaluates that variable and replaces it with the result

    Dot notation is used for all lookups in templates, in the following
    ordering:
    - dictionary lookup
    - attribute lookup
    - method call
    - list-index lookup

FILTERS
    You can modify variables for display by using filters.

    Examples
    {{ value|lower }} - convert to lowercase
    {{ value|default:"nothing" }}


TAGS
    {% tag %}, manages control flow in the templates

    {% for item in items %}
    {% if items %}
    {% if items and not polls %}
    {% if value < 100 %}
    {% if 'hello' in greetings %}


"""

"""
URLS - A CLOSER LOOK

    Parameters
    - Regex, dispatches to the *first* view that matches.
        The regex can be made to ``capture`` parameters like:
        ^polls/(?P<poll_id>\d+)/$
    - View, function to be called. Must satisfy the contract
        that the first parameter is a request, and captured parameters as the
        following arguments.
    - Kwargs, arbitrary arguments passed to the target view. Commonly used for
        overriding default parameters
    - Name, names you url so that you can refer to it elsewhere. Particularly
        useful when linking inside of templates

"""

# Let's create a poll/{id} url
url(r'^polls/(?P<poll_id>\d+)/$', 'polls.views.poll_detail', name="")


# And the view
from django.http import Http404


def poll_detail(request, poll_id):
    try:
        poll = Poll.objects.get(id=poll_id)
    except Poll.DoesNotExist:
        return Http404
    return render_to_response('polls/poll_detail.html', {'poll': poll})

# Cool shortcut
from django.shortcuts import get_object_or_404
poll = get_object_or_404(Poll, pk=poll_id)
return render_to_response('polls/poll_detail.html', {'poll': poll})
# Does exactly the same as above

# Similar for lists
polls = get_list_or_404(Poll, startswith="W")


"""
GENERIC VIEWS

    - There are common patterns for views

    Most common:
    - ListView, displays a list of a particular model
    - DetailView, display one single model

"""
from django.views.generic import DetailView, ListView
from polls.models import Poll

url(r'^polls/(?P<pk>\d+)/$', DetailView.as_view(model=Poll)),
url(r'^polls/$', ListView.as_view(model=Poll)),

# Okay, there are some black magic here. The views have a default for the
# templates that perfectly matches what we already are using.

# Change the templates:
# DetailView: poll
# ListView: object_list


# The context name can be overridden by setting ``context_object_name``
# and the template name w/ ``template_name``
url(r'^polls/$', ListView.as_view(model=Poll,
    context_object_name='object_list',
    template_name='polls/poll_list.html')),


"""
CLASS BASED VIEWS

    - New in Django 1.3
    - Before this, only function based views were possible

    - A function view always contains the code for selecting a particular
        subset of data, which make it harder for reuse. Classes can encapsulate
        both data and presentation logic, and enables independant reuse

"""

# Let's say we only want to show a subset of Polls in a list?
from django.views.generic import ListView


class NewestPolls(ListView):
    queryset = Poll.objects.all().order_by('-pub_date')[:3]

url(r'^newest/$', NewestPolls.as_view()),


"""
BATTERIES INCLUDED

    - Administration pages and authorization
    - django.contrib.auth is enabled by default
        Remember that we did enter admin username and password when creating
        the database
"""

# Add admin in INSTALLED_APPS in settings.py
# Uncomment admin in urls.py
# Show admin user interface

# We can of course access the models as usual
from django.contrib.auth.models import User
User.objects.all()
# etc

# Let's make use of the users and restrict a view so that
# you have to be logged in
from django.contrib.auth.decorators import login_required
url(r'^newest/$', login_required(NewestPolls.as_view())),

# It actually tries to redirect to the default login pages as well


# We can add our own models to the admin ui!

# touch polls/admin.py

from polls.models import Poll, Choice
from django.contrib import admin
admin.site.register(Poll)
admin.site.register(Choice)

# After enabling the admin stuff we need to create some new tables!
# ./manage.py syncdb

# You can customize a lot of the admin behaviour by creating and admin class
# for your model


class PollAdmin(admin.ModelAdmin):
    """Show two columns instead of the __unicode__ representation"""
    list_display = ('question', 'pub_date')

admin.site.register(Poll, PollAdmin)


"""


WHAT HAVEN'T I COVERED?

    TONS!
    - Forms and validations, although we got a sneak peek in the admin ui.
    - Middleware, (we've seen session and auth in action though)
    - Schema migrations
    - Unit testing
    - Caching
    - I18N

    and much more

"""
