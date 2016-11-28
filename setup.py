
import os
from setuptools import setup

README = os.path.join(os.path.dirname(__file__), 'README.md')
LONG_DESCRIPTION = open(README, 'r').read()
CLASSIFIERS = [
    "Development Status :: 3 - Alpha",
    "Environment :: Web Environment",
    "Framework :: Django",
    "Framework :: Django",
    "Framework :: Django :: 1.8",
    "Framework :: Django :: 1.9",
    "Framework :: Django :: 1.10",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: BSD License",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3.4",
    "Programming Language :: Python :: 3.5",
    "Topic :: Software Development",
    "Topic :: Software Development :: Libraries :: Application Frameworks",
]

setup(
    name="django-google-maps",
    version='0.6.0',
    author="Aaron Madison",
    author_email="aaron.l.madison@gmail.com",
    description="Plugs google maps V3 api into Django admin.",
    long_description=LONG_DESCRIPTION,
    url="https://github.com/madisona/django-google-maps",
    packages=("django_google_maps",),
    include_package_data=True,
    install_requires=open('requirements/requirements.txt').read().split('\n'),
    tests_require=open('requirements/test.txt').read().split('\n'),
    classifiers=CLASSIFIERS,
    zip_safe=False,
)
