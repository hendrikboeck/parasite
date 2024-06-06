from rusttypes.option import Nil
from rusttypes.result import Ok
from parasite import p


def test_never_default() -> None:
    assert p.never().parse_safe(None).is_err()
    assert p.never().parse_safe(1).is_err()
    assert p.never().parse_safe(1.0).is_err()
    assert p.never().parse_safe("hello").is_err()
    assert p.never().parse_safe(True).is_err()
    assert p.never().parse_safe(False).is_err()
    assert p.never().parse_safe([]).is_err()
    assert p.never().parse_safe({}).is_err()
    assert p.never().parse_safe(()).is_err()
    assert p.never().parse_safe(set()).is_err()
    assert p.never().parse_safe(frozenset()).is_err()
    assert p.never().parse_safe(object()).is_err()


def test_never_find() -> None:
    assert p.never().find_and_parse_safe({}, "key") == Ok(Nil)
    assert p.never().find_and_parse_safe({"key": "value"}, "key").is_err()
