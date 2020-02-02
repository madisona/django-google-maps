
import os
from setuptools import setup

README = os.path.join(os.path.dirname(__file__), 'README.md')
LONG_DESCRIPTION = open(README, 'r').read()
CLASSIFIERS = [
    "Development Status :: 4 - Beta",
    "Environment :: Web Environment",
    "Framework :: Django",
    "Framework :: Django",
    "Framework :: Django :: 1.11",
    "Framework :: Django :: 2.0",
    "Framework :: Django :: 2.2",
    "Framework :: Django :: 3.0",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: BSD License",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Topic :: Software Development",
    "Topic :: Software Development :: Libraries :: Application Frameworks",
]

setup(
    name="django-google-maps",
    version='1.0.0',
    author="Aaron Madison",
    author_email="aaron.l.madison@gmail.com",
    description="Plugs google maps V3 api into Django admin.",
    long_description=LONG_DESCRIPTION,
    url="https://github.com/madisona/django-google-maps",
    packages=("django_google_maps",),
    include_package_data=True,
    install_requires=open('requirements/requirements.txt').read().splitlines(),
    tests_require=open('requirements/test.txt').read().splitlines(),
    classifiers=CLASSIFIERS,
    zip_safe=False,
)
