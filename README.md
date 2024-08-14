# Envrac

*Brings consistency to environment variables.*

## Overview

Envrac (**en**vironment **v**ariable **r**eading **a**nd **c**hecking) is a tiny library for reading environment variables in Python:

```python
>>> from envrac import env
>>> env.int('AGE')
42
```

You should definitely use envrac instead or `os.environ`/`os.getenv` as it:

1. Ensures variables are read consistently (type and default) throughout your project*.
2. Lets you discover all the variables that your project* reads.
3. Removes code bloat for casting types and catching errors etc.
4. Improves safety by not printing the actual values to STDOUT in errors.
5. Handles prefixing, grouping to dictionary, explicit null and other useful bits.

*\* Not just your project, but any imported package which uses envrac too, so spread the word!*

## Installation

Envrac has no dependencies so can be installed easily:

```
pip install envrac
```

## Usage

### Importing

Import `env` exactly like this:

```python
from envrac import env
```

Note that `env` is **an object, not a module**, so this won't work:

```python
# DON'T DO THIS!
from envrac.env import *
from envrac.env import str
```

### Setting variables

Note that environment variables:

- Are always stored as strings.
- Are only set in the current process and any child processes.

The `put` method is a quick way to set and delete environment variables while testing: 

```python
>>> env.put('AGE', 42)
>>> os.environ['AGE']
'42'
>>> env.put('AGE')
>>> os.environ['AGE']
KeyError: 'AGE'
```

This is the equivalent of doing:

```python
>>> os.environ['AGE'] = '42'
>>> del os.environ['AGE']
```

The examples that follow will mostly use the latter to show the type conversion more clearly.

### Reading variables

Read environment variables using methods `str`, `bool`, `int`, `float`, `date`, `datetime` or `time` which work as you'd expect:

```python
>>> os.environ['NAME'] = 'Bob'
>>> os.environ['AGE'] = '42'
>>> os.environ['DOB'] = '2000-01-01'
>>> env.str('NAME')
'Bob'
>>> env.int('AGE')
42
>>> env.date('DOB')
datetime.date(2000, 1, 1)
```

If envrac can't parse the value, you get an error:

```python
>>> os.environ['AGE'] = 'fourty two'
>>> env.int('AGE')
envrac.exceptions.EnvracParsingError: 
  Value for environment variable "AGE" could not be parsed to type `int`.
  Value: ***HIDDEN***
  See envrac documentation for help.
```

> Notice how envrac masks the actual value to minimises the risk of leaking secrets to logs etc. You can override this behaviour in configuration.

### Default values

You can provide default values raw, or as a string:

```python
>>> env.int('SIZE', 10)
10
>>> env.int('SIZE', '10')
10
```

If you don't specify a default, you get an error if the environment variable is not set:

```python
>>> env.str('CITY')
envrac.exceptions.EnvracUnsetVariableError:
  Environment variable "CITY" must be set.
  See envrac documentation for help.
```

### Consistency checks

If you attempt to read a variable using a different default to previously, you get an error:

```python
>>> env.int('SIZE', 10)
10
>>> env.int('SIZE', 11)
envrac.exceptions.EnvracSpecificationError: 
  Environment variable "SIZE" requested differently in multiple places.
  Diff: 
    default: 10 != 11
  See envrac documentation for help.
```

The same applies for going from default to no default or vice versa:

```python
>>> env.int('SIZE')
envrac.exceptions.EnvracSpecificationError: 
  Environment variable "SIZE" requested differently in multiple places.
  Diff: 
    default: 10 != <undefined>
  See envrac documentation for help
```

Note that `<undefined>` (borrowed from JavaScript) is not the same as `None` which is a valid default:

```python
>>> env.int('WEIGHT', None)
None
>>> env.int('WEIGHT')
envrac.exceptions.EnvracSpecificationError: 
 Environment variable "WEIGHT" requested differently in multiple places.
  Diff: 
    default: None != <undefined>
  See envrac documentation for help.
```

You also get an error if you attempt to read a variable using a different type to previously:

```python
>>> os.environ['HEIGHT'] = '175'
>>> env.int('HEIGHT')
175
>>> env.float('HEIGHT')
envrac.exceptions.EnvracSpecificationError: 
  Environment variable "HEIGHT" requested differently in multiple places.
  Diff: 
    type: int != float
  See envrac documentation for help.
```

Ensuring consistency avoids many problems with environment variables, which are already quite accident prone due to typos and such.

Envrac does this by storing the specification from the first attempt to read a variable, including the default values (it doesn't store the read values) in a register. 

While experimenting you can simply `reset` envrac's register:

```python
>>> env.int('AGE')
42
>>> env.reset()
>>> env.str('AGE')
'42'
```

### Dates and booleans

##### Date, datetime and time

These use the type's `fromisoformat` internally so you must use ISO format:

```python
>>> env.date('DATE', '1999-09-10')
>>> env.date('DATETIME', '1999-09-10 16:20:00')
>>> env.date('TIME', '16:20')
```

##### Boolean

Boolean variables must be `1`, `0` `true` or `false` case insensitive:

```python
>>> os.environ['ACTIVE'] = 'TRUE'
>>> env.bool('ACTIVE')
True
```

This restriction prevents arbitrary values from being interpreted as `True` as would happen if you simply used `bool()` :

```python
>>> bool(42)
True
>>> os.environ['AGE'] = '42'
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

### Nullable variables

Sometimes `None` is a valid value, in choices or otherwise:

```python
>>> env.str('FONT_STYLE', choices=[None, 'BOLD', 'ITALIC'])
```

But you cannot set an environment variable to `None`. All you can do is leave it unset, which in the above example will throw an `EnvracUnsetVariableError` as there is no default.

You could set `None` as default, but then you would not detect if a variable is unset or typed wrong:

```python
>>> os.environ['FONT'] = 'BOLD'
>>> env.str('FONT_STYLE', choices=[None, 'BOLD', 'ITALIC'])
envrac.exceptions.EnvracUnsetVariableError: 
  Environment variable "FONT_STYLE" must be set.
  See envrac documentation for help.
```

The way around this is to pass `read_none=True` which interprets `NULL` or `NONE` (case insensitive) as `None`:

```python
>>> env.reset()
>>> os.environ['FONT_STYLE'] = 'none'
>>> env.str('FONT_STYLE', choices=[None, 'BOLD', 'ITALIC'], read_none=True)
None
```

The above forces the environment to set a value as there is no default.

You can still provide a default, which may be something other than `None`:

```python
>>> env.reset()
>>> del os.environ['FONT_STYLE']
>>> env.str('FONT_STYLE', 'BOLD', choices=['BOLD', 'ITALIC', None], read_none=True)
'BOLD'
```

### Read values as dict

You can read multiple environment variables to a dict like so:

```python
>>> os.environ['NAME'] = 'users_db'
>>> os.environ['PORT'] = '5432'
>>> env.dict('NAME', 'PORT:int')
{'DB_NAME': 'users_db', 'DB_PORT': 5432}
```

The syntax is as follows:

```python
'FOO'          # read FOO as a string
'FOO=bar'      # read FOO as a string, default to 'bar'
'FOO:int'      # read FOO as an int
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

The `dict` method doesn't support choices, min or max values. 

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
...   env.dict('NAME', 'PORT:int')
...
{'USER_DB_NAME': 'users_db', 'USER_DB_PORT': 5432}
```

You can also remove the prefix from the dictionary keys:


```python
>>> os.environ['USER_DB_NAME'] = 'users_db'
>>> os.environ['USER_DB_PORT'] = '5432'
>>> with env.prefix('USER_DB_'):
...   env.dict('NAME', 'PORT:int', drop_prefix=False)
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

| Name           | Type | Default | Effect                                               |
| -------------- | ---- | ------- | ---------------------------------------------------- |
| discovery_mode | bool | False   | Suppresses errors so you can discover (see below).   |
| print_values   | bool | False   | Causes values to be printed in errors and discovery. |

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

The idea is to be able to see at a glance all the configuration options that are required or available in your project.

Of course, your code may throw errors for unset/badly set variables. To get around this, set `discovery_mode = True` which suppresses those errors, allowing you to print:

```python
from envrac import env
env.config.discovery_mode = True
import your_code
env.print()
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

If any third party library use envrac too, you will see the environment variables they request. If they don't, why not send them a PR?

### Security considerations

Environment variables often contain sensitive information like passwords, and a simple mistake could easily leak this information:

```python
>>> os.environ['DB_PORT'] = 'MY_BIG_FAT_DB_PASSWORD'
>>> os.environ['DB_PASS'] = '5432'
>>> float(os.environ['DB_PORT'])
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ValueError: could not convert string to float: 'MY_BIG_FAT_DB_PASSWORD'
```

If errors are captured in log files, sent to some third party service or (worst of all) displayed in a web page, this could be a serious problem.

Envrac helps prevent this to a small degree (just make sure `print_values = False` in prod) but can't fully protect you. 

Bear in mind that some logging services will capture local variables. Most services (such as Sentry) have options to scrub sensitive data, however these are only as good as you configure them to be.

## Issues

Please [raise an issue on github](https://github.com/andyhasit/envrac/issues) or submit a PR.

## Licence

MIT

