# Dev Guidelines

## Publishing workflow

This is the overview for publishing.

1. Create a branch named **0.0.3** or whatever.
2. Set the version in **envrac/\_\_init\_\_.py** to match that.
3. Ensure all your changes are committed, and that you have the latest changes from master (this gets checked anyway) because you don't want to publish something that doesn't match the source code that is tagged with that version.
4. Publish to test.pypi with `./scripts/publish-test.sh`
5. Install in another virtualenv with `./scripts/install-from-test-pypi.sh`
6. Open a Python terminal and check version and functionality.
7. Merge to main with `git merge --squash`
8. Publish to pypi and tag `./scripts/publish-live.sh`

#### Notes

Everything is controlled by the **scripts** which generally run the **checks.sh** script first, which:

* Ensures your branch and version match
* You have no uncommitted changes.
* You have the latest changes from main.
* Tests pass.
* Quality checks have run.

