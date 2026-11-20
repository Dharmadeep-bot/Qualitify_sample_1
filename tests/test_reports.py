from shopapp import reports


def test_discount():
    assert reports.apply_discount_rule("total * 0.5", 10) == 5
