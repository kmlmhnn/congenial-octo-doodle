import io
import pytest

from diff import Differ


def test_all_operations_in_order():
    f1 = "abc\ndef\nghi\n"
    f2 = "def\njkl\nmno\n"
    sep = "---\n"
    assert diff_result(f1, f2, sep) == "def\n" + sep + "abc\nghi\n" + sep + "jkl\nmno\n"


@pytest.mark.parametrize(
    "f1, f2, f1nf2, f1_f2, f2_f1",
    [("foo", "", "", "foo", ""), ("", "foo", "", "", "foo"), ("", "", "", "", "")],
)
def test_case_where_f1_or_f2_is_empty(f1, f2, f1nf2, f1_f2, f2_f1):
    sep = "---\n"
    assert diff_result(f1, f2, sep) == f1nf2 + sep + f1_f2 + sep + f2_f1


@pytest.mark.parametrize(
    "f1, f2, f1nf2, f1_f2, f2_f1",
    [("foo", "foo\n", "foo", "", ""), ("foo\nbar", "bar", "bar", "foo\n", "")],
)
def test_case_where_last_line_has_no_trailing_newline(f1, f2, f1nf2, f1_f2, f2_f1):
    sep = "---\n"
    assert diff_result(f1, f2, sep) == f1nf2 + sep + f1_f2 + sep + f2_f1


@pytest.mark.parametrize(
    "f1, f2, f1nf2, f1_f2, f2_f1",
    [("\n\n\n", "\n\n", "\n\n", "\n", ""), ("a\n\n\nb", "\n\nb", "\n\nb", "a\n", "")],
)
def test_empty_lines_are_handled_correctly(f1, f2, f1nf2, f1_f2, f2_f1):
    sep = "---\n"
    assert diff_result(f1, f2, sep) == f1nf2 + sep + f1_f2 + sep + f2_f1


def test_f1_and_f2_preserves_order_and_is_a_proper_subset_of_f1():
    f1 = "\n".join(["1", "2", "3", "4", "5", "6"])
    f2 = "\n".join(["6", "3", "9", "10"])
    fout = io.StringIO()
    d = Differ(io.StringIO(f1), io.StringIO(f2), fout)
    d.print_f1_and_f2()
    fout.seek(0, 0)
    assert fout.read() == "3\n6"


def test_f1_minus_f2_preserves_order_and_is_a_proper_subset_of_f1():
    f1 = "\n".join(["1", "2", "3", "4", "5", "6"])
    f2 = "\n".join(["3", "9", "10", "2", "4"])
    fout = io.StringIO()
    d = Differ(io.StringIO(f1), io.StringIO(f2), fout)
    d.print_f1_minus_f2()
    fout.seek(0, 0)
    assert fout.read() == "1\n5\n6"


def test_f2_minus_f1_preserves_order_and_is_a_proper_subset_of_f2():
    f1 = "\n".join(["1", "2", "3", "4", "5", "6"])
    f2 = "\n".join(["3", "9", "10", "2", "4", "7"])
    fout = io.StringIO()
    d = Differ(io.StringIO(f1), io.StringIO(f2), fout)
    d.print_f2_minus_f1()
    fout.seek(0, 0)
    assert fout.read() == "9\n10\n7"


def diff_result(f1, f2, sep):
    fout = io.StringIO()
    d = Differ(io.StringIO(f1), io.StringIO(f2), fout)
    d.print_f1_and_f2()
    print(sep, file=fout, end="")
    d.print_f1_minus_f2()
    print(sep, file=fout, end="")
    d.print_f2_minus_f1()
    fout.seek(0, 0)
    return fout.read()
