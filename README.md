# !!! Remove this section !!!
1. Create empty Git repository with your preferred name: example `django-my-new-pkg-name`
2. Checkout local copy of this new **empty** repository
3. Copy all the contents of this repository inside the **new cloned empty repository**
4. Massive **replace** the string `django-hashtag` with your new package's name `django-my-new-pkg-name`
5. Massive **replace** the string `PACKAGE_NAME` with your src location `my_new_pkg_src_location`
6. **Edit** the `tests/settings.py` file for the needed configuration to test your app
7. **Rename and edit** the `tests/test_fake.py` file for the needed application's tests
8. Install python's requirements `pip install -r requirements/requirements.in`
9. Install python's requirements `pip install -r requirements/dev.in`
10. Install python's package `pip install .` to test the package's local version  
11. Execute `python runtests.py` and validate all tests are passed (if any error is present, the automatic workflow on tag will fail)
12. Edit docs ...
13. Install python requirements `pip install -r requirements/docs.in`
14. Execute `python setup.py sdist bdist_wheel` to build the project
15. Execute `twine upload dist/*` to upload the builded files
16. Inside PyPi repository, **generate** new API key with the only scope of project
17. Inside Git repository's settings, section *General*, **enable** the `Allow auto-merge` and `Automatically delete head branches`
18. Inside Git repository's settings, section *Access*, **add access** to be able to execute workflows (as team member's or bot-user collaborator)
19. Inside Git repository's settings, section *Security*, **add security repository secret** named `PYPI_API_TOKEN` to be able to upload packages inside PyPi's repository

# django-hashtag [![PyPi license](https://img.shields.io/pypi/l/django-hashtag.svg)](https://pypi.python.org/pypi/django-hashtag)

[![PyPi status](https://img.shields.io/pypi/status/django-hashtag.svg)](https://pypi.python.org/pypi/django-hashtag)
[![PyPi version](https://img.shields.io/pypi/v/django-hashtag.svg)](https://pypi.python.org/pypi/django-hashtag)
[![PyPi python version](https://img.shields.io/pypi/pyversions/django-hashtag.svg)](https://pypi.python.org/pypi/django-hashtag)
[![PyPi downloads](https://img.shields.io/pypi/dm/django-hashtag.svg)](https://pypi.python.org/pypi/django-hashtag)
[![PyPi downloads](https://img.shields.io/pypi/dw/django-hashtag.svg)](https://pypi.python.org/pypi/django-hashtag)
[![PyPi downloads](https://img.shields.io/pypi/dd/django-hashtag.svg)](https://pypi.python.org/pypi/django-hashtag)

## GitHub ![GitHub release](https://img.shields.io/github/tag/DLRSP/django-hashtag.svg) ![GitHub release](https://img.shields.io/github/release/DLRSP/django-hashtag.svg)

## Test [![codecov.io](https://codecov.io/github/DLRSP/django-hashtag/coverage.svg?branch=main)](https://codecov.io/github/DLRSP/django-hashtag?branch=main) [![pre-commit.ci status](https://results.pre-commit.ci/badge/github/DLRSP/django-hashtag/main.svg)](https://results.pre-commit.ci/latest/github/DLRSP/django-hashtag/main) [![gitthub.com](https://github.com/DLRSP/django-hashtag/actions/workflows/ci.yaml/badge.svg)](https://github.com/DLRSP/django-hashtag/actions/workflows/ci.yaml)

## Check Demo Project
* Check the demo repo on [GitHub](https://github.com/DLRSP/example/tree/django-hashtag)

## Requirements
-   Python 3.8+ supported.
-   Django 3.2+ supported.

## Setup
1. Install from **pip**:
```shell
pip install django-hashtag
```

2. Modify `settings.py` by adding the app to `INSTALLED_APPS`:
```python
INSTALLED_APPS = [
    # ...
    "taggit",
    "hashtag",
    # ...
]
```

3. Execute Django's command `migrate` inside your project's root:
```sheel
python manage.py migrate
```

## Run Example Project

```shell
git clone --depth=50 --branch=django-hashtag https://github.com/DLRSP/example.git DLRSP/example
cd DLRSP/example
python manage.py runserver
```

Now browser the app @ http://127.0.0.1:8000
