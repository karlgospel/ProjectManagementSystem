import pytest
from _pytest import unittest


# def update_task_start_and_end_dates(self, task_id, status):
#     # Set start and end dates based on if status has been updated
#     # Users options are limited to minimise errors
#     try:
#         current_status = self.get_status(task_id)
#         if current_status == 'Not Started' and status == 'In-Progress':
#             set_start_date(task_id)
#         elif current_status == 'In-Progress' and status == 'Completed':
#             self.set_end_date(task_id)
#         elif current_status == 'Not Started' and status == 'Completed':
#             self.set_start_date(task_id)
#             self.set_end_date(task_id)
#         elif current_status == 'Completed' and status == 'In-Progress':
#             self.delete_task_end_date(task_id)
#     except sqlite3.Error as e:
#         print("Error updating task start and end dates:", e)

class TestStringMethods(unittest.UnitTestCase):


    @pytest.fixture
    def prep_input():
        a = 10
        b = 12
        return (a, b)


    def sum(a, b):
        return (a + b)


    def test_sum_equal(prep_input):
        result = sum(prep_input[0], prep_input[1])
        assert result == 22


    def test_sum_greater(prep_input):
        result = sum(prep_input[0], prep_input[1])
        assert result > 20


    def test_sum_less(prep_input):
        result = sum(prep_input[0], prep_input[1])
        assert result < 40

if __name__ == '__main__':
    unittest.main()