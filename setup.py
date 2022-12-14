# :coding: utf-8
# :copyright: Copyright (c) 2016 ftrack

import os
import re
import shutil

import pip
import setuptools
from pip._internal import main as pip_main
from pkg_resources import parse_version
from setuptools import find_packages, setup
from setuptools.command.test import test as TestCommand

if parse_version(pip.__version__) < parse_version('19.3.0'):
    raise ValueError('Pip should be version 19.3.0 or higher')


FTRACK_CONNECT_PIPELINE_VERSION = '0.8.4'

PLUGIN_NAME = 'ftrack-connect-nuke-publish-{0}'

ROOT_PATH = os.path.dirname(os.path.realpath(__file__))
SOURCE_PATH = os.path.join(ROOT_PATH, 'source')
README_PATH = os.path.join(ROOT_PATH, 'README.rst')

RESOURCE_PATH = os.path.join(
    ROOT_PATH, 'resource'
)

HOOK_PATH = os.path.join(
    ROOT_PATH, 'hook'
)

BUILD_PATH = os.path.join(
    ROOT_PATH, 'build'
)

STAGING_PATH = os.path.join(
    BUILD_PATH, PLUGIN_NAME
)

# Read version from source.
with open(os.path.join(
    SOURCE_PATH, 'ftrack_connect_nuke_publish', '_version.py')
) as _version_file:
    VERSION = re.match(
        r'.*__version__ = \'(.*?)\'', _version_file.read(), re.DOTALL
    ).group(1)

# Update staging path with the plugin version
STAGING_PATH = STAGING_PATH.format(VERSION)


# Custom commands.
class PyTest(TestCommand):
    '''Pytest command.'''

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        '''Import pytest and run.'''
        import pytest
        errno = pytest.main(self.test_args)
        raise SystemExit(errno)


class BuildPlugin(setuptools.Command):
    '''Build plugin.'''
    description = 'Download dependencies and build plugin .'

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        '''Run the build step.'''
        # Clean staging path
        shutil.rmtree(STAGING_PATH, ignore_errors=True)

        # Copy plugin files
        shutil.copytree(
            RESOURCE_PATH,
            os.path.join(STAGING_PATH, 'resource')
        )

        # Copy plugin files
        shutil.copytree(
            HOOK_PATH,
            os.path.join(STAGING_PATH, 'hook')
        )

        pip_main.main(
            [
                'install',
                '.',
                '--target',
                os.path.join(STAGING_PATH, 'dependencies')
            ]
        )

        result_path = shutil.make_archive(
            os.path.join(
                BUILD_PATH,
                PLUGIN_NAME.format(VERSION)
            ),
            'zip',
            STAGING_PATH
        )

        print 'Result: ' + result_path


# Configuration.
setup(
    name='ftrack-connect-nuke-publish',
    version=VERSION,
    description='A dialog to publish assets from Nuke to ftrack using pyblish.',
    long_description=open(README_PATH).read(),
    keywords='ftrack',
    url='https://bitbucket.org/ftrack/ftrack-connect-nuke-publish',
    author='ftrack',
    author_email='support@ftrack.com',
    license='Apache License (2.0)',
    packages=find_packages(SOURCE_PATH),
    package_dir={
        '': 'source'
    },
    setup_requires=[
        'sphinx >= 1.2.2, < 2',
        'sphinx_rtd_theme >= 0.1.6, < 2',
        'lowdown >= 0.1.0, < 2'
    ],
    install_requires=[
        'clique==1.3.1',
        'pyblish-base >= 1.4.3',
        (
            'ftrack-connect-pipeline @ https://bitbucket.org/ftrack/'
            'ftrack-connect-pipeline/get/{0}.zip'
            '#egg=ftrack-connect-pipeline-{0}'
        ).format(FTRACK_CONNECT_PIPELINE_VERSION),
        (
            'qtext @ git+https://bitbucket.org/ftrack/qtext/get/0.2.2.zip'
            '#egg=QtExt-0.2.2'
        )
    ],
    tests_require=[
        'pytest >= 2.3.5, < 3'
    ],
    cmdclass={
        'test': PyTest,
        'build_plugin': BuildPlugin
    },
    zip_safe=False
)
