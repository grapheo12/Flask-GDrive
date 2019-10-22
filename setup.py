"""
Flask-GDrive
-----------------------------------

Wrapper over the Google Drive API to assist in serving
static files directly from a folder in Google Drive.

View docs and examples at our [Github
repo](https://github.com/grapheo12/Flask-Gdrive)
"""
from setuptools import setup, find_packages

setup(
    name='Flask-GDrive',
    version='0.6',
    url='https://github.com/grapheo12/Flask-GDrive',
    license='MIT',
    author='Shubham Mishra',
    author_email='smishra99.iitkgp@gmail.com',
    description='Flask extension for Google Drive API',
    long_description=__doc__,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask',
        'google-api-python-client',
        'google-auth-httplib2',
        'google-auth-oauthlib'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
