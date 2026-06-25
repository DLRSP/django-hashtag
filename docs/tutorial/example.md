# Example

A quick walkthrough of using `django-hashtag` in a project.

## Run the demo project

``` shell
git clone --depth=50 --branch=django-hashtag https://github.com/DLRSP/example.git DLRSP/example
cd DLRSP/example
python manage.py runserver
```

Then browse the app at <http://127.0.0.1:8000>.

## Tag a model

`django-hashtag` builds on [django-taggit](https://github.com/jazzband/django-taggit).
Attach a tag manager to your model and assign tags as usual, then render and
filter them with the helpers documented in [Templates](templates.md).
