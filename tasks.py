from invoke import task
import os


BASE_DIR = os.path.realpath(os.path.dirname(__file__))
BUILD_DIR = os.path.join(BASE_DIR, 'build')
SOURCE_DIR = os.path.join(BASE_DIR, 'source')
LOCALE_DIR = os.path.join(SOURCE_DIR, 'locale',
                          '%s', 'LC_MESSAGES')
DOCTREES_DIR = os.path.join(BUILD_DIR, 'doctrees')
POT_DIR = os.path.join(BUILD_DIR, 'gettext')

LANGUAGES = {'en', 'de', 'ru', 'ko', 'es_CL', 'ro'}
MAIN_TARGET = 'html'
REPOSITORY = 'git@github.com:OpenTechSchool/python-beginners.git'
SERVE_PORT = 8000


@task
def setup(c):
    """Setup html build directory to push to repo"""
    clean()
    target_dir = os.path.join(BUILD_DIR, MAIN_TARGET)
    c.run(f'mkdir -p {target_dir}')
    c.run(f'git clone {REPOSITORY} -b gh-pages --single-branch {target_dir}')


@task
def build(c, language:str=None, target:str=MAIN_TARGET):
    if language is None:
        print('Please build a specific language; one of')
        print(', '.join(LANGUAGES))
        exit()
    elif language not in LANGUAGES:
        exit(f'Language {language} not available.')
    if os.path.isdir(LOCALE_DIR % language):
        compile_pos(c,language)


    src = SOURCE_DIR
    dest = os.path.join(BUILD_DIR, target, language)
    arg = f"sphinx-build --builder {target} --doctree-dir {DOCTREES_DIR} --define language={language} {src} {dest}"
    c.run(arg)
    if 'html' in target:
        static_files = os.path.join(BASE_DIR, '_static', '*')
        target_dir = os.path.join(BUILD_DIR, target)
        c.run(f'cp {static_files} {target_dir}' )
    print(f"build finished; the {target} files are in {dest}.")


@task
def build_all(c, target:str=MAIN_TARGET):
    for lang in LANGUAGES:
        build(c, lang, target)


@task
def clean(c, language:str=None, target:str=MAIN_TARGET):
    if language is not None:
        arg = f'rm -rfv {os.path.join(BUILD_DIR, target, language)}'
    else:
        arg = f'rm -rfv {os.path.join(BUILD_DIR, target)}'
    c.run(arg)

@task
def clean_all(c, verbose:bool=False):
    c.run("sphinx-build -M clean source build")

@task
def serve(c, port:int=SERVE_PORT, serve_dir:str=None):
    """Run a web server to serve the built project"""
    raise DeprecationWarning("Use `python -m http.server -d build/html' to run a server")

@task
def update_pos(c, language:str):
    """Update .po files from the source pot files"""
    if language not in LANGUAGES:
        exit('Language %s not available.' % language)
    gen_pots(c)
    arg = f'sphinx-intl update -p {POT_DIR} -l {language}'
    c.run(arg)

@task
def compile_pos(c, language):
    """Compile .po files into .mo files"""
    if language not in LANGUAGES:
        exit(f'Language {language} not available.')
    arg = f"sphinx-intl build -l {language}"
    c.run(arg)

@task
def gen_pots(c):
    """
    Generate .pot templates from sphinx source files
    """
    c.run(f'sphinx-build --builder gettext {SOURCE_DIR} {POT_DIR}')
