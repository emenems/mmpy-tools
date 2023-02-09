"""
Unit test for MySQL
Since this requires database, no real tests are here :D
"""
import pytest
from mmpy_tools import MySQL

def test_MySQL():
    """Since this requires database, will throw error if inputs not provided
    """
    with pytest.raises(Exception):
        assert MySQL()
