# Compose Stack Installation

This section describes the installation and configuration of the SubredditLog application itself via a Docker Compose
stack.

## Install Docker and Docker-Compose

Install the following per Docker-provided documentation:

- [Docker](https://docs.docker.com/engine/install/)
- [docker-compose](https://docs.docker.com/compose/install/)

## Download SubredditLog

Download the [latest stable release](https://github.com/seancallaway/SubredditLog/releases) from GitHub as a tarball or
zip file and extract it to your desired path (e.g. `~/subredditlog/`).

## Configuration

Move into the SubredditLog directory and make a copy of `.env.example` named `.env`. This file will hold 
all of your local configuration parameters.

```shell
cp .env.example .env
```

Open `env.config` with your preferred text editor and configure each of the following required values:

- `ALLOWED_HOSTS`
- `SECRET_KEY`
- `DB_PASSWORD`

### ALLOWED HOSTS

This is a list of the valid hostnames and IP addresses by which this server can be reached. You must specify at least 
one name or IP address. (Note that this does not restrict the locations from which NetBox may be accessed: It is merely 
for [HTTP host header validation](https://docs.djangoproject.com/en/3.1/topics/security/#host-headers-virtual-hosting).)

Each value should be separated by a space.

```shell
ALLOWED_HOSTS=subredditlog.example.com 192.168.1.2
```

If you are not yet sure what the domain name and/or IP address of the SubredditLog installation will be, you can set
this to a wildcard (asterisk) to allow all host values.

```shell
ALLOWED_HOSTS=*
```

### SECRET KEY

This parameter must be assigned a randomly-generated key employed as a salt for hashing and related cryptographic 
functions. (Note, however, that it is _never_ directly used in the encryption of secret data.) This key must be unique 
to this installation and is recommended to be at least 50 characters long. It should not be shared outside the local 
system.

The following online tool can be used to generate a good secret key: https://miniwebtool.com/django-secret-key-generator/

!!! warning
    In the case of a highly available installation with multiple web servers, `SECRET_KEY` must be identical among all 
servers in order to maintain a persistent user session state.

### DB_PASSWORD

Input a random, secure password to be used for the local database connection.

The following online tool can be used to generate a working password: https://nupass.pw

When you have finished modifying the configuration, remember to save the file.

## Start the Compose Stack

After the configuration has been set, you can bring up the compose stack with the following command:

```shell
sudo docker-compose -f docker-compose.prod.yml up -d
```

If no error messages have been generated, then the application is running properly.

## Create a Super User

SubredditLog does not come with any predefined user accounts. You'll need to create a super user (administrative 
account) to be able to login. This can be created with the following command:

```shell
sudo docker-compose -f docker-compose.prod.yml exec app python manage.py createsuperuser
```

Follow the on-screen instructions, using your Reddit username as the username. Email address can be skipped by pressing 
Enter, as SubredditLog does not utilize email addresses in any way.

## Test the Application

Connect to the name or IP of the server (as defined in `ALLOWED_HOSTS`) on port 7654; for example, 
<http://127.0.0.1:7654/>. You should be greeted with the SubredditLog home page.

Try logging in using the super user account we just created. Once authenticated, you'll be able to access all areas of 
the UI, including the admin interface.
