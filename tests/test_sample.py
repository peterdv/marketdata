# -*- coding: utf-8; mode: python-mode; -*-


def test_always_passes():
    assert True

# def test_always_fails():
#     assert False


def inc(x):
    return x + 1


def test_answer():
    assert inc(3) == 4


#
# The tmp_path fixture will provide a temporary directory
# unique to the test invocation,
# created in the base temporary directory.
#

CONTENT = "content"


#
# The tmp_path fixture will provide a pathlib.Path object
# to a temporary directory which is unique to each test function
# created in the base temporary directory.
#
def test_create_file_tmp_path(tmp_path):
    d = tmp_path / "sub"
    d.mkdir()
    p = d / "hello.txt"
    p.write_text(CONTENT)
    assert p.read_text() == CONTENT
    assert len(list(tmp_path.iterdir())) == 1
    # assert 0


#
# The tmpdir fixture will provide a py.path.local object
# to a temporary directory which is unique to each test function
# created in the base temporary directory.
#
# Replaced by tmp_path.
#
def test_create_file_tmpdir(tmpdir):
    p = tmpdir.mkdir("sub").join("hello.txt")
    p.write(CONTENT)
    assert p.read() == CONTENT
    assert len(tmpdir.listdir()) == 1
    # assert 0
#
# The tmpdir_factory is a session-scoped fixture
# which can be used to create arbitrary temporary directories
# from any other fixture or test
# and return pathlib.Path objects.
#
# For example, suppose your test suite needs a large image on disk,
# which is generated procedurally.
# Instead of computing the same image for each test that uses it
# into its own tmpdir, you can generate it once per-session to save time
#
# See https://docs.pytest.org/en/stable/tmpdir.html
