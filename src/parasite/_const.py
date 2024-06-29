# -- STL Imports --
import re

RE_EMAIL = re.compile(
    r"^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z"
    r"0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$",
)
"""
Regex pattern for email validation as per RFC2822 standards.

Attribution:
    - https://regexr.com/2rhq7, by Tripleaxis (from .NET helpfiles)
"""

RE_URL = re.compile(
    r"^((\w+:\/\/)[-a-zA-Z0-9:@;?&=\/%\+\.\*!'\(\),\$_\{\}\^~\[\]`#|]+)$",
)
"""
Regex pattern for URL/URI validation.

Attribution:
    - https://regexr.com/2ri7q, by Gabriel Mariani
"""

RE_UUID = re.compile(
    r"^[0-9A-Za-z]{8}-[0-9A-Za-z]{4}-4[0-9A-Za-z]{3}-[89ABab][0-9A-Za-z]{3}-[0-9A-Za-z]{12}$"
)
"""Regex pattern validation for UUID v4 as per RFC9562.

Attribution:
    - http://en.wikipedia.org/wiki/Universally_unique_identifier#Version_4_.28random.29
    - https://regexr.com/39f77, by clayzermk1
"""

# Copyright (c) 2022 Colin McDonnell
# All rights reserved.
#
# Original Project: https://github.com/colinhacks/zod
# License File: licenses/zod_mit.txt
RE_CUID = re.compile(r"^c[^\\s-]{8,}$")
"""Regex pattern for CUID validation."""

# Copyright (c) 2022 Colin McDonnell
# All rights reserved.
#
# Original Project: https://github.com/colinhacks/zod
# License File: licenses/zod_mit.txt
RE_CUID2 = re.compile(r"^[a-z][a-z0-9]*$")
"""Regex pattern for CUID2 validation."""

# Copyright (c) 2022 Colin McDonnell
# All rights reserved.
#
# Original Project: https://github.com/colinhacks/zod
# License File: licenses/zod_mit.txt
RE_ULID = re.compile(r"^[0-9A-HJKMNP-TV-Z]{26}$")
"""Regex pattern for ULID validation."""

# Copyright (c) 2022 Colin McDonnell
# All rights reserved.
#
# Original Project: https://github.com/colinhacks/zod
# License File: licenses/zod_mit.txt
RE_IPV4 = re.compile(
    r"^(?:(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])\.){3}(?:25[0-5]|2[0-4][0-9]|1[0-9]"
    r"[0-9]|[1-9][0-9]|[0-9])$"
)
"""Regex pattern for IPv4 validation."""

# Copyright (c) 2022 Colin McDonnell
# All rights reserved.
#
# Original Project: https://github.com/colinhacks/zod
# License File: licenses/zod_mit.txt
RE_IPV6 = re.compile(
    r"^(([a-f0-9]{1,4}:){7}|::([a-f0-9]{1,4}:){0,6}|([a-f0-9]{1,4}:){1}:([a-f0-9]{1,4}:){0,5}|"
    r"([a-f0-9]{1,4}:){2}:([a-f0-9]{1,4}:){0,4}|([a-f0-9]{1,4}:){3}:([a-f0-9]{1,4}:){0,3}|"
    r"([a-f0-9]{1,4}:){4}:([a-f0-9]{1,4}:){0,2}|([a-f0-9]{1,4}:){5}:([a-f0-9]{1,4}:){0,1})([a-f0-9]"
    r"{1,4}|(((25[0-5])|(2[0-4][0-9])|(1[0-9]{2})|([0-9]{1,2}))\\.){3}((25[0-5])|(2[0-4][0-9])|"
    r"(1[0-9]{2})|([0-9]{1,2})))$"
)
"""Regex pattern for IPv6 validation."""
