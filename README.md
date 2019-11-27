SPyTEx
======

_(this is still in early development, features will be added mostly according
to internal needs, see planned features section at the end)_

**SPyTEx** (_Simple Python Task Executor_) is a small library and CLI utility
allowing to run arbitrary tasks defined in your Python code as ordinary
functions and configured through simple but flexible JSON-based specifications.

Warning
-------

Arbitrary Python code can be run through SPyTEx, even malicious!
**Never run SPyTEx on untrusted input files!**

Motivation
----------

SPyTEx has been created for use in dynamic codebases which do not have one or
few well-defined and stable entry points, but contain a large amount of
interrelated functions and classes which can represent either single tasks by
themselves or be used as parts of larger tasks.

The goal of SPyTEx is to provide a single entry point from which users can run
all these tasks, without the need to create a command line interface (CLI) for
each of them. Once SPyTEx is deployed alongside with your codebase, e.g. in a
Python package distribution or in a Docker container, you can use its CLI to
call arbitrary functions with arbitrary arguments, even if they were not
planned to be used as entry points. Function and arguments are specified in a
JSON file, with a specific syntax allowing to create complex Python objects as
arguments.

While simple Python scripts can be used to launch arbitrary functions inside a
codebase, SPyTEx allows to define tasks in form of JSON files which are a more
standard format and provide some short notations for functionality such as
unpickling objects from local or remote files.

Task specification
------------------

A task is a call to a function (or any callable object). SPyTEx represents
calls in JSON as an object with a `!` entry specifying the full dotted name
(i.e. `package.subpackage.module.name`) of the function to be invoked.

```
{"!": "acme.learn.train_model"}
```

This would be equivalent to launch a Python script like

```
from acme.learn import train_model
train_model()
```

To pass keyword arguments, just add them as entries to the same object.

```
{
  "!": "acme.learn.train_model",
  "data": "trainset.csv",
  "model": "svm"
}

# equivalent to:
from acme.learn import train_model
train_model(data='trainset.csv', model='svm')
```

To pass positional arguments, pass a list with `*` as key.

```
{
  "!": "acme.learn.train_model",
  "*": ["data1.csv", "data2.csv"],
  "model": "svm"
}

# equivalent to:
from acme.learn import train_model
train_model('data1.csv', 'data2.csv', model='svm')
```

In order to pass more complex objects as arguments, a nested invocation can be
specified in place of a single value: such invocation can be a class
instantiation. In the example below we instantiate a [scikit-learn] classifier.

```
{
  "!": "acme.learn.train_model",
  "data": "trainset.csv",
  "model": {
    "!": "sklearn.svm.SVC",
    "C": 0.1,
    "kernel": "poly",
    "degree": 3
  }
}

# equivalent to:
from acme.learn import train_model
from sklearn.svm import SVC
train_model(data='trainset.csv', model=SVC(C=0.1, kernel='poly', degree=3))
```

Running a task
--------------

```
spytex task_file.json
```

Internals
---------

The `spytex` command performs the following key steps:

1. the indicated source file is parsed using Python standard `json` module into
   an object graph made of standard Python objects (dicts, lists, ...);
2. such graph is _compiled_ into a graph of `Definition` objects, which
   formally represent the operators used in SPyTEx JSON (function calls, raw
   values, ...)
3. the `Definition`s in the graph are recursively _resolved_: each of them is
   turned into the object it represents (function calls are executed, raw
   values are unwrapped, ...)

Planned features
----------------

_(in rough priority order)_

- additional operators in JSON, e.g. to pass a date in "YYYY-MM-DD" format or
  to unpickle an object from a file
- support for remote files (HTTP, S3, ...) by integrating [smart-open]
- command-line parameters (referenceable from JSON file) and options (e.g.
  logging configuration)
- support for different syntaxes (e.g. using keywords in place of symbols)
  and/or for JSON alternatives (e.g. [TOML])
- proper documentation
- test suite

[scikit-learn]: https://scikit-learn.org/
[smart-open]: https://pypi.org/project/smart-open/
[TOML]: https://github.com/toml-lang/toml
