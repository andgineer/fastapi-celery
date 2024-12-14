# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/andgineer/fastapi-celery/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                                        |    Stmts |     Miss |   Cover |   Missing |
|-------------------------------------------- | -------: | -------: | ------: | --------: |
| backend/app/api/create\_task.py             |        9 |        0 |    100% |           |
| backend/app/api/exception\_handlers.py      |       26 |        9 |     65% |20-23, 33, 43-44, 54-55, 65 |
| backend/app/api/get\_task.py                |       16 |        5 |     69% |17-18, 22-24 |
| backend/app/api/routing.py                  |       11 |        0 |    100% |           |
| backend/app/api/v1/auth/get\_token.py       |       18 |        0 |    100% |           |
| backend/app/api/v1/auth/get\_user\_group.py |       49 |       24 |     51% |18, 35, 41-49, 61-90 |
| backend/app/api/v1/models/auth.py           |       11 |        0 |    100% |           |
| backend/app/api/v1/models/errors.py         |        7 |        0 |    100% |           |
| backend/app/api/v1/models/words.py          |        3 |        0 |    100% |           |
| backend/app/api/v1/root.py                  |        8 |        0 |    100% |           |
| backend/app/api/v1/words/create.py          |       10 |        0 |    100% |           |
| backend/app/api/v1/words/delete.py          |        9 |        1 |     89% |        22 |
| backend/app/api/v1/words/get.py             |       12 |        0 |    100% |           |
| backend/app/celery\_app.py                  |       33 |        3 |     91% | 62-63, 73 |
| backend/app/config.py                       |       73 |        9 |     88% |12, 53, 98, 102, 106, 110, 119, 123, 127 |
| backend/app/controllers/tasks.py            |       33 |        8 |     76% |28, 53, 59-64 |
| backend/app/controllers/words.py            |        2 |        0 |    100% |           |
| backend/app/db/session.py                   |       32 |        6 |     81% |20, 38-39, 50-51, 69 |
| backend/app/json\_serializer.py             |        9 |        9 |      0% |     12-30 |
| backend/app/main.py                         |       29 |        5 |     83% |55-57, 64-66 |
| backend/app/modules\_load.py                |        9 |        0 |    100% |           |
| backend/app/tasks/base.py                   |       33 |       16 |     52% |56-62, 86-94 |
| backend/app/tasks/debug.py                  |       21 |        8 |     62% |     27-39 |
| backend/app/tasks/states.py                 |        2 |        0 |    100% |           |
| backend/app/tasks/words.py                  |       24 |        5 |     79% |     33-37 |
| backend/app/version.py                      |        1 |        0 |    100% |           |
|                                   **TOTAL** |  **490** |  **108** | **78%** |           |


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