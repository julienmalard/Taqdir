import os

from pkg_resources import resource_filename


def وسائل_پانا(نام):
    return resource_filename(__name__, os.path.join('مسل', نام))
