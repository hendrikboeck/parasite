import re
from rusttypes.option import Nil, Some
from rusttypes.result import Ok
from parasite import p


def test_string_default() -> None:
    assert p.string().parse_safe("hello") == Ok("hello")

    assert p.string().parse_safe(None).is_err()
    assert p.string().parse_safe(1).is_err()
    assert p.string().parse_safe(1.0).is_err()
    assert p.string().parse_safe(True).is_err()
    assert p.string().parse_safe(False).is_err()
    assert p.string().parse_safe([]).is_err()
    assert p.string().parse_safe({}).is_err()
    assert p.string().parse_safe(()).is_err()
    assert p.string().parse_safe(set()).is_err()
    assert p.string().parse_safe(frozenset()).is_err()
    assert p.string().parse_safe(object()).is_err()


def test_string_find() -> None:
    assert p.string()._find_and_parse_safe({}, "key").is_err()
    assert p.string()._find_and_parse_safe({"key": "value"}, "key") == Ok(Some("value"))


def test_string_optional() -> None:
    assert p.string().optional()._find_and_parse_safe({}, "key") == Ok(Nil)
    assert p.string().optional()._find_and_parse_safe({"key": "value"}, "key") == Ok(Some("value"))

    assert p.string().required()._find_and_parse_safe({}, "key").is_err()
    assert p.string().required()._find_and_parse_safe({"key": "value"}, "key") == Ok(Some("value"))


def test_string_nullable() -> None:
    assert p.string().nullable()._find_and_parse_safe({}, "key").is_err()
    assert p.string().nullable()._find_and_parse_safe({"key": "value"}, "key") == Ok(Some("value"))
    assert p.string().nullable()._find_and_parse_safe({"key": None}, "key") == Ok(Some(None))

    assert p.string().not_nullable()._find_and_parse_safe({}, "key").is_err()
    assert p.string().not_nullable()._find_and_parse_safe({"key": "value"}, "key") == Ok(
        Some("value")
    )
    assert p.string().not_nullable()._find_and_parse_safe({"key": None}, "key").is_err()


def test_string_trim() -> None:
    assert p.string().trim().parse_safe("  hello  ") == Ok("hello")
    assert p.string().trim().parse_safe("hello") == Ok("hello")
    assert p.string().trim().parse_safe("  hello") == Ok("hello")
    assert p.string().trim().parse_safe("hello  ") == Ok("hello")
    assert p.string().trim().parse_safe("  hello  ") == Ok("hello")
    assert p.string().trim().parse_safe("  ") == Ok("")


def test_string_to_lower() -> None:
    assert p.string().to_lower().parse_safe("HELLO") == Ok("hello")
    assert p.string().to_lower().parse_safe("hello") == Ok("hello")
    assert p.string().to_lower().parse_safe("HeLLo") == Ok("hello")
    assert p.string().to_lower().parse_safe("hello") == Ok("hello")
    assert p.string().to_lower().parse_safe("  hello  ") == Ok("  hello  ")
    assert p.string().to_lower().parse_safe("  ") == Ok("  ")


def test_string_to_upper() -> None:
    assert p.string().to_upper().parse_safe("HELLO") == Ok("HELLO")
    assert p.string().to_upper().parse_safe("hello") == Ok("HELLO")
    assert p.string().to_upper().parse_safe("HeLLo") == Ok("HELLO")
    assert p.string().to_upper().parse_safe("hello") == Ok("HELLO")
    assert p.string().to_upper().parse_safe("  hello  ") == Ok("  HELLO  ")
    assert p.string().to_upper().parse_safe("  ") == Ok("  ")


def test_string_min() -> None:
    assert p.string().min(5).parse_safe("hello") == Ok("hello")
    assert p.string().min(5).parse_safe("hello world") == Ok("hello world")

    assert p.string().min(5).parse_safe("hell").is_err()


def test_string_max() -> None:
    assert p.string().max(5).parse_safe("hell") == Ok("hell")
    assert p.string().max(5).parse_safe("hello") == Ok("hello")

    assert p.string().max(5).parse_safe("hello world").is_err()


def test_string_length() -> None:
    assert p.string().length(5).parse_safe("hello") == Ok("hello")

    assert p.string().length(5).parse_safe("hell").is_err()
    assert p.string().length(5).parse_safe("hello world").is_err()


def test_string_not_empty() -> None:
    assert p.string().not_empty().parse_safe("hello") == Ok("hello")
    assert p.string().not_empty().parse_safe("").is_err()


def test_transform_before_parse() -> None:
    assert p.string().max(5).trim().transform_before_parse().parse_safe("  hello  ") == Ok("hello")
    assert p.string().max(5).trim().transform_before_parse().parse_safe("hello") == Ok("hello")

    assert p.string().max(5).trim().parse_safe("  hello  ").is_err()


def test_string_starts_with() -> None:
    assert p.string().starts_with("hello").parse_safe("hello world") == Ok("hello world")
    assert p.string().starts_with("hello").parse_safe("hello") == Ok("hello")

    assert p.string().starts_with("hello").parse_safe("world").is_err()


def test_string_ends_with() -> None:
    assert p.string().ends_with("world").parse_safe("hello world") == Ok("hello world")
    assert p.string().ends_with("world").parse_safe("world") == Ok("world")

    assert p.string().ends_with("world").parse_safe("hello").is_err()


def test_string_contains() -> None:
    assert p.string().contains("world").parse_safe("hello world") == Ok("hello world")
    assert p.string().contains("world").parse_safe("world") == Ok("world")

    assert p.string().contains("world").parse_safe("hello").is_err()


def test_string_email() -> None:
    assert p.string().email().parse_safe("test@gmail.com") == Ok("test@gmail.com")
    assert p.string().email().parse_safe("hello").is_err()


def test_url() -> None:
    assert p.string().url().parse_safe("https://www.google.com") == Ok("https://www.google.com")
    assert p.string().url().parse_safe("hello").is_err()


def test_string_uuid() -> None:
    id_ = "e99ec0df-87ca-4d56-a913-991500154108"

    assert p.string().uuid().parse_safe(id_) == Ok(id_)
    assert p.string().uuid().parse_safe("hello").is_err()


def test_string_cuid() -> None:
    id_ = "clwta4wuf000009jp98jbggmo"

    assert p.string().cuid().parse_safe(id_) == Ok(id_)
    assert p.string().cuid().parse_safe("hello").is_err()


def test_string_cuid2() -> None:
    id_ = "nv1wfjjccvmzezbu98wjj7gr"

    assert p.string().cuid2().parse_safe(id_) == Ok(id_)
    assert p.string().cuid2().parse_safe("hello_").is_err()


def test_string_ulid() -> None:
    id_ = "01HZ4TH3GR88DZRFC8CPWEKPNQ"

    assert p.string().ulid().parse_safe(id_) == Ok(id_)
    assert p.string().ulid().parse_safe("hello").is_err()


def test_string_ipv4() -> None:
    assert p.string().ipv4().parse_safe("10.0.0.1") == Ok("10.0.0.1")
    assert p.string().ipv4().parse_safe("10.0.0.1.110").is_err()
    assert p.string().ipv4().parse_safe("hello").is_err()


def test_string_ipv6() -> None:
    assert p.string().ipv6().parse_safe("2001:0db8:85a3:0000:0000:8a2e:0370:7334") == (
        Ok("2001:0db8:85a3:0000:0000:8a2e:0370:7334")
    )
    assert (
        p.string()
        .ipv6()
        .parse_safe(
            "2001:0db8:85a3:0000:0000:8a2e:0370:7334:2001:0db8:85a3:0000:0000:8a2e:0370:7334"
        )
        .is_err()
    )
    assert p.string().ipv6().parse_safe("hello").is_err()


def test_string_regex() -> None:
    rex = re.compile(r"^[0-9]+$")

    assert p.string().regex(rex).parse_safe("123456") == Ok("123456")
    assert p.string().regex(rex).parse_safe("hello").is_err()

    s1 = p.string().regex(rex)
    s1._m_regex = None
    assert s1.parse_safe("123456").is_err()

    s2 = p.string()
    s2._m_regex_t = None
    assert s2.parse_safe("123456") == Ok("123456")


def test_string_match() -> None:
    assert p.string().match(r"^[0-9]+$").parse_safe("123456") == Ok("123456")
    assert p.string().match(r"^[0-9]+$").parse_safe("hello").is_err()
