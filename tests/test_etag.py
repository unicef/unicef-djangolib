from unittest.mock import Mock

from unicef_djangolib.etag import etag_cached


def test_etag():
    def view(self):
        return {}

    func1 = etag_cached('test')(view)
    func2 = etag_cached('test', True)(view)
    assert func1(Mock())
    assert func2(Mock())

    func1.invalidate()
