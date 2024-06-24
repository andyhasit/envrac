# Envrac

*Makes using environment variables nicer and safer.*

## Overview

Envrac is a library which solves some of the pain points of working with environment variables in Python:

* Unset variables can cause unpredictable results.
* You may need to parse values to different types.
* You can't readily discover which variables your code wants to read.
* You don't want to leak the values to logs etc.

The word "envrac" is:

  * An abbreviation of **en**vironment **v**ariable **r**eading **a**nd **c**hecking.
  * A play on the French term *"en vrac"*.

## Tutorial

The tutorial takes about 3 minutes and covers all you need to know.

### Installation

You can safely install and uninstall envrac - there are no third party dependencies:

```
pip install envrac
```

### Experimenting

The easiest way to experiment is to open a Python shell and set environment variables using `os.environ`:

```python
>>> import os
>>> os.environ['NAME'] = 'Andy'
>>> os.environ['AGE'] = '42'
```

Note that environment variables are:

- Always stored as strings.
- Loaded into `os.environ` when the Python process starts.
- Only set in the current process and child processes.

So variables you set this way will not affect your shell session or system.

### Importing

Import `env` exactly like this:

```python
>>> from envrac import env
```

Note that `env` is an object, not a module, so **this won't work**:

```python
# DON'T DO THIS
>>> from envrac.env import *
```

### Reading variables

Read environment variables using the method corresponding the type you want:

```python
>>> env.str('NAME')
'Andy'
>>> env.int('AGE')
42
```

The simple read methods available are  `str`, `bool`, `int`, `float` `date`, `datetime` and `time`.

If a variable is not set and no default was provided, you get an error:

```python
>>> env.str('CITY')
envrac.exceptions.EnvracUnsetVariableError:
  Environment variable CITY must be set.
  See envrac documentation for help.
```

### Consistency checks

If you try to read `AGE` as `str` having previously read it as `int` you get an error:

````python
>>> env.str('AGE')
envrac.exceptions.EnvracSpecificationError: 
  Environment variable "AGE" requested differently in multiple places.
  Diff: 
    type: str != int
  See envrac documentation for help.
````

Environment variables are inputs to your program, and should be validated/converted the same way throughout. Envrac helps ensure this.

While experimenting you can simply `clear` envrac's register:

```python
>>> env.clear()
>>> env.str('AGE')
'42'
```

### Default values

You can provide default values raw:

```python
>>> from datetime import date
>>> env.date('DOB', date(2000, 1, 1))
datetime.date(2000, 1, 1)
```

Or as strings:

```python
>>> env.date('DOB', '2000-01-01')
datetime.date(2000, 1, 1)
```

The above didn't raise an error as both dates are the same, but a different default will result in an error: 

```python
>>> env.date('DOB', '1999-09-09')
envrac.exceptions.EnvracSpecificationError: 
  Environment variable "AGE" requested differently in multiple places.
  Diff: 
    default: date(2000, 1, 1) != date(1999, 9, 9)
  See envrac documentation for help.
```

Envrac stores variable specifications but not the values:

```python
>>> os.environ['DOB'] = '2024-06-24'
>>> env.date('DOB', '2000-01-01')
datetime.date(2024, 6, 24)
>>> del os.environ['DOB']
>>> env.date('DOB', '2000-01-01')
datetime.date(2000, 1, 1)
```

### Parsing errors

If the value can't be parsed to that type you get an error:

```python
>>> os.environ['AGE'] = 'fourty two'
>>> env.int('AGE')
envrac.exceptions.EnvracParsingError: 
  Value for environment variable "AGE" could not be parsed to type `int`.
  Value: ***HIDDEN***
  See envrac documentation for help.
```

Notice how envrac hides the value form the print out. This is to reduce the chance of accidentally leaking environment variables, which is a major security risk. You can override this behaviour in configuration.

### Read different types

##### date, datetime and time

These use the type's `fromisoformat` internally so you must use ISO format:

```python
>>> env.date('DATE', '1999-09-10')
>>> env.date('DATETIME', '1999-09-10 16:20:00')
>>> env.date('TIME', '16:20')
```

##### bool

Boolean variables must be `1`, `0` `true` or `false` case insensitive:

```python
>>> os.environ['ACTIVE'] = 'TRUE'
>>> env.bool('ACTIVE')
True
```

This restriction prevents arbitrary values from being interpreted as `True` as would happen if you simply used `bool()` :

```python
>>> os.environ['AGE'] = '42'
>>> bool(42)
True
>>> env.bool('AGE')
  Value for environment variable "AGE" could not be parsed to type `bool`.
  Value: ***HIDDEN***
  Try: 1/0/true/false (case insensitive)
  See envrac documentation for help.
```

### Restrict allowed values

You can specify choices:

```python
>>> os.environ['FONT_STYLE'] = 'Arial'
>>> env.str('FONT_STYLE', choices=['BOLD', 'ITALIC'])
envrac.exceptions.EnvracChoiceError: 
  Environment variable "FONT_STYLE" must be one of "BOLD", "ITALIC".
  value: ***HIDDEN***
  See envrac documentation for help.
```

Or min and/or max values:

```python
>>> os.environ['AGE'] = '100'
>>> env.int('AGE', min_val=12, max_val=45)
envrac.exceptions.EnvracRangeError: 
  Value for environment variable "AGE" must be in range `12` - `45`.
  Value: ***HIDDEN***
  See envrac documentation for help.
```

These options are only applicable to types for which it makes sense.

### Allow None

In some cases `None` is a valid value:

```python
>>> env.str('FONT_STYLE', choices=['BOLD', 'ITALIC', None])
```

However there is no way to set the value to `None` via the environment.

If you set `None` as the default value, you will not detect unset variables, which can easily happen with a typo:

```python
>>> os.environ['F0NT_STYLE'] = 'BOLD'
>>> env.str('FONT_STYLE', None, choices=['BOLD', 'ITALIC', None])
None
```

Another option is to interpret the text `NULL` or `NONE` as `None` which you can do by adding `_` to the method name:

```python
>>> os.environ['F0NT_STYLE'] = 'NONE'
>>> env.str('FONT_STYLE', choices=['BOLD', 'ITALIC', None])
None
```

This protects you against unset variables:

```python
>>> del os.environ['F0NT_STYLE']
>>> env.str('FONT_STYLE', choices=['BOLD', 'ITALIC', None])
envrac.exceptions.EnvracUnsetVariableError: 
  Environment variable "FONT_STYLE" must be set.
  See envrac documentation for help.
```

All the read methods we have seen so far have a counterpart with `_` suffix which will interpret `NULL` or `NONE` (case insensitive) as `None`.

This also allows you to set a default other than `None`:

```python
>>> env.str_('FONT_STYLE', 'BOLD', choices=['BOLD', 'ITALIC', None])
'BOLD'
```

Of course, setting a default puts you back to being vulnerable to unset variables and typos. 

### Read many values at once

You can read many environment variables at once like so:

```python
>>> os.environ['DB_NAME'] = 'users_db'
>>> os.environ['DB_PORT'] = '5432'
>>> env.dict('NAME', 'PORT:int')
{'DB_NAME': 'users_db', 'DB_PORT': 5432}
```

The syntax is as follows:

```python
'FOO'          # read FOO as a string
'FOO=bar      # read FOO as a string, default to 'bar'
'FOO:int'     # read FOO as an int
'FOO:int=0'    # read FOO as an int, default to 0
'?FOO:int'     # read FOO as an int, but allow 'NULL'
'?FOO:int=0'   # read FOO as an int, default to 0, but allow 'NULL'
```

You get the same consistency checks as you would normally:

```python
>>> env.int('AGE')
>>> env.dict('AGE:float')
envrac.exceptions.EnvracSpecificationError: 
  Environment variable "AGE" requested differently in multiple places.
  Diff: 
    type: int != float
  See envrac documentation for help.
```

The `dict` method doesn't support choices, min or max values. If you need to do that:

```python
{
    **env.dict('WIDTH:int', 'HEIGHT:int'),
    'COLOR' = env.str('COLOR', choices=colors)
}
```

### Prefixes

To read multiple environment variables which use the same prefix, use the `prefix` context:

```py
>>> os.environ['USER_DB_NAME'] = 'user_db'
>>> os.environ['USER_DB_PORT'] = '5432'
>>> with env.prefix('USER_DB_'):
...   env.str('NAME')
...   env.int('PORT')
...
'user_db'
5432
```

You typically use this with the `dict` method:


```python
>>> os.environ['USER_DB_NAME'] = 'users_db'
>>> os.environ['USER_DB_PORT'] = '5432'
>>> with env.prefix('USER_DB_'):
...   conn_args = env.dict('NAME', 'PORT:int')
...
{'USER_DB_NAME': 'users_db', 'USER_DB_PORT': 5432}
```

You can also remove the prefix from the dictionary keys:


```python
>>> os.environ['USER_DB_NAME'] = 'users_db'
>>> os.environ['USER_DB_PORT'] = '5432'
>>> with env.prefix('USER_DB_'):
...   conn_args = env.dict('NAME', 'PORT:int', drop_prefix=False)
...
{'NAME': 'users_db', 'PORT': 5432}
```

This only affects the returned dictionary, consistency checks look at the full variable name.

### Configuration

There are two ways to configure envrac:

##### Using environment variables

They are all prefixed with `ENVRAC_CONFIG_` :

```
ENVRAC_CONFIG_DISCOVERY_MODE=true
```

##### Through code

Map the environment variable to lowercase, and drop the prefix:

```python
env.config.discovery_mode = True
```

#### Available options

| Name           | Type | Default | Effect                                                   |
| -------------- | ---- | ------- | -------------------------------------------------------- |
| discovery_mode | bool | False   | Suppresses Unset errors so you can discover (see below). |
| print_values   | bool | False   | Causes values to be printed in errors and discovery.     |

Note that more advanced logging which records variables may still leak the values.

### Discovery

Use the `print` method to print all the environment variables requested through envrac:

```python
>>> env.int('AGE', 10)
>>> env.print()
NAME                  TYPE DEFAULT NULLABLE CHOICES MIN  MAX 
-------------------------------------------------------------
AGE                   int  10      False    None    None None
ENVRAC_DISCOVERY_MODE bool False   False    None    None None
ENVRAC_PRINT_VALUES   bool False   False    None    None None
```

If your throws `UnsetVariableErrors` before you reach this, set `discovery_mode = True` which suppresses those errors:

```python
>>> from envrac import env
>>> env.config.discovery_mode = True
>>> import your_code # won't throw UnsetVariableErrors
>>> env.print()
```

Additionally you can set `print_values = True` which will show you the current raw (uncoverted) value of the environment variable:

```python
>>> os.environ['AGE'] = 'five'
>>> env.config.print_values = True
>>> env.print()
NAME                  TYPE DEFAULT NULLABLE CHOICES MIN  MAX  RAW
-------------------------------------------------------------------
AGE                   int  9       False    None    None None five 
ENVRAC_DISCOVERY_MODE bool False   False    None    None None None 
ENVRAC_PRINT_VALUES   bool False   False    None    None None None 
```

## Issues

Please [raise an issue on github](https://github.com/andyhasit/envrac/issues) or submit a PR.

## Licence

MIT


