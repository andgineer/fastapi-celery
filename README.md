# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/andgineer/fastapi-celery/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                                        |    Stmts |     Miss |   Cover |   Missing |
|-------------------------------------------- | -------: | -------: | ------: | --------: |
| backend/app/api/create\_task.py             |        9 |        0 |    100% |           |
| backend/app/api/exception\_handlers.py      |       25 |        9 |     64% |17-20, 27, 34-35, 42-43, 52 |
| backend/app/api/get\_task.py                |       15 |        5 |     67% |15-16, 20-22 |
| backend/app/api/routing.py                  |       11 |        0 |    100% |           |
| backend/app/api/v1/auth/get\_token.py       |       17 |        0 |    100% |           |
| backend/app/api/v1/auth/get\_user\_group.py |       49 |       24 |     51% |18, 35, 41-49, 59-88 |
| backend/app/api/v1/models/auth.py           |       11 |        0 |    100% |           |
| backend/app/api/v1/models/errors.py         |        7 |        0 |    100% |           |
| backend/app/api/v1/models/words.py          |        3 |        0 |    100% |           |
| backend/app/api/v1/root.py                  |        8 |        0 |    100% |           |
| backend/app/api/v1/words/create.py          |       10 |        0 |    100% |           |
| backend/app/api/v1/words/delete.py          |        9 |        1 |     89% |        22 |
| backend/app/api/v1/words/get.py             |       14 |        0 |    100% |           |
| backend/app/celery\_app.py                  |       33 |        3 |     91% | 62-63, 73 |
| backend/app/config.py                       |       73 |        9 |     88% |12, 53, 96, 100, 104, 108, 117, 121, 125 |
| backend/app/controllers/tasks.py            |       33 |        8 |     76% |28, 53, 59-64 |
| backend/app/controllers/words.py            |        2 |        0 |    100% |           |
| backend/app/db/session.py                   |       32 |        6 |     81% |20, 34-35, 43-44, 62 |
| backend/app/json\_serializer.py             |        8 |        8 |      0% |     12-29 |
| backend/app/main.py                         |       28 |        5 |     82% |52-54, 61-63 |
| backend/app/modules\_load.py                |        8 |        0 |    100% |           |
| backend/app/tasks/base.py                   |       28 |       12 |     57% |50-56, 73-81 |
| backend/app/tasks/debug.py                  |       20 |        9 |     55% |  9, 23-35 |
| backend/app/tasks/states.py                 |        2 |        0 |    100% |           |
| backend/app/tasks/words.py                  |       23 |        5 |     78% |     31-35 |
| backend/app/version.py                      |        1 |        0 |    100% |           |
|                                   **TOTAL** |  **479** |  **104** | **78%** |           |


## Setup coverage badge

Below are examples of the badges you can use in your main branch `README` file.

### Direct image

[![Coverage badge](https://raw.githubusercontent.com/andgineer/fastapi-celery/python-coverage-comment-action-data/badge.svg)](https://htmlpreview.github.io/?https://github.com/andgineer/fastapi-celery/blob/python-coverage-comment-action-data/htmlcov/index.html)

This is the one to use if your repository is private or if you don't want to customize anything.

### [Shields.io](https://shields.io) Json Endpoint

[![Coverage badge](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/andgineer/fastapi-celery/python-coverage-comment-action-data/endpoint.json)](https://htmlpreview.github.io/?https://github.com/andgineer/fastapi-celery/blob/python-coverage-comment-action-data/htmlcov/index.html)

Using this one will allow you to [customize](https://shields.io/endpoint) the look of your badge.
It won't work with private repositories. It won't be refreshed more than once per five minutes.

### [Shields.io](https://shields.io) Dynamic Badge

[![Coverage badge](https://img.shields.io/badge/dynamic/json?color=brightgreen&label=coverage&query=%24.message&url=https%3A%2F%2Fraw.githubusercontent.com%2Fandgineer%2Ffastapi-celery%2Fpython-coverage-comment-action-data%2Fendpoint.json)](https://htmlpreview.github.io/?https://github.com/andgineer/fastapi-celery/blob/python-coverage-comment-action-data/htmlcov/index.html)

This one will always be the same color. It won't work for private repos. I'm not even sure why we included it.

## What is that?

This branch is part of the
[python-coverage-comment-action](https://github.com/marketplace/actions/python-coverage-comment)
GitHub Action. All the files in this branch are automatically generated and may be
overwritten at any moment.