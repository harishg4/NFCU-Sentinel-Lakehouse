from nfcu_sentinel.utils.dq_checks import null_check, uniqueness_check, range_check


def test_null_check() -> None:
    result = null_check([1, None, 3], "amount")
    assert not result.passed


def test_uniqueness_check() -> None:
    result = uniqueness_check(["a", "b", "b"], "id")
    assert not result.passed


def test_range_check() -> None:
    result = range_check([1.0, 5.0, 100.0], "score", 0.0, 10.0)
    assert not result.passed
