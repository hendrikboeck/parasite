from parasite import p, Namespace
import pytest


def test_namespace():
    with pytest.raises(TypeError) as excinfo:
        Namespace()

    assert "cannot instantiate a namespace" in str(excinfo.value)

    with pytest.raises(TypeError) as excinfo:
        p()

    assert "cannot instantiate a namespace" in str(excinfo.value)
