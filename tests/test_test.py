# delete this file later it's literally just to test the tests
import pytest


def test_always_passes():
    assert True, "This test is designed to pass and verify CI/CD workflow setup."


@pytest.mark.xfail
def test_never_passes():
    assert False, "This test is designed to fail and verify CI/CD workflow setup."
