from rusttypes.option import Nil, Some
from rusttypes.result import Ok
from parasite import p


def test_variant_default() -> None:
    assert p.variant().parse_safe(None).is_err()
    assert p.variant().parse_safe(1).is_err()
    assert p.variant().parse_safe(1.0).is_err()
    assert p.variant().parse_safe("hello").is_err()
    assert p.variant().parse_safe(True).is_err()
    assert p.variant().parse_safe(False).is_err()
    assert p.variant().parse_safe([]).is_err()
    assert p.variant().parse_safe({}).is_err()
    assert p.variant().parse_safe(()).is_err()
    assert p.variant().parse_safe(set()).is_err()
    assert p.variant().parse_safe(frozenset()).is_err()
    assert p.variant().parse_safe(object()).is_err()


def test_variant_add_variant() -> None:
    v = p.variant().add_variant(p.number()).add_variant(p.string())

    assert v.parse_safe(1) == Ok(1)
    assert v.parse_safe(1.0) == Ok(1.0)
    assert v.parse_safe("hello") == Ok("hello")

    assert v.parse_safe(None).is_err()
    assert v.parse_safe(True).is_err()
    assert v.parse_safe(False).is_err()
    assert v.parse_safe([]).is_err()
    assert v.parse_safe({}).is_err()
    assert v.parse_safe(()).is_err()
    assert v.parse_safe(set()).is_err()
    assert v.parse_safe(frozenset()).is_err()
    assert v.parse_safe(object()).is_err()


def test_variant_find() -> None:
    v = p.variant().add_variant(p.number()).add_variant(p.string())

    assert v._find_and_parse_safe({}, "key").is_err()
    assert v._find_and_parse_safe({"key": 1}, "key") == Ok(Some(1))
    assert v._find_and_parse_safe({"key": 1.0}, "key") == Ok(Some(1.0))
    assert v._find_and_parse_safe({"key": "value"}, "key") == Ok(Some("value"))


def test_variant_optional() -> None:
    v = p.variant().add_variant(p.number()).add_variant(p.string())

    assert v.optional()._find_and_parse_safe({}, "key") == Ok(Nil)
    assert v.optional()._find_and_parse_safe({"key": 1}, "key") == Ok(Some(1))
    assert v.optional()._find_and_parse_safe({"key": 1.0}, "key") == Ok(Some(1.0))
    assert v.optional()._find_and_parse_safe({"key": "value"}, "key") == Ok(Some("value"))

    assert v.required()._find_and_parse_safe({}, "key").is_err()
    assert v.required()._find_and_parse_safe({"key": 1}, "key") == Ok(Some(1))
    assert v.required()._find_and_parse_safe({"key": 1.0}, "key") == Ok(Some(1.0))
    assert v.required()._find_and_parse_safe({"key": "value"}, "key") == Ok(Some("value"))


def test_variant_nullable() -> None:
    v = p.variant().add_variant(p.number()).add_variant(p.string())

    assert v.nullable()._find_and_parse_safe({}, "key").is_err()
    assert v.nullable()._find_and_parse_safe({"key": 1}, "key") == Ok(Some(1))
    assert v.nullable()._find_and_parse_safe({"key": 1.0}, "key") == Ok(Some(1.0))
    assert v.nullable()._find_and_parse_safe({"key": "value"}, "key") == Ok(Some("value"))
    assert v.nullable()._find_and_parse_safe({"key": None}, "key") == Ok(Some(None))

    assert v.non_nullable()._find_and_parse_safe({}, "key").is_err()
    assert v.non_nullable()._find_and_parse_safe({"key": 1}, "key") == Ok(Some(1))
    assert v.non_nullable()._find_and_parse_safe({"key": 1.0}, "key") == Ok(Some(1.0))
    assert v.non_nullable()._find_and_parse_safe({"key": "value"}, "key") == Ok(Some("value"))
    assert v.non_nullable()._find_and_parse_safe({"key": None}, "key").is_err()


def test_variant_rm_variant() -> None:
    v = p.variant().add_variant(p.number()).add_variant(p.string()).rm_variant(p.number())

    assert v.parse_safe("hello") == Ok("hello")
    assert v.parse_safe(1).is_err()
    assert v.parse_safe(1.0).is_err()


def test_variant_rm_variant_safe() -> None:
    v = p.variant().add_variant(p.number()).add_variant(p.string())

    assert v.rm_variant_safe(p.number()).unwrap().parse_safe("hello") == Ok("hello")
    assert v.rm_variant_safe(p.any()).is_err()
