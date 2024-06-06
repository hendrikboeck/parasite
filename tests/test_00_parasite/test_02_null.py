from rusttypes.option import Nil, Some
from rusttypes.result import Ok
from parasite import p


def test_null_default() -> None:
    assert p.null().parse_safe(None) == Ok(None)

    assert p.null().parse_safe(1).is_err()
    assert p.null().parse_safe(1.0).is_err()
    assert p.null().parse_safe(True).is_err()
    assert p.null().parse_safe("hello").is_err()
    assert p.null().parse_safe([]).is_err()
    assert p.null().parse_safe({}).is_err()
    assert p.null().parse_safe(()).is_err()
    assert p.null().parse_safe(set()).is_err()
    assert p.null().parse_safe(frozenset()).is_err()
    assert p.null().parse_safe(object()).is_err()


def test_null_optional() -> None:
    assert p.null().optional().find_and_parse_safe({}, "key") == Ok(Nil)
    assert p.null().optional().find_and_parse_safe({"key": None}, "key") == Ok(Some(None))

    assert p.null().required().find_and_parse_safe({}, "key").is_err()
    assert p.null().required().find_and_parse_safe({"key": None}, "key") == Ok(Some(None))
