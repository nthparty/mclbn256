import fnmatch
from os import makedirs, path, listdir, walk, remove
from os.path import abspath
from shutil import rmtree
from subprocess import check_call
from sys import executable
from zipfile import ZipFile

import pystache

from truckle import build_wheel

PYPI_PACKAGE_NAME = 'mclbn256'

BINARY_IMPORTS = [
    """import platform
import pkg_resources

def load_library(path_name):
    if platform.system() == 'Windows':
        lib_ext = ".dll"
    elif platform.system() == 'Darwin':
        lib_ext = ".dylib"
    else:
        lib_ext = ".so"
    return cdll.LoadLibrary(pkg_resources.resource_filename('mclbn256', path_name+lib_ext))""",
]

IMPORT_PATCHES = [
    'mclbn256.tmpl',
]

#
# Find the specific platform tags on PyPI for the project you are working with.
#
PLATFORMS = [
    'win32',                  # Windows (x86/AMD 32-bit)
    'win_amd64',              # Windows (x86/AMD 64-bit)
    'manylinux_2_17_x86_64',  # Linux (x86/AMD 64-bit)
    'macosx_10_15_x86_64',    # Intel core macOS (x86/AMD 64-bit)
    'macosx_12_0_arm64',      # Apple silicon macOS (M1/M2/ARM 64-bit)
    'macosx_11_0_universal2', # macOS universal bundle (x86/AMD+M1/M2/ARM 64-bit)
]


for plattag in PLATFORMS:
    build_dir = path.join('.', 'build', plattag)
    src_dir = path.join(build_dir, PYPI_PACKAGE_NAME)
    if path.exists(build_dir):
        rmtree(build_dir)
    makedirs(build_dir)
    check_call([executable, '-m',
        'pip', 'download', PYPI_PACKAGE_NAME+'=='+'1.3.0',
        '--platform='+plattag, '--only-binary=:all:',
        '--dest='+build_dir#, '--version=1.3.0',
    ])

    [wheel_filename] = listdir(build_dir)
    with ZipFile(path.join(build_dir, wheel_filename), 'r') as zip_ref:
        zip_ref.extractall(build_dir)

    src_dir = path.join(build_dir, PYPI_PACKAGE_NAME)

    print(*listdir(src_dir))

    binaries = [path.join(dp, f) for dp, dn, fn in walk(src_dir) for f in fn
                if ('.pyd' in f) or ('.dll' in f) or ('.so' in f) or ('.dylib' in f)]

    # assert len(binaries) == 1 and "Support for multiple binaries (rare edge case) is not yet implemented."

    bss = []
    for binary_path in map(path.join, binaries):

        print('binary_path =', binary_path)

        f = open(binary_path, 'rb')
        bss.append(f.read())
        f.close()
        remove(binary_path)  # Either remove the already-portably-bundled binaries here, or have truckle ignore them.

    assert len(BINARY_IMPORTS) == 1 and "Support for multiple imports (edge case) is not yet implemented."
    assert len(IMPORT_PATCHES) == 1 and "Support for multiple patches (edge case) is not yet implemented."

    #data = {'hex://'+path.relpath(binaries[0], start=src_dir): bs.hex() for i, bs, filepath in enumerate(zip(bss, binary_path))}
    data = {'BINARY_HEX_'+str(i+1): bs.hex() for i, bs in enumerate(bss)}#{'BINARY_HEX': bs.hex()}
    template = open(IMPORT_PATCHES[0], encoding='utf-8').read()
    patched_code = pystache.render(template, data)

    def findReplace(directory, find, replace, filePattern):
        # Citation: https://stackoverflow.com/a/6257321
        for parentpath, dirs, files in walk(abspath(directory)):
            for filename in fnmatch.filter(files, filePattern):
                filepath = path.join(parentpath, filename)
                with open(filepath) as f:
                    s = f.read()
                s = s.replace(find, replace)
                with open(filepath, "w") as f:
                    f.write(s)

    # Inject rendered source patch into src directory file(s).
    findReplace(src_dir, BINARY_IMPORTS[0], patched_code, "*.py")

    build_wheel(build_dir, platform_tag=plattag)




# plattag = 'macosx_11_0_arm64'
# build_wheel('/Users/whowe/Downloads/datacable-1.1.0-------macosx_11_0_arm64', platform_tag=plattag)
