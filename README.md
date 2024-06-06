# `parasite` - `zod` inspired library for Python 3.11+

> **DISCLAIMER:**
>
> This library is under active development, expect things to break or not to work as expected.
> Creating an issue for bugs you encounter would be appreciated. Documentation is currently work in
> progress.

## Table of Contents

- [Why?](#why)
- [What about the name?](#what-about-the-name)
- [Getting Started](#getting-started)
- [Documentation](#documentation)
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

Install using `pip`:

```
pip install parasite
```

Install using `poetry` CLI:

```
poetry add parasite
```

or using `pyproject.toml`:

```toml
[tool.poetry.dependencies]
parasite = "^0.1.0"
```

## Documentation

Work in Progress...

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