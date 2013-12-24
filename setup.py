from setuptools import setup, find_packages


version = __import__('user_action_confirmation').get_version()


def get_requires_list(filename):
    s = open(filename).read().split("\n")
    dependenses = []
    if len(s):
        for pkg in s:
            if pkg.strip() == '' or pkg.startswith("#"):
                continue
            if pkg.startswith("-e"):
                continue
                try:
                    p = pkg.split("#egg=")[1]
                    dependenses += [p, ]
                except:
                    continue
            else:
                dependenses += [pkg, ]
    return dependenses


setup(
    name = "django-user-action-confirmation",
    version = version,
    description = "Easy and simple way to confirm user actions in your django projects",
    keywords = "confirm actions, confirmation, user action confirmation",
    author = "Alex Kamedov",
    author_email = "alex@kamedov.ru",
    url = "https://github.com/alekam/django-user-action-confirmation",
    license = "New BSD License",
    platforms = ["any"],
    classifiers = ["Development Status :: %s" % version,
                   "Environment :: Web Environment",
                   "Framework :: Django",
                   "Intended Audience :: Developers",
                   "License :: OSI Approved :: BSD License",
                   "Operating System :: OS Independent",
                   "Programming Language :: Python",
                   "Topic :: Utilities"],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=get_requires_list('requirements.txt'),
)
