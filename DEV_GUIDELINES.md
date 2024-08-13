# Dev Guidelines

## Publishing workflow

#### Set branch and version

1. Create a branch named exactly after the version you want.
2. Set the new version in **envrac/\_\_init\_\_.py**.

The tests will ensure this is the case, which prevents you accidentally forgetting to increment the version.

#### Build the package

This creates the wheel file in **dist** directory.

```sh
./scripts/build.sh
```

#### Upload to test.pypi

This uploads to test.pypi:

```sh
./scripts/publish-test.sh
```

#### Install from test.pypi

In a different project, run this to uninstall envrac, and install the new version from test.pypi:

```sh
/scripts/install-from-test-pypi.sh
```

#### Check the version:

```
python -c "import envrac; print(envrac.VERSION
```

Check code works as expected.

#### Merge to main

You should have rebased from main to ensure there are no unexpected changes.



Check there are no uncommitted changes.

Run checks, the run the precommit checks and pytest:

```sh
./scripts/publish-test.sh
```



TODO:

* Make checks ensure we have latest changes from master.

