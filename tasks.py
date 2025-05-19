from invoke import task
import os

import http.server as httpserver
import socketserver


BASE_DIR = os.path.realpath(os.path.dirname(__file__))
BUILD_DIR = os.path.join(BASE_DIR, 'build')
SOURCE_DIR = os.path.join(BASE_DIR, 'source')
LOCALE_DIR = os.path.join(SOURCE_DIR, 'locale',
                          '%s', 'LC_MESSAGES')
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
    arg = f"sphinx-build -b {target} -d {os.path.join(BUILD_DIR, 'doctrees')} -D language={language} {src} {dest}"
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
        c.run(f'rm -rfv {os.path.join(BUILD_DIR, target, language)}')
    else:
        c.run(f'rm -rfv {os.path.join(BUILD_DIR, target)}')

@task
def clean_all(c):
    c.run(f'rm -rfv {BUILD_DIR}/*')

@task
def serve(c, port:int=SERVE_PORT, serve_dir:str=None):
    """Run a web server to serve the built project"""
    if serve_dir is None:
        serve_dir = os.path.join(BUILD_DIR, MAIN_TARGET)
    port = int(port)
    os.chdir(serve_dir)
    handler = httpserver.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer(("", port), handler)
    print("serving on http://%s:%s" % httpd.server_address)
    httpd.serve_forever()

@task
def update_pos(c, language:str):
    """Update .po files from the source pot files"""
    if language not in LANGUAGES:
        exit('Language %s not available.' % language)
    gen_pots(c)
    pot_dir = os.path.join(BUILD_DIR, 'gettext')
    arg = f'sphinx-intl update -p {pot_dir} -l {language}'
    c.run(arg)


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
    let sphinx Makefile to the job!
    """
    c.run('make gettext')
