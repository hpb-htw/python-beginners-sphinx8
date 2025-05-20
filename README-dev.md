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

### Workflow:

* Generate POT files from source/*.rst
* Generate/update PO files for each language
* For each language:
    * Translate terms in PO files of the language
    * Compile PO file in MO files
* Build a language or all languages

 

### Command for workflow

* To generate POT-file:

```bash
invoke gen-pots
```

* To update/generated PO-files from POT-files:

```bash
invoke update-pos --language=<lang>
```

* To compile all MO-files of a language

```bash
invoke compile-pos --language=<lang>
```

* To compile a single MO-file for debug

```bash
msgfmt "conditional_loops.po" -o "locale/de/LC_MESSAGES/conditional_loops.mo"
```

* To build a language

```bash
invoke build --language=<lang>
```

* To build all languages

```bash
invoke build-all
```

