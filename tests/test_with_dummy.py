"""
Tests run on a dummy package
"""
import ubelt as ub
from os.path import join


def make_dummy_package(dpath, pkgname='mkinit_dummy_module'):
    """
    Creates a dummy package structure with or without __init__ files
    """
    root = ub.ensuredir(join(dpath, pkgname))
    ub.delete(root)
    ub.ensuredir(root)
    paths = {
        'root': root,
        'submod1': ub.touch(join(root, 'submod1.py')),
        'submod2': ub.touch(join(root, 'submod2.py')),
        'subdir1': ub.ensuredir(join(root, 'subdir1')),
        'subdir2': ub.ensuredir(join(root, 'subdir2')),
    }
    paths['subdir1_init'] = ub.touch(join(paths['subdir1'], '__init__.py'))
    paths['subdir2_init'] = ub.touch(join(paths['subdir2'], '__init__.py'))
    paths['root_init'] = ub.touch(join(paths['root'], '__init__.py'))

    ub.writeto(paths['subdir1_init'], ub.codeblock(
        '''
        simple_subattr1 = "hello world"
        simple_subattr2 = "hello world"
        _private_attr = "hello world"
        '''))

    ub.writeto(paths['subdir2_init'], ub.codeblock(
        '''
        __all__ = ['public_attr']

        public_attr = "hello world"
        private_attr = "hello world"
        '''))

    ub.writeto(paths['submod1'], ub.codeblock(
        '''
        import six

        attr1 = True
        attr2 = six.moves.zip

        # ------------------------

        if True:
            good_attr_01 = None

        if False:
            bad_attr_false1 = None

        if None:
            bad_attr_none1 = None

        # ------------------------

        if True:
            good_attr_02 = None
        else:
            bad_attr_true2 = None

        if False:
            bad_attr_false2 = None
        else:
            good_attr_03 = None

        if None:
            bad_attr_none2 = None
        else:
            good_attr_04 = None

        # ------------------------

        if True:
            good_attr_05 = None
        elif False:
            bad_attr3 = None
        else:
            bad_attr3 = None

        if False:
            bad_attr_elif_True3_0 = None
        elif True:
            good_attr_06 = None
        else:
            bad_attr_elif_True3_1 = None

        # ------------------------
        import sys

        if sys.version_info.major == 3:
            good_attr_07 = 'py3'
            bad_attr_uncommon4_1 = None
        else:
            good_attr_07 = 'py2'
            bad_attr_uncommon4_0 = None

        # ------------------------
        # This is static, so maybe another_val exists as a global
        if sys.version_info.major == good_attr_07:
            good_attr_08 = None
            bad_attr_uncommon5_1 = None
            bad_attr_uncommon5_0 = None
        elif sys:
            good_attr_08 = None
            bad_attr_uncommon5_1 = None
        else:
            good_attr_08 = None
            bad_attr_uncommon5_0 = None

        # ------------------------
        flag1 = sys.version_info.major < 10
        flag2 = sys.version_info.major > 10
        flag3 = sys.version_info.major > 10

        if flag1:
            bad_attr_num6 = 1
        elif flag2:
            bad_attr_num6 = 1
        elif flag3:
            bad_attr_num6 = 1

        if flag1:
            bad_attr_num6_0 = 1
        elif 0:
            bad_attr_num0 = 1
        elif 1:
            bad_attr_09 = 1
        else:
            bad_attr13 = 1

        if flag1:
            good_attr_09 = 1
        elif 1:
            good_attr_09 = 1
            bad_attr_09_1 = 1
        elif 2 == 3:
            pass

        # ------------------------

        if 'foobar':
            good_attr_10 = 1

        if False:
            bad_attr_str7 = 1
        elif (1, 2):
            good_attr_11 = 1
        elif True:
            bad_attr_true8 = 1

        # ------------------------

        if flag1 != flag2:
            good_attr_12 = None
        else:
            bad_attr_12 = None
            raise Exception

        # ------------------------

        try:
            good_attr_13 = None
            bad_attr_13 = None
        except Exception:
            good_attr_13 = None

        # ------------------------

        try:
            good_attr_14 = None
        except Exception:
            bad_attr_14 = None
            raise

        # ------------------------

        def func1():
            pass

        class class1():
            pass

        if __name__ == '__main__':
            bad_attr_main = None

        if __name__ == 'something_else':
            bad_something_else = None
        '''))
    return paths


def check_dummy_root_init(text):
    for i in range(1, 15):
        want = 'good_attr_{:02d}'.format(i)
        assert want in text, 'missing {}'.format(want)
    assert 'bad_attr' not in text
    assert 'public_attr' in text
    assert 'private_attr' not in text
    assert 'simple_subattr1' in text
    assert 'simple_subattr2' in text
    assert '_private_attr' not in text
    # print('ans = {!r}'.format(ans))


def test_static_import_without_init():
    """
    python ~/code/mkinit/tests/test_with_dummy.py test_static_import_without_init
    """
    import mkinit
    cache_dpath = ub.ensure_app_cache_dir('mkinit/tests')
    paths = make_dummy_package(cache_dpath)
    ub.delete(paths['root_init'])

    modpath = paths['root']
    text = mkinit.static_init(modpath)
    check_dummy_root_init(text)


def test_static_init():
    """
    python ~/code/mkinit/tests/test_with_dummy.py test_static_import_without_init
    """
    import mkinit
    cache_dpath = ub.ensure_app_cache_dir('mkinit/tests')
    paths = make_dummy_package(cache_dpath)

    modpath = paths['root']
    text = mkinit.static_init(modpath)
    check_dummy_root_init(text)


def test_static_find_locals():
    """
    python ~/code/mkinit/tests/test_with_dummy.py test_static_find_locals
    """
    import mkinit
    cache_dpath = ub.ensure_app_cache_dir('mkinit/tests')
    paths = make_dummy_package(cache_dpath)
    ub.delete(paths['root_init'])
    modpath = paths['root']
    imports = list(mkinit.static_mkinit._find_local_submodules(modpath))
    print('imports = {!r}'.format(imports))


def test_dynamic_init():
    """
    python ~/code/mkinit/tests/test_with_dummy.py test_dynamic_init
    """
    import mkinit
    cache_dpath = ub.ensure_app_cache_dir('mkinit/tests')
    paths = make_dummy_package(cache_dpath, 'dynamic_dummy_mod1')
    module = ub.import_module_from_path(paths['root'])
    text = mkinit.dynamic_mkinit.dynamic_init(module.__name__)
    print(text)
    for i in range(1, 15):
        want = 'good_attr_{:02d}'.format(i)
        assert want in text, 'missing {}'.format(want)


if __name__ == '__main__':
    """
    CommandLine:
        python -B %HOME%/code/mkinit/tests/test_with_dummy.py all
    """
    import xdoctest
    xdoctest.doctest_module(__file__)
