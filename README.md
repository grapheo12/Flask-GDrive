# Flask-GDrive

Flask Plugin that removes the hassles of using the awesome Google Drive and Sheets API in a Flask project. It can use the Google Drive as CDN and Google Sheets as a replacement of Databases. Aimed at less data heavy projects.

## Components

For now, it has 2 main components:

- GDriveStatic
- GDriveDB

`GDriveStatic` is used as a replacement for the common `static` folder.
`GDriveDB` uses a set of Google Sheets as a database. Currently, it supports only basic CRUD operations.

## Setup

You need to have the Google Developer Credentials for your project to use this. Save the credentials in a safe location and initiate your app following the template given in [example.py](https://github.com/grapheo12/Flask-GDrive/flask_gdrive/example.py).