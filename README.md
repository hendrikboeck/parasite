![Stars][stars-shield]
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![Code Coverage][coverage-shield]](#code-coverage)


<br />
<div align="center">
<a href="https://github.com/hendrikboeck/parasite">
    <img src="https://raw.githubusercontent.com/hendrikboeck/parasite/main/.github/parasite_logo.png" alt="Logo" width="128" height="128">
</a>

<h1 align="center">parasite <code>v0.1.9</code></h1>

<p align="center">
    <code>zod</code> inspired library for Python 3.11+
    <br />
    <a href="https://github.com/hendrikboeck/parasite/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    |
    <a href="https://github.com/ohendrikboeck/parasite/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
</p>
</div>

> [!WARNING]
>
> This library is under active development, expect things to break or not to work as expected.
> Creating an issue for bugs you encounter would be appreciated. Documentation is currently work in
> progress.

## Table of Contents

- [Why?](#why)
- [What about the name?](#what-about-the-name)
- [Getting Started](#getting-started)
  - [Installing](#installing)
  - [Example usage](#example-usage)
- [Documentation](#documentation)
- [Code Coverage](#code-coverage)
- [License (_MIT License_)](#license-mit-license)

## Why?

Data and object validation in Python is essential to ensure that the inputs to a program are
accurate and adhere to expected formats, thereby preventing runtime errors and enhancing code
reliability. The TypeScript library `zod` offers a concise and expressive syntax for schema
validation, making it easier to define and enforce data structures. Implementing a similar library
in Python would greatly benefit developers by providing a streamlined, declarative approach to
validation, reducing boilerplate code and improving maintainability. This would facilitate more
robust data handling and enhance the overall quality of Python applications.

## What about the name?

I chose the name "Parasite" for this library because it draws heavy inspiration from the TypeScript
`zod` library, which excels in schema validation with its concise and expressive syntax. The name
"Parasite" is also a nod to one of Superman's iconic supervillains, serving as an homage to the
library that inspired this creation.

## Getting Started

### Installing

Install using `pip`:

```sh
pip install parasite
```

Install using `poetry` CLI:

```sh
poetry add parasite
```

or using `pyproject.toml`:

```toml
[tool.poetry.dependencies]
parasite = "^0.1.0"
```

### Example usage

```python
from parasite import p

schema = p.obj({
    "name": p.string().required(),
    "age": p.number().integer().min(0).optional(),
}).strip()

data = {
    "name": "John Doe",
    "age": 42,
    "extra": "This will be stripped",
}

schema.parse(data)   # {"name": "John Doe", "age": 42}
schema.parse({})   # ValidationError: Missing required key: "name"
```

## Documentation

> [!IMPORTANT]
>
> You can find the sphinx online documentation [here](https://hendrikboeck.github.io/parasite)!

## Code Coverage



```
---------- coverage: platform linux, python 3.11.9-final-0 -----------
Name                       Stmts   Miss  Cover
----------------------------------------------
src/parasite/__init__.py      22      0   100%
src/parasite/_const.py        17      0   100%
src/parasite/_utils.py         7      0   100%
src/parasite/any.py           27      0   100%
src/parasite/array.py         70      0   100%
src/parasite/boolean.py       72      0   100%
src/parasite/errors.py         1      0   100%
src/parasite/never.py         18      0   100%
src/parasite/null.py          29      0   100%
src/parasite/number.py       106      0   100%
src/parasite/object.py        93      0   100%
src/parasite/string.py       207      0   100%
src/parasite/type.py          29      0   100%
src/parasite/variant.py       61      0   100%
----------------------------------------------
TOTAL                        759      0   100%
```


## License (_MIT License_)

Copyright (c) 2024, Hendrik Böck <<hendrikboeck.dev@protonmail.com>>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

[license-shield]: https://img.shields.io/github/license/hendrikboeck/parasite?style=for-the-badge
[license-url]: https://github.com/hendrikboeck/parasite/blob/main/LICENSE
[issues-shield]: https://img.shields.io/github/issues/hendrikboeck/parasite?style=for-the-badge
[issues-url]: https://github.com/hendrikboeck/parasite/issues
[forks-shield]: https://img.shields.io/github/forks/hendrikboeck/parasite?style=for-the-badge
[forks-url]: https://github.com/hendrikboeck/parasite/forks
[contributors-shield]: https://img.shields.io/github/contributors/hendrikboeck/parasite?style=for-the-badge
[contributors-url]: https://github.com/hendrikboeck/parasite/contributors
[stars-shield]: https://img.shields.io/github/stars/hendrikboeck/parasite?style=for-the-badge
[coverage-shield]: https://img.shields.io/badge/Code%20Coverage-100%25-brightgreen.svg?style=for-the-badge
