import json
import unittest
from main import *


# class TestSumBoroughRacks(unittest.TestCase):

#     def test_sum_borough_racks(var):
#         borough_name = 'Manhattan'
#         f = open(f"mocks/fake_racks.json")
#         data = json.load(f)
#         rack_count = sum_racks_by_borough(borough_name, data)
#         correct_answer = 1
#         var.assertEqual(correct_answer, rack_count,
#                         f"Should be {correct_answer}")

#     def test_no_racks(var):
#         borough_name = 'Long Island'
#         f = open(f"mocks/fake_racks.json")
#         data = json.load(f)
#         rack_count = sum_racks_by_borough(borough_name, data)
#         correct_answer = 0
#         var.assertEqual(correct_answer,
#                         rack_count, f"Should be {correct_answer}")


# class TestSumRackSubtype(unittest.TestCase):

#     def test_sum_rack_subtype(var):
#         subtype_name = 'U-Rack'
#         f = open(f"mocks/fake_racks.json")
#         data = json.load(f)
#         rack_count = sum_racks_by_subtype(subtype_name, data)
#         correct_answer = 1
#         var.assertEqual(correct_answer, rack_count,
#                         f"Should be {correct_answer}")

#     def test_no_racks(var):
#         subtype_name = 'Hula Hoop'
#         f = open(f"mocks/fake_racks.json")
#         data = json.load(f)
#         rack_count = sum_racks_by_subtype(subtype_name, data)
#         correct_answer = 0
#         var.assertEqual(correct_answer,
#                         rack_count, f"Should be {correct_answer}")


class TestSumRackByNta(unittest.TestCase):

    def test_sum_rack_by_nta(var):
        f = open(f"mocks/fake_racks.json")
        data = json.load(f)
        rack_count = sum_racks_by_nta(data)
        correct_answer = 1
        var.assertEqual(correct_answer, rack_count,
                        f"Should be {correct_answer}")

    # def test_no_racks_in_nta(var):
    #     nta_name = 'North Village'
    #     f = open(f"mocks/fake_racks.json")
    #     data = json.load(f)
    #     rack_count = sum_racks_by_nta(data)
    #     correct_answer = 0
    #     var.assertEqual(correct_answer,
    #                     rack_count, f"Should be {correct_answer}")


# class TestSumRackByYear(unittest.TestCase):

#     def test_sum_racks_by_year(var):
#         year = '2001'
#         f = open(f"mocks/fake_racks.json")
#         data = json.load(f)
#         rack_count = get_dates(data)
#         correct_answer = 1
#         var.assertEqual(correct_answer, rack_count,
#                         f"Should be {correct_answer}")

#     def test_no_racks_year(var):
#         nta_name = 'North Village'
#         f = open(f"mocks/fake_racks.json")
#         borough_data = json.load(f)
#         rack_count = sum_racks_by_subtype(nta_name, borough_data)
#         correct_answer = 0
#         var.assertEqual(correct_answer,
#                         rack_count, f"Should be {correct_answer}")


if __name__ == "__main__":
    unittest.main()
