
import os
from setuptools import setup

README = os.path.join(os.path.dirname(__file__), 'README.rst')
LONG_DESCRIPTION = open(README, 'r').read()
CLASSIFIERS = [
    "Development Status :: 4 - Beta",
    "Environment :: Web Environment",
    "Framework :: Django",
    "Framework :: Django",
    "Framework :: Django :: 2.2",
    "Framework :: Django :: 3.2",
    "Framework :: Django :: 4.0",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: BSD License",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Topic :: Software Development",
    "Topic :: Software Development :: Libraries :: Application Frameworks",
]

setup(
    name="django-google-maps",
    version='0.12.4',
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
