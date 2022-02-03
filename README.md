# SubredditLog
> A Moderation Log for Subreddit Moderators with Both Public and Private Interfaces

A tool that allows subreddit moderators to add mod log entries, including private notes, to aid in subreddit moderation.

## Installation

SubredditLog is installed as a docker-compose stack. Please see [the documentation](docs/installation/index.md) for 
more details.

## Usage example

Usage of SubredditLog is documented [here](docs/usage/index.md).

## Development setup

```sh
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Release History

- 0.2.1
  - Adds ability for moderators to edit their entries and superusers to edit all entries
- 0.2
  - Adds real-time notification of previous entries for a user
  - Adds ability to change your own password
  - Adds link to Django Admin in top nav for superusers
  - Allows importing of pre-existing mod logs in Excel format
  - Adds ability to add earlier entries via Django admin
- 0.1.3
  - Update dependencies due to security issues 
- 0.1.2
  - Update dependencies due to security issues 
- 0.1.1
  - Fixed bugs in styling of the admin panel
  - Fixed various documentation bugs.
- 0.1
  - Initial release

## Meta

Sean Callaway – [@smcallaway](https://twitter.com/smcallaway) – seancallaway@gmail.com

Distributed under the Apache 2.0 license. See ``LICENSE`` for more information.

## Contributing

1. Fork it (<https://gitlab.com/scallaway/SubredditLog/-/forks/new>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Merge Request
