"""Unit tests for rules.py: no HTTP and no database needed."""
import unittest
from datetime import date

import rules

TODAY = date(2026, 11, 5)  # fixed date so the tests never depend on the real clock


def loan(due_date="2026-11-05", returned=0, fine=0, fine_paid=0):
    return {"due_date": due_date, "returned": returned, "fine": fine, "fine_paid": fine_paid}


class FineTests(unittest.TestCase):
    def test_no_fine_when_returned_early(self):
        self.assertEqual(rules.fine_for("2026-11-10", TODAY), 0)

    def test_no_fine_on_due_date(self):
        self.assertEqual(rules.fine_for("2026-11-05", TODAY), 0)

    def test_one_day_late_costs_fifty_cents(self):
        self.assertEqual(rules.fine_for("2026-11-04", TODAY), 0.50)

    def test_five_days_late_costs_two_fifty(self):
        self.assertEqual(rules.fine_for("2026-10-31", TODAY), 2.50)

    def test_current_fine_of_open_loan_grows_each_day(self):
        self.assertEqual(rules.current_fine(loan(due_date="2026-11-01"), TODAY), 2.0)

    def test_current_fine_of_returned_loan_is_the_stored_fine(self):
        self.assertEqual(rules.current_fine(loan(due_date="2026-11-01", returned=1, fine=1.5), TODAY), 1.5)


class AmountOwedTests(unittest.TestCase):
    def test_nothing_owed_without_loans(self):
        self.assertEqual(rules.amount_owed([], TODAY), 0)

    def test_open_late_loan_counts(self):
        self.assertEqual(rules.amount_owed([loan(due_date="2026-10-31")], TODAY), 2.5)

    def test_unpaid_returned_fine_counts(self):
        self.assertEqual(rules.amount_owed([loan(returned=1, fine=3.0)], TODAY), 3.0)

    def test_paid_fine_does_not_count(self):
        self.assertEqual(rules.amount_owed([loan(returned=1, fine=3.0, fine_paid=1)], TODAY), 0)


class LimitTests(unittest.TestCase):
    def test_student_limit_is_three(self):
        self.assertEqual(rules.loan_limit("student"), 3)

    def test_staff_limit_is_five(self):
        self.assertEqual(rules.loan_limit("staff"), 5)

    def test_loans_remaining_ignores_returned_loans(self):
        loans = [loan(), loan(returned=1)]
        self.assertEqual(rules.loans_remaining("student", loans), 2)


class DateTests(unittest.TestCase):
    def test_new_loan_lasts_14_days(self):
        self.assertEqual(rules.default_due_date(TODAY), "2026-11-19")

    def test_renewal_adds_14_days_to_due_date(self):
        self.assertEqual(rules.renewed_due_date("2026-11-19"), "2026-12-03")

    def test_due_today_is_not_overdue(self):
        self.assertFalse(rules.is_overdue("2026-11-05", TODAY))

    def test_due_yesterday_is_overdue(self):
        self.assertTrue(rules.is_overdue("2026-11-04", TODAY))


if __name__ == "__main__":
    unittest.main()
