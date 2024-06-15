from rusttypes.option import Nil, Some
from rusttypes.result import Ok
from parasite import p


def test_boolean_default() -> None:
    assert p.boolean().parse_safe(True) == Ok(True)
    assert p.boolean().parse_safe(False) == Ok(False)

    assert p.boolean().parse_safe(None).is_err()
    assert p.boolean().parse_safe(1).is_err()
    assert p.boolean().parse_safe(1.0).is_err()
    assert p.boolean().parse_safe("hello").is_err()
    assert p.boolean().parse_safe([]).is_err()
    assert p.boolean().parse_safe({}).is_err()
    assert p.boolean().parse_safe(()).is_err()
    assert p.boolean().parse_safe(set()).is_err()
    assert p.boolean().parse_safe(frozenset()).is_err()
    assert p.boolean().parse_safe(object()).is_err()


def test_boolean_find() -> None:
    assert p.boolean()._find_and_parse_safe({}, "key").is_err()
    assert p.boolean()._find_and_parse_safe({"key": True}, "key") == Ok(Some(True))


def test_boolean_optional() -> None:
    assert p.boolean().optional()._find_and_parse_safe({}, "key") == Ok(Nil)
    assert p.boolean().optional()._find_and_parse_safe({"key": True}, "key") == Ok(Some(True))

    assert p.boolean().required()._find_and_parse_safe({}, "key").is_err()
    assert p.boolean().required()._find_and_parse_safe({"key": True}, "key") == Ok(Some(True))


def test_boolean_nullable() -> None:
    assert p.boolean().nullable()._find_and_parse_safe({}, "key").is_err()
    assert p.boolean().nullable()._find_and_parse_safe({"key": True}, "key") == Ok(Some(True))
    assert p.boolean().nullable()._find_and_parse_safe({"key": None}, "key") == Ok(Some(None))

    assert p.boolean().non_nullable()._find_and_parse_safe({}, "key").is_err()
    assert p.boolean().non_nullable()._find_and_parse_safe({"key": True}, "key") == Ok(Some(True))
    assert p.boolean().non_nullable()._find_and_parse_safe({"key": None}, "key").is_err()


def test_boolean_leaniant() -> None:
    assert p.boolean().leaniant().parse_safe("true") == Ok(True)
    assert p.boolean().leaniant().parse_safe("1") == Ok(True)
    assert p.boolean().leaniant().parse_safe("yes") == Ok(True)
    assert p.boolean().leaniant().parse_safe("y") == Ok(True)
    assert p.boolean().leaniant().parse_safe(1) == Ok(True)
    assert p.boolean().leaniant().parse_safe(1.0) == Ok(True)
    assert p.boolean().leaniant().parse_safe(True) == Ok(True)

    assert p.boolean().leaniant().parse_safe("false") == Ok(False)
    assert p.boolean().leaniant().parse_safe("0") == Ok(False)
    assert p.boolean().leaniant().parse_safe("no") == Ok(False)
    assert p.boolean().leaniant().parse_safe("n") == Ok(False)
    assert p.boolean().leaniant().parse_safe(0) == Ok(False)
    assert p.boolean().leaniant().parse_safe(0.0) == Ok(False)
    assert p.boolean().leaniant().parse_safe(float("nan")) == Ok(False)
    assert p.boolean().leaniant().parse_safe(False) == Ok(False)

    re_true = r'^foo$'
    re_false = r'^bar$'
    assert p.boolean().leaniant(re_true, re_false).parse_safe("foo") == Ok(True)
    assert p.boolean().leaniant(re_true, re_false).parse_safe("bar") == Ok(False)
    assert p.boolean().leaniant(re_true, re_false).parse_safe(1) == Ok(True)
    assert p.boolean().leaniant(re_true, re_false).parse_safe(0) == Ok(False)


def test_boolean_literal() -> None:
    assert p.boolean().literal(True).parse_safe(True) == Ok(True)
    assert p.boolean().literal(True).parse_safe(False).is_err()

    assert p.boolean().literal(False).parse_safe(False) == Ok(False)
    assert p.boolean().literal(False).parse_safe(True).is_err()
