# Contributing to SubredditLog

First off, thanks for taking the time to contribute!

The following is a set of guidelines for contributing to SubredditLog which is hosted by
[Sean Callaway](https://gitlab.com/scallaway) on GitLab. These are mostly guidelines, not rules. Use your best
judgment and feel free to propose changes to this document in a pull request.

### Table of Content

[I Just Have a Question](#i-just-have-a-question)

[What Should I Know Before Getting Started?](#what-should-i-know-before-getting-started)

[How Can I Contribute?](#how-can-i-contribute)
  * [Reporting Bugs](#reporting-bugs)
  * [Suggesting Enhancements](#suggesting-enhancements)
  * [Your First Code Contribution](#your-first-code-contribution)
  * [Pull Requests](#pull-requests)

[Styleguides](#styleguides)
  * [Git Commit Messages](#git-commit-messages)
  * [Python Styleguide](#python-styleguide)

## I Just Have a Question

For now, feel free to open [an issue](https://gitlab.com/scallaway/SubredditLog/-/issues/new?issue) and assign it
the "Question" label.

## What Should I Know Before Getting Started?

SubredditLog was created by the moderators of [/r/lfg](https://old.reddit.com/r/lfg) in order to take our existing
moderator notes (stored in a shared Google Sheet) and provide a better interface and structured data formats.

The goal was always to make this available to moderators of other subreddits and all work going forward should keep
that in mind.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues and pull requests as you might find out that you don’t need
to create one. When opening a [new bug ticket](https://gitlab.com/scallaway/SubredditLog/-/issues/new), please select
the "BUG" template and keep the following in mind:

- **Use a clear and descriptive title** to identify the problem.
- **Describe the exact steps which reproduce the problem**. 
- **Include screenshots or animated GIFs** which show you following the described steps and clearly demonstrate the problem.

**NOTE:** If you find a closed issue that seems like it is the same thing that you're experiencing, open a new issue
and include a link to the original issue in the body of your new one.

### Suggesting Enhancements

If you want to suggest a new feature or a change to an existing one, please open a 
[new ticket](https://gitlab.com/scallaway/SubredditLog/-/issues/new), select the "FEATURE" template, and fill it out
completely.

### Your First Code Contribution

### Merge Requests

- Do not create a merge request without an associated issue.
- Select the "DEFAULT" merge request template and fill it out completely.
- Do not include issue numbers in your MR title

## Styleguides

### Git Commit Messages

* Use the present tense ("Add feature" not "Added feature")
* Use the imperative move ("Move button to..." not "Moves button to...")
* Limit the first line to 72 characters or less
* Reference issues and pull requests liberally after the first line

### Python Styleguide

All Python code is linted with [Flake8](https://flake8.pycqa.org/en/latest/) and
[isort](https://pycqa.github.io/isort/).

* Follow [PEP8](https://www.python.org/dev/peps/pep-0008/) with the following exceptions:
    * Line lengths should not exceed 120 characters
* Imports should be sorted alphabetically, both the packages and the modules.
  ```python
  from logging import getLogger

  from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
  from django.views.generic import CreateView, ListView, TemplateView, UpdateView

  from entries.models import Entry, Rule
  ```
* All files should end with a newline.
