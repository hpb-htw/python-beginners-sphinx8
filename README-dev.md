# Setup Project

## Set up a working environment
This project requires python>=3.13 to run sphinx 8.2

```bash
python3.13 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Translation

<https://www.sphinx-doc.org/en/master/usage/advanced/intl.html>

* To generate POT-file:

```bash
make gettext
```

* To update/generated PO-files:

```bash
sphinx-intl update -p build/gettext -l de
```

* To update MO-file

```bash
msgfmt "conditional_loops.po" -o "locale/de/LC_MESSAGES/conditional_loops.mo"
```
