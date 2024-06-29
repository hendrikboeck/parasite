from rusttypes.option import Nil, Some
from rusttypes.result import Ok
from parasite import p


def test_array_default() -> None:
    assert p.array().parse_safe([]) == Ok([])
    assert p.array().parse_safe([1, 2, 3]) == Ok([1, 2, 3])
    assert p.array().parse_safe([1.0, 2.0, 3.0]) == Ok([1.0, 2.0, 3.0])
    assert p.array().parse_safe(["hello", "world"]) == Ok(["hello", "world"])
    assert p.array().parse_safe([True, False]) == Ok([True, False])
    assert p.array().parse_safe([[], {}]) == Ok([[], {}])
    assert p.array().parse_safe([(), set()]) == Ok([(), set()])
    assert p.array().parse_safe([set(), frozenset()]) == Ok([set(), frozenset()])

    assert p.array().parse_safe(None).is_err()
    assert p.array().parse_safe(1).is_err()
    assert p.array().parse_safe(1.0).is_err()
    assert p.array().parse_safe("hello").is_err()
    assert p.array().parse_safe(True).is_err()
    assert p.array().parse_safe(False).is_err()
    assert p.array().parse_safe({}).is_err()
    assert p.array().parse_safe(()).is_err()
    assert p.array().parse_safe(set()).is_err()
    assert p.array().parse_safe(frozenset()).is_err()
    assert p.array().parse_safe(object()).is_err()


def test_array_find() -> None:
    assert p.array()._find_and_parse_safe({}, "key").is_err()
    assert p.array()._find_and_parse_safe({"key": []}, "key") == Ok(Some([]))

    assert p.array()._find_and_parse_safe({"key": [1, 2, 3]}, "key") == Ok(Some([1, 2, 3]))
    assert p.array()._find_and_parse_safe({"key": [1.0, 2.0, 3.0]}, "key") == Ok(
        Some([1.0, 2.0, 3.0])
    )
    assert p.array()._find_and_parse_safe({"key": ["hello", "world"]}, "key") == Ok(
        Some(["hello", "world"])
    )
    assert p.array()._find_and_parse_safe({"key": [True, False]}, "key") == Ok(Some([True, False]))
    assert p.array()._find_and_parse_safe({"key": [[], {}]}, "key") == Ok(Some([[], {}]))
    assert p.array()._find_and_parse_safe({"key": [(), set()]}, "key") == Ok(Some([(), set()]))
    assert p.array()._find_and_parse_safe({"key": [set(), frozenset()]}, "key") == Ok(
        Some([set(), frozenset()])
    )


def test_array_optional() -> None:
    assert p.array().optional()._find_and_parse_safe({}, "key") == Ok(Nil)
    assert p.array().optional()._find_and_parse_safe({"key": []}, "key") == Ok(Some([]))

    assert p.array().required()._find_and_parse_safe({}, "key").is_err()
    assert p.array().required()._find_and_parse_safe({"key": []}, "key") == Ok(Some([]))


def test_array_nullable() -> None:
    assert p.array().nullable()._find_and_parse_safe({}, "key").is_err()
    assert p.array().nullable()._find_and_parse_safe({"key": []}, "key") == Ok(Some([]))
    assert p.array().nullable()._find_and_parse_safe({"key": None}, "key") == Ok(Some(None))

    assert p.array().not_nullable()._find_and_parse_safe({}, "key").is_err()
    assert p.array().not_nullable()._find_and_parse_safe({"key": []}, "key") == Ok(Some([]))
    assert p.array().not_nullable()._find_and_parse_safe({"key": None}, "key").is_err()


def test_array_min() -> None:
    assert p.array().min(1).parse_safe([]).is_err()
    assert p.array().min(1).parse_safe([1]) == Ok([1])
    assert p.array().min(1).parse_safe([1, 2, 3]) == Ok([1, 2, 3])


def test_array_max() -> None:
    assert p.array().max(1).parse_safe([1, 2, 3]).is_err()
    assert p.array().max(1).parse_safe([1]) == Ok([1])
    assert p.array().max(1).parse_safe([]) == Ok([])


def test_array_not_empty() -> None:
    assert p.array().not_empty().parse_safe([]).is_err()
    assert p.array().not_empty().parse_safe([1, 2, 3]) == Ok([1, 2, 3])
    assert p.array().not_empty().parse_safe([1.0, 2.0, 3.0]) == Ok([1.0, 2.0, 3.0])
    assert p.array().not_empty().parse_safe(["hello", "world"]) == Ok(["hello", "world"])
    assert p.array().not_empty().parse_safe([True, False]) == Ok([True, False])
    assert p.array().not_empty().parse_safe([[], {}]) == Ok([[], {}])
    assert p.array().not_empty().parse_safe([(), set()]) == Ok([(), set()])
    assert p.array().not_empty().parse_safe([set(), frozenset()]) == Ok([set(), frozenset()])

    assert p.array().not_empty().parse_safe(None).is_err()
    assert p.array().not_empty().parse_safe(1).is_err()
    assert p.array().not_empty().parse_safe(1.0).is_err()
    assert p.array().not_empty().parse_safe("hello").is_err()
    assert p.array().not_empty().parse_safe(True).is_err()
    assert p.array().not_empty().parse_safe(False).is_err()
    assert p.array().not_empty().parse_safe({}).is_err()
    assert p.array().not_empty().parse_safe(()).is_err()
    assert p.array().not_empty().parse_safe(set()).is_err()
    assert p.array().not_empty().parse_safe(frozenset()).is_err()
    assert p.array().not_empty().parse_safe(object()).is_err()


def test_array_empty() -> None:
    assert p.array().empty().parse_safe([]) == Ok([])
    assert p.array().empty().parse_safe([1, 2, 3]).is_err()
    assert p.array().empty().parse_safe([1.0, 2.0, 3.0]).is_err()
    assert p.array().empty().parse_safe(["hello", "world"]).is_err()
    assert p.array().empty().parse_safe([True, False]).is_err()
    assert p.array().empty().parse_safe([[], {}]).is_err()
    assert p.array().empty().parse_safe([(), set()]).is_err()
    assert p.array().empty().parse_safe([set(), frozenset()]).is_err()


def test_array_length() -> None:
    assert p.array().length(1).parse_safe([]).is_err()
    assert p.array().length(1).parse_safe([1]) == Ok([1])


def test_array_element() -> None:
    a = p.array().element(p.number().integer())

    assert a.parse_safe([1, 2, 3]) == Ok([1, 2, 3])
    assert a.parse_safe([1.0, 2.0, 3.0]).is_err()
    assert a.parse_safe(["hello", "world"]).is_err()
    assert a.parse_safe([True, False]).is_err()
    assert a.parse_safe([[], {}]).is_err()
    assert a.parse_safe([(), set()]).is_err()
    assert a.parse_safe([set(), frozenset()]).is_err()
    assert a.parse_safe([object(), object()]).is_err()
