# Atrium to Lokki fetcher 

Fetch worked hours from Open Atrium to Lokki.

## Installation

  Add the downloaded directory to your path.

### Dependencies

  *  **SQLAclhemy:** sudo pip install SQLAlchemy
  *  **prettytable:** sudo pip install prettytable
  *  **pystache:** sudo pip install pystache
  *  **oauthlib:** sudo pip install oauthlib

### Drupal Services

  Atrium fetch requires a Drupal service providing access for views with 
  2-legged OAuth.

## Usage

### Initializing database

    af init db_path.sqlite

  Init command disregards the currently selected database as this could cause 
  data loss.

### Selecting database
  
  The active database is selected by the environment variable AF\_DB\_PATH. It 
  should contain a path to an SQLite database.

  Atrium fetch is able to start a shell session with the variable set:

    af shell db_path.sqlite

  If a relative path is specified, it is converted to an absolute path before
  starting the shell.

### Managing settings

    af config set setting-name value

    af config get \[setting-name\]

    af config list

#### Available settings

##### baseurl
  **required** Base URL of the service. Eg. http://atrium.example.com/
  Not the URL of the service - check that baseurl + /oauth/request\_token works.

##### oauth\_key
  **required** OAuth key

##### oauth\_secret
  **required** OAuth secret

### Managing profiles

    af profile add handle 

    af profile set lokki_db lokki_db.sql

    af profile set price_per_hour 20
    af profile set endpoint billing
    af profile set view_name view
    af profile set display_name page_1

### Fetching new rows

    af fetch profile_name

