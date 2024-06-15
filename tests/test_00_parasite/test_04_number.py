from rusttypes.option import Nil, Some
from rusttypes.result import Ok
from parasite import p


def test_number_default() -> None:
    assert p.number().parse_safe(1) == Ok(1)
    assert p.number().parse_safe(1.0) == Ok(1.0)

    assert p.number().parse_safe(None).is_err()
    assert p.number().parse_safe(True).is_err()
    assert p.number().parse_safe(False).is_err()
    assert p.number().parse_safe("hello").is_err()
    assert p.number().parse_safe([]).is_err()
    assert p.number().parse_safe({}).is_err()
    assert p.number().parse_safe(()).is_err()
    assert p.number().parse_safe(set()).is_err()
    assert p.number().parse_safe(frozenset()).is_err()
    assert p.number().parse_safe(object()).is_err()


def test_number_find() -> None:
    assert p.number()._find_and_parse_safe({}, "key").is_err()
    assert p.number()._find_and_parse_safe({"key": 1}, "key") == Ok(Some(1))
    assert p.number()._find_and_parse_safe({"key": 1.0}, "key") == Ok(Some(1.0))


def test_number_optional() -> None:
    assert p.number().optional()._find_and_parse_safe({}, "key") == Ok(Nil)
    assert p.number().optional()._find_and_parse_safe({"key": 1}, "key") == Ok(Some(1))
    assert p.number().optional()._find_and_parse_safe({"key": 1.0}, "key") == Ok(Some(1.0))

    assert p.number().required()._find_and_parse_safe({}, "key").is_err()
    assert p.number().required()._find_and_parse_safe({"key": 1}, "key") == Ok(Some(1))
    assert p.number().required()._find_and_parse_safe({"key": 1.0}, "key") == Ok(Some(1.0))


def test_number_nullable() -> None:
    assert p.number().nullable()._find_and_parse_safe({}, "key").is_err()
    assert p.number().nullable()._find_and_parse_safe({"key": 1}, "key") == Ok(Some(1))
    assert p.number().nullable()._find_and_parse_safe({"key": 1.0}, "key") == Ok(Some(1.0))
    assert p.number().nullable()._find_and_parse_safe({"key": None}, "key") == Ok(Some(None))

    assert p.number().non_nullable()._find_and_parse_safe({}, "key").is_err()
    assert p.number().non_nullable()._find_and_parse_safe({"key": 1}, "key") == Ok(Some(1))
    assert p.number().non_nullable()._find_and_parse_safe({"key": 1.0}, "key") == Ok(Some(1.0))
    assert p.number().non_nullable()._find_and_parse_safe({"key": None}, "key").is_err()


def test_number_integer() -> None:
    assert p.number().integer().parse_safe(1) == Ok(1)
    assert p.number().integer().parse_safe(1.0).is_err()


def test_number_gt() -> None:
    assert p.number().gt(1).parse_safe(2) == Ok(2)
    assert p.number().gt(1).parse_safe(1).is_err()
    assert p.number().gt(1).parse_safe(0).is_err()


def test_number_gte() -> None:
    assert p.number().gte(1).parse_safe(2) == Ok(2)
    assert p.number().gte(1).parse_safe(1) == Ok(1)
    assert p.number().gte(1).parse_safe(0).is_err()


def test_number_positive() -> None:
    assert p.number().positive().parse_safe(1) == Ok(1)
    assert p.number().positive().parse_safe(0).is_err()
    assert p.number().positive().parse_safe(-1).is_err()


def test_number_not_negative() -> None:
    assert p.number().not_negative().parse_safe(1) == Ok(1)
    assert p.number().not_negative().parse_safe(0) == Ok(0)
    assert p.number().not_negative().parse_safe(-1).is_err()


def test_number_min() -> None:
    assert p.number().min(1).parse_safe(0).is_err()
    assert p.number().min(1).parse_safe(1) == Ok(1)
    assert p.number().min(1).parse_safe(2) == Ok(2)


def test_number_lt() -> None:
    assert p.number().lt(1).parse_safe(0) == Ok(0)
    assert p.number().lt(1).parse_safe(1).is_err()
    assert p.number().lt(1).parse_safe(2).is_err()


def test_number_lte() -> None:
    assert p.number().lte(1).parse_safe(0) == Ok(0)
    assert p.number().lte(1).parse_safe(1) == Ok(1)
    assert p.number().lte(1).parse_safe(2).is_err()


def test_number_negative() -> None:
    assert p.number().negative().parse_safe(-1) == Ok(-1)
    assert p.number().negative().parse_safe(0).is_err()
    assert p.number().negative().parse_safe(1).is_err()


def test_number_not_positive() -> None:
    assert p.number().not_positive().parse_safe(-1) == Ok(-1)
    assert p.number().not_positive().parse_safe(0) == Ok(0)
    assert p.number().not_positive().parse_safe(1).is_err()


def test_number_max() -> None:
    assert p.number().max(1).parse_safe(0) == Ok(0)
    assert p.number().max(1).parse_safe(1) == Ok(1)
    assert p.number().max(1).parse_safe(2).is_err()
