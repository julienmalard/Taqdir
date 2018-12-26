import unittest
from urllib import request


class امتحان_ناسا(unittest.TestCase):
    pass


request.urlretrieve("https://power.larc.nasa.gov/cgi-bin/v1/DataAccess.py")
