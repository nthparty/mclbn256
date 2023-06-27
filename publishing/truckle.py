"""
A simple setuptools alternative for packing Python FFI bindings into wheels.
"""
from __future__ import annotations


# import datacable









import base64
import glob
import hashlib
import os
import sys
import zipfile
from typing import Union
import doctest
import toml
from packaging.tags import platform_tags#, parse_tag

from email.parser import Parser
from io import StringIO

def parse(fp):
    return Parser().parse(fp)
def get(msg, header):
    return _collapse_leading_ws(header, msg.get(header))
def get_all(msg, header):
    return [_collapse_leading_ws(header, x) for x in msg.get_all(header)]

def _collapse_leading_ws(header, txt):
    """
    ``Description`` header must preserve newlines; all others need not
    """
    if header.lower() == 'description':  # preserve newlines
        return '\n'.join([x[8:] if x.startswith(' ' * 8) else x
                          for x in txt.strip().splitlines()])
    else:
        return ' '.join([x.strip() for x in txt.splitlines()])

class Distribution(object):
    metadata_version = None
    # version 1.0
    name = None
    version = None
    platforms = ()
    supported_platforms = ()
    summary = None
    description = None
    keywords = None
    home_page = None
    download_url = None
    author = None
    author_email = None
    license = None
    # version 1.1
    classifiers = ()
    requires = ()
    provides = ()
    obsoletes = ()
    # version 1.2
    maintainer = None
    maintainer_email = None
    requires_python = None
    requires_external = ()
    requires_dist = ()
    provides_dist = ()
    obsoletes_dist = ()
    project_urls = ()
    # version 2.1
    provides_extras = ()
    description_content_type = None
    # version 2.2
    dynamic = ()

    def extractMetadata(self):
        data = self.read()
        self.parse(data)

    def read(self):
        raise NotImplementedError

    def _getHeaderAttrs(self):
        HEADER_ATTRS_1_0 = ( # PEP 241
            ('Metadata-Version', 'metadata_version', False),
            ('Name', 'name', False),
            ('Version', 'version', False),
            ('Platform', 'platforms', True),
            ('Supported-Platform', 'supported_platforms', True),
            ('Summary', 'summary', False),
            ('Description', 'description', False),
            ('Keywords', 'keywords', False),
            ('Home-Page', 'home_page', False),
            ('Author', 'author', False),
            ('Author-email', 'author_email', False),
            ('License', 'license', False),
        )

        HEADER_ATTRS_1_1 = HEADER_ATTRS_1_0 + ( # PEP 314
            ('Classifier', 'classifiers', True),
            ('Download-URL', 'download_url', False),
            ('Requires', 'requires', True),
            ('Provides', 'provides', True),
            ('Obsoletes', 'obsoletes', True),
        )

        HEADER_ATTRS_1_2 = HEADER_ATTRS_1_1 + ( # PEP 345
            ('Maintainer', 'maintainer', False),
            ('Maintainer-email', 'maintainer_email', False),
            ('Requires-Python', 'requires_python', False),
            ('Requires-External', 'requires_external', True),
            ('Requires-Dist', 'requires_dist', True),
            ('Provides-Dist', 'provides_dist', True),
            ('Obsoletes-Dist', 'obsoletes_dist', True),
            ('Project-URL', 'project_urls', True),
        )

        HEADER_ATTRS_2_0 = HEADER_ATTRS_1_2  #XXX PEP 426?

        HEADER_ATTRS_2_1 = HEADER_ATTRS_1_2 + ( # PEP 566
            ('Provides-Extra', 'provides_extras', True),
            ('Description-Content-Type', 'description_content_type', False)
        )

        HEADER_ATTRS_2_2 = HEADER_ATTRS_2_1 + ( # PEP 643
            ('Dynamic', 'dynamic', True),
        )

        HEADER_ATTRS = {
            '1.0': HEADER_ATTRS_1_0,
            '1.1': HEADER_ATTRS_1_1,
            '1.2': HEADER_ATTRS_1_2,
            '2.0': HEADER_ATTRS_2_0,
            '2.1': HEADER_ATTRS_2_1,
            '2.2': HEADER_ATTRS_2_2,
        }

        return HEADER_ATTRS.get(self.metadata_version, [])

    def parse(self, data):
        fp = StringIO((data))
        # print('StringIO', StringIO)
        msg = parse(fp)
        # print('must_decode', must_decode)

        if 'Metadata-Version' in msg and self.metadata_version is None:
            value = get(msg, 'Metadata-Version')
            metadata_version = self.metadata_version = value

        for header_name, attr_name, multiple in self._getHeaderAttrs():

            if attr_name == 'metadata_version':
                continue

            if header_name in msg:
                if multiple:
                    values = get_all(msg, header_name)
                    # print(attr_name, '=', value)
                    setattr(self, attr_name, values)
                else:
                    value = get(msg, header_name)
                    if value != 'UNKNOWN':
                        # print(attr_name, '=', value)
                        setattr(self, attr_name, value)

        body = msg.get_payload()
        if body:
            # print('description = ', body)
            setattr(self, 'description', body)

    def __iter__(self):
        for header_name, attr_name, multiple in self._getHeaderAttrs():
            yield attr_name

    iterkeys = __iter__

def build_wheel(extracted_wheel_path: str, wheel_file_name: str = None, platform_tag: str = None) -> str:
    # pylint: disable=C0301 # Accommodates long link URLs.
    """
    Build a wheel.

    Example.

    >>> 1 in [1]
    True
    """

    plattag = platform_tag or next(platform_tags()) or 'py3-none-any'  # or os.path.basename(project_root).split('-')[-1]

    # infofile = 'pyproject.standalone.toml' if 'pyproject.standalone.toml' in pyproject_path else ('pyproject.toml' if 'pyproject.toml' in pyproject_path else None)
    #
    # project_root = pyproject_path[:-len(infofile)]
    project_root = os.path.abspath(extracted_wheel_path)
    #version_guess = [x for x in os.listdir(os.path.join(project_root, os.path.pardir)) if os.path.basename(project_root)+'-' in x and '.dist-info' in x][0][len(os.path.basename(project_root)+'-'):-len('.dist-info')]  # Usually this line would be unnecessary.
    #
    # with open(pyproject_path, 'r') as fd:
    #     pyproject = toml.loads(fd.read())
    #     fd.close()
    # with open(os.path.join(project_root, '-'.join(os.path.basename(project_root).split('-')[:2]) + '.dist-info', 'METADATA'), 'r') as fd:
    # with open(os.path.join(project_root, os.path.basename(project_root) + '-' + version_guess + '.dist-info', 'METADATA'), 'r') as fd:
    with open(os.path.join(project_root, [x for x in os.listdir(project_root) if '.dist-info' in x][0], 'METADATA'), 'r') as fd:
        # pyproject = toml.loads(fd.read())
        pyproject = Distribution()
        pyproject.parse(fd.read())
        fd.close()

    pyproject.new_name = pyproject.name#'csvtables'#pyproject.name + '_bundleable'
    pyproject.old_name = pyproject.name
    pyproject.name = pyproject.new_name

    pyproject.new_version = '1.3.2'#pyproject.version
    pyproject.old_version = pyproject.version
    pyproject.version = pyproject.new_version

    # pyproject = Distribution()
    # pyproject.parse(m)
    # print(vars(pyproject))


    # {distribution}-{version}(-{build tag})?-{python tag}-{abi tag}-{platform tag}.whl
    wheel_file_name = wheel_file_name or F"{pyproject.name}-" \
                                         F"{pyproject.version}-" \
                                         F"py3-" \
                                         F"none-" \
                                         F"{plattag}" \
                                         F".whl"

    if os.path.isdir(os.path.join(project_root, pyproject.old_name)):
        module_root = os.path.join(project_root, pyproject.old_name)
    elif os.path.isdir(os.path.join(project_root, 'src', pyproject.old_name)):
        module_root = os.path.join(project_root, 'src', pyproject.old_name)
    else:
        raise ModuleNotFoundError("Cannot find module source!")

    old_info_root = F"{pyproject.old_name}-{pyproject.old_version}.dist-info"
    info_root = F"{pyproject.name}-{pyproject.new_version}.dist-info"

    # with open(project_root + pyproject['project']['readme'], 'r') as fd:
    #     readme = fd.read()
    #     fd.close()
    readme = pyproject.description

    # metadata = ('METADATA', F"Metadata-Version: 2.1\n" \
    #                         F"Name: {pyproject['project']['name']}\n" \
    #                         F"Version: {pyproject['project']['version']}\n" \
    #                         F"Summary: {pyproject['project']['description']}\n" \
    #                         F"Home-page: {pyproject['project']['urls']['Repository']}\n" \
    #                         F"Author: {pyproject['project']['authors'][0]['name']}\n" \
    #                         F"Author-email: {pyproject['project']['authors'][1]['email']}\n" \
    #                         F"Project-URL: Bug Tracker, {pyproject['project']['urls']['Repository']}"
    #                         F"/issues\n" \
    #                         F"Classifier: Programming Language :: Python :: 3\n" \
    #                         F"Classifier: Operating System :: OS Independent\n" \
    #                         F"Requires-Python: {pyproject['project']['requires-python']}\n" \
    #                         F"Description-Content-Type: text/x-rst\n" \
    #                         F"License-File: LICENSE\n\n{readme}".encode('ascii', 'ignore'))
    metadata = ('METADATA', F"Metadata-Version: 2.1\n" \
                            F"Name: {pyproject.name}\n" \
                            F"Version: {pyproject.version}\n" \
                            F"Summary: {pyproject.summary}\n" \
                            F"Home-page: {pyproject.home_page}\n" \
                            F"Author: {pyproject.author}\n" \
                            F"Author-email: {pyproject.author_email}\n" \
                            # F"Project-URL: Bug Tracker, {pyproject['project']['urls']['Repository']}"
                            F"/issues\n" \
                            F"License: {pyproject.license}\n" \
                            F"Classifier: Programming Language :: Python :: 3\n" \
                            F"Classifier: Operating System :: OS Independent\n" \
                            F"Requires-Python: {pyproject.requires_python}\n" \
                            F"Description-Content-Type: text/x-rst\n" \
                            F"License-File: LICENSE\n\n{readme}".encode('ascii', 'ignore'))
    # F"Classifier: License :: OSI Approved :: MIT License\n" \



    license = ('LICENSE', (
        lambda fd: (
            lambda read:
            fd.close() or read
        )(fd.read())
    )(open(os.path.join(project_root, old_info_root, 'LICENSE'), 'rb')))

    wheel = ('WHEEL', F"Wheel-Version: 1.0\n" \
                      F"Generator: truckle (0.1.x)\n" \
                      F"Root-Is-Purelib: false\n".encode('ascii') +
                     b"\n".join(F"Tag: {tag}".encode('ascii') for tag in plattag.split('.')) + b"\n\n")

    print(wheel[1].decode())

    toplevel = ('top_level.txt', F"{pyproject.name}\n".encode())

    record = ('RECORD', b'')

    pushed_directory = os.getcwd()  # Does Python need push/popd functionality?
    os.chdir(project_root)
    module_file_paths = glob.glob(os.path.join(module_root, '**', '*'), recursive=True)
    os.chdir(module_root)
    module_files = list(map(os.path.relpath,
                            glob.glob(os.path.join(module_root, '**', '*'), recursive=True)))

    module_data = [
        (filepath, open(filepath, 'rb').read())
        for filepath
        in module_files if os.path.isfile(filepath) and '__pycache__' not in filepath
    ]

    record = ('RECORD', '\n'.join(
        (lambda parent_dir: os.path.join(parent_dir, filename))(
            pyproject.name if (i >= 5) else info_root  # 4 == len([m, w, tl, r, l])
        ) + ',sha256='
        + base64.urlsafe_b64encode(hashlib.sha256(contents).digest()).rstrip(b"=").decode()
        + ',' + str(len(contents))
        for i, (filename, contents)
        in reversed(list(enumerate(
            list(reversed([metadata, wheel, toplevel, record, license]))
            + module_data
        )))
    ))

    # # print(metadata)
    # # print(wheel)
    # # print(toplevel)
    # print(record)
    # print()



    module_files_not_pycache = [
        filepath
        for filepath
        in module_files if os.path.isfile(filepath) and '__pycache__' not in filepath
    ]

    files = [
            filepath
            for filepath
            in module_file_paths if os.path.isfile(filepath) and '__pycache__' not in filepath
        ]

    zf = zipfile.ZipFile(os.path.join(project_root, wheel_file_name), 'w')

    for file_relpath, file_path in zip(module_files_not_pycache, files):
        # print(file_path, os.path.join(pyproject.name, file_relpath))
        zf.write(file_path, os.path.join(pyproject.name, file_relpath))
        print(os.path.join(pyproject.name, file_relpath))

    for file_relpath, file_contents in [metadata, wheel, toplevel, record, license]:
        # # print(len(file_contents), os.path.join(info_root, file_relpath))
        # # zf.writestr(file_contents, os.path.join(info_root, file_relpath))
        # print(os.path.join(info_root, file_relpath), len(file_contents))
        zf.writestr(os.path.join(info_root, file_relpath), file_contents)
        print(os.path.join(info_root, file_relpath))
    #
    # zf.close()
    #
    # zf = zipfile.ZipFile(os.path.join(project_root, wheel_file_name), 'r')
    #
    # for i in zf.infolist():
    #     print(f"is_dir: {i.is_dir()}; filename: {i.filename}")
    #
    # zf.close()
    #
    #
    print(F"`{pyproject.name}` v{pyproject.version} wheel built at {os.path.join(project_root, wheel_file_name)}\n")

    os.chdir(pushed_directory)

    return os.path.join(project_root, wheel_file_name)


if __name__ == "__main__":
    doctest.testmod()  # pragma: no cover
    # # truckle('/Users/whowe/Documents/GitHub/mclbn256/setup.cfg')
    plattag = 'macosx_11_0_arm64'
    build_wheel('/Users/whowe/Downloads/datacable-1.1.0-------macosx_11_0_arm64', platform_tag=plattag)
    # # truckle('/Users/whowe/Documents/GitHub/truckle/pyproject.toml')
    # truckle('/Users/whowe/Documents/GitHub/lhe/pyproject.toml')
