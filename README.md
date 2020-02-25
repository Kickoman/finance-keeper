# Finance Keeper

A super budget management system by super developers

## How to run

### Requirements

First of all, of course, you need **Python** on your system. Further there is a list of python
packages that are needed to run this project.

1. Django
2. mysqlclient

**Note about installing mysqlclient:** There are may be some difficulties when you're trying to
run `pip install mysqlclient`. On linux (Ubuntu is tested as well) you need to install `libmysqlclient-dev`,
and `-dev` version of python and maybe `libssl-dev`. On Windows you need to follow [This instructions](https://stackoverflow.com/a/51164104/10767549)

### Running

1. Clone the latest version of `development` branch from repo.
2. `cd` to the directory with file `manage.py`
3. Execute command `python manage.py migrate` (Needed only on first run or when errors about migrations are shown)
4. Run `python manage.py runserver`
5. Open `127.0.0.1:8000` in browser.

If you're using linux, maybe you'll need to replace `python` command with `python3`.