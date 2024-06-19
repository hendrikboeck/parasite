from rusttypes.option import Nil, Some
from rusttypes.result import Ok
from parasite import p


def test_object_default() -> None:
    assert p.obj().parse_safe({}) == Ok({})
    assert p.obj().parse_safe({"key": "value"}) == Ok({"key": "value"})
    assert p.obj().parse_safe({"key": 1}) == Ok({"key": 1})
    assert p.obj().parse_safe({"key": 1.0}) == Ok({"key": 1.0})
    assert p.obj().parse_safe({"key": True}) == Ok({"key": True})
    assert p.obj().parse_safe({"key": []}) == Ok({"key": []})
    assert p.obj().parse_safe({"key": {}}) == Ok({"key": {}})
    assert p.obj().parse_safe({"key": ()}) == Ok({"key": ()})
    assert p.obj().parse_safe({"key": set()}) == Ok({"key": set()})
    assert p.obj().parse_safe({"key": frozenset()}) == Ok({"key": frozenset()})

    assert p.obj().parse_safe(None).is_err()
    assert p.obj().parse_safe(1).is_err()
    assert p.obj().parse_safe(1.0).is_err()
    assert p.obj().parse_safe("hello").is_err()
    assert p.obj().parse_safe(True).is_err()
    assert p.obj().parse_safe(False).is_err()
    assert p.obj().parse_safe([]).is_err()
    assert p.obj().parse_safe(()).is_err()
    assert p.obj().parse_safe(set()).is_err()
    assert p.obj().parse_safe(frozenset()).is_err()
    assert p.obj().parse_safe(object()).is_err()


def test_object_find() -> None:
    assert p.obj()._find_and_parse_safe({}, "key").is_err()
    assert p.obj()._find_and_parse_safe({"key": {}}, "key") == Ok(Some({}))


def test_object_optional() -> None:
    assert p.obj().optional()._find_and_parse_safe({}, "key") == Ok(Nil)
    assert p.obj().optional()._find_and_parse_safe({"key": {}}, "key") == Ok(Some({}))

    assert p.obj().required()._find_and_parse_safe({}, "key").is_err()
    assert p.obj().required()._find_and_parse_safe({"key": {}}, "key") == Ok(Some({}))


def test_object_nullable() -> None:
    assert p.obj().nullable()._find_and_parse_safe({}, "key").is_err()
    assert p.obj().nullable()._find_and_parse_safe({"key": {}}, "key") == Ok(Some({}))
    assert p.obj().nullable()._find_and_parse_safe({"key": None}, "key") == Ok(Some(None))

    assert p.obj().not_nullable()._find_and_parse_safe({}, "key").is_err()
    assert p.obj().not_nullable()._find_and_parse_safe({"key": {}}, "key") == Ok(Some({}))
    assert p.obj().not_nullable()._find_and_parse_safe({"key": None}, "key").is_err()


def test_object_init_items() -> None:
    o = p.obj({"key": p.string()})
    assert o._m_items == {"key": p.string()}

    assert o.parse_safe({"key": "value"}) == Ok({"key": "value"})
    assert o.parse_safe({"key": 1}).is_err()


def test_object_init_items_optional() -> None:
    o = p.obj({"key": p.string().optional()})
    assert o._m_items == {"key": p.string().optional()}

    assert o.parse_safe({"key": "value"}) == Ok({"key": "value"})
    assert o.parse_safe({}) == Ok({})
    assert o.parse_safe({"key": None}).is_err()
    assert o.parse_safe({"key": 1}).is_err()


def test_object_init_items_nullable() -> None:
    o = p.obj({"key": p.string().nullable()})
    assert o._m_items == {"key": p.string().nullable()}

    assert o.parse_safe({"key": "value"}) == Ok({"key": "value"})
    assert o.parse_safe({"key": None}) == Ok({"key": None})
    assert o.parse_safe({}).is_err()
    assert o.parse_safe({"key": 1}).is_err()


def test_object_strict() -> None:
    o = p.obj({"key": p.string()}).strict()

    assert o.parse_safe({"key": "value"}) == Ok({"key": "value"})
    assert o.parse_safe({"key": "value", "key2": "value2"}).is_err()
    assert o.parse_safe({}).is_err()


def test_object_strip() -> None:
    o = p.obj({"key": p.string().optional()}).strip()

    assert o.parse_safe({"key": "value"}) == Ok({"key": "value"})
    assert o.parse_safe({"key": "value", "key2": "value2"}) == Ok({"key": "value"})
    assert o.parse_safe({}) == Ok({})


def test_object_extend() -> None:
    o1 = p.obj({"key": p.string()})
    o2 = p.obj({"key2": p.string()})

    o1.extend(o2)
    assert o1._m_items == {"key": p.string(), "key2": p.string()}
    assert o2._m_items == {"key2": p.string()}

    o1 = p.obj({"key": p.string()})
    o2 = p.obj({"key": p.number()})

    o1.extend(o2)
    assert o1._m_items == {"key": p.number()}
    assert o2._m_items == {"key": p.number()}


def test_object_merge() -> None:
    o1 = p.obj({"key": p.string()})
    o2 = p.obj({"key2": p.string()})

    o1.merge(o2)
    assert o1._m_items == {"key": p.string(), "key2": p.string()}
    assert o2._m_items == {"key2": p.string()}

    o1 = p.obj({"key": p.string()})
    o2 = p.obj({"key": p.number()})

    o1.merge(o2)
    assert o1._m_items == {"key": p.variant([p.string(), p.number()])}
    assert o2._m_items == {"key": p.number()}

    o1 = p.obj({"key": p.variant([p.string(), p.number()])})
    o2 = p.obj({"key": p.boolean()})

    o1.merge(o2)
    assert o1._m_items == {"key": p.variant([p.string(), p.number(), p.boolean()])}
    assert o2._m_items == {"key": p.boolean()}

    o1 = p.obj({"key": p.obj({"key": p.string()})})
    o2 = p.obj({"key": p.obj({"key2": p.string()})})

    o1.merge(o2)
    assert o1._m_items == {"key": p.obj({"key": p.string(), "key2": p.string()})}
    assert o2._m_items == {"key": p.obj({"key2": p.string()})}


def test_object_pick() -> None:
    assert p.obj({
        "key": p.string(),
        "key2": p.string()
    }).pick(["key"]) == p.obj({"key": p.string()})

    assert p.obj({
        "key": p.string(),
        "key2": p.string()
    }).pick_safe(["key"]) == p.obj({"key": p.string()})

    try:
        p.obj({"key": p.string(), "key2": p.string()}).pick(["key3"])
        assert False
    except KeyError:
        assert True

    assert p.obj({"key": p.string(), "key2": p.string()}).pick_safe(["key3"]) == p.obj({})


def test_object_omit() -> None:
    assert p.obj({
        "key": p.string(),
        "key2": p.string()
    }).omit(["key"]) == p.obj({"key2": p.string()})

    assert p.obj({
        "key": p.string(),
        "key2": p.string()
    }).omit(["key3"]) == p.obj({
        "key": p.string(),
        "key2": p.string()
    })


def test_object_add_item() -> None:
    assert p.obj().add_item("key", p.string()) == p.obj({"key": p.string()})
    assert p.obj({
        "key": p.string()
    }).add_item("key2", p.string()) == p.obj({
        "key": p.string(),
        "key2": p.string()
    })
