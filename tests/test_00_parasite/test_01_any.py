from rusttypes.option import Nil, Some
from rusttypes.result import Ok
from parasite import p


def test_any_default() -> None:
    assert p.any().parse_safe(None) == Ok(None)
    assert p.any().parse_safe(1) == Ok(1)
    assert p.any().parse_safe(1.0) == Ok(1.0)
    assert p.any().parse_safe("hello") == Ok("hello")
    assert p.any().parse_safe(True) == Ok(True)
    assert p.any().parse_safe(False) == Ok(False)
    assert p.any().parse_safe([]) == Ok([])
    assert p.any().parse_safe({}) == Ok({})
    assert p.any().parse_safe(()) == Ok(())
    assert p.any().parse_safe(set()) == Ok(set())
    assert p.any().parse_safe(frozenset()) == Ok(frozenset())

    o = object()
    assert p.any().parse_safe(o) == Ok(o)


def test_any_optional() -> None:
    assert p.any().optional()._find_and_parse_safe({}, "key") == Ok(Nil)
    assert p.any().optional()._find_and_parse_safe({"key": "value"}, "key") == Ok(Some("value"))

    assert p.any().required()._find_and_parse_safe({}, "key").is_err()
    assert p.any().required()._find_and_parse_safe({"key": "value"}, "key") == Ok(Some("value"))
