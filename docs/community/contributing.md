# Contributing

## Clone

``` shell
git clone https://github.com/DLRSP/django-hashtag/
cd django-hashtag
```

## Run the test suite

``` shell
pytest tests/ -v
```

Or across the supported matrix with tox:

``` shell
tox -e py311-django42
```

## Pull requests

* Add tests for new behaviour.
* Add a `news/` fragment for any user-facing change (towncrier); for example
  `news/+my-change.feature.rst`.
* Run `pre-commit run --all-files` before opening the pull request.
