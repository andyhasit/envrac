# TODO:
# check that:
# - there are no uncommitted changes
# - the current commit is tagged and this matches the version
# - the version hasn't been published yet
# - the current commit is on master
# then build and publish.
bash scripts/build.sh
# python -m twine upload --repository pypi dist/*
