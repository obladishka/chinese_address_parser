from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from parser.services import find_province, translate_words, find_parent_objects, check_logic, make_translations


class ParserTestCase(APITestCase):

    fixtures = ["address_objects.json", "provinces_fixture.json", "special_words_fixture.json"]

    def test_get(self):
        params = {"address": "浙江省杭州市余杭区五常街道文一西路969号1幢6楼601室"}
        url = reverse("api-page")
        request = self.client.get(url, query_params=params)
        response = request.json()
        correct_response = {
            "region": "Zhejiang Province", 
            "area": "杭州 City", 
            "city": "余杭 District, 五常 Sub-District",
            "street": "文一西 Road", 
            "house_num": "969 No.", 
            "house_ex": "1 Building", 
            "unit_num": "6 Floor, 601 Room"
        }

        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(response, correct_response)

    def test_find_province(self):
        address = "浙江省杭州市余杭区五常街道文一西路969号1幢6楼601室"
        region, address = find_province(address)

        self.assertEqual(region, "Zhejiang Province")
        self.assertEqual(address, "杭州市余杭区五常街道文一西路969号1幢6楼601室")

    def test_translate_words(self):
        address = "深圳市福田区深南大道中段2005号华润大厦"
        address = translate_words(address)

        self.assertEqual(address, "深圳市福田区深南大道中段2005号华润 Plaza, ")

    def test_find_parent_objects(self):
        address = "杭州市余杭区五常街道文一西路969号1幢6楼601室"
        address = find_parent_objects(address)
        correct_answer = {
            "area": "杭州市",
            "city": "余杭区",
            "street": "五常街道文一西路",
            "house_num": "969号",
            "unit_num": "1幢6楼601室"
        }

        self.assertEqual(address, correct_answer)

    def test_check_logic(self):
        address = "杭州市余杭区五常街道文一西路969号1幢6楼601室"
        address = check_logic(address)
        correct_answer = {
            "area": "杭州市",
            "city": "余杭区五常街道",
            "street": "文一西路",
            "house_num": "969号",
            "house_ex": "1幢",
            "unit_num": "6楼601室"
        }

        self.assertEqual(address, correct_answer)

    def test_make_translations(self):
        address = {
            "area": "杭州市",
            "city": "余杭区五常街道",
            "street": "文一西路",
            "house_num": "969号",
            "house_ex": "1幢",
            "unit_num": "6楼601室"
        }
        address = make_translations(**address)
        correct_answer = {
            "area": "杭州 City",
            "city": "余杭 District, 五常 Sub-District",
            "street": "文一西 Road",
            "house_num": "969 No.",
            "house_ex": "1 Building",
            "unit_num": "6 Floor, 601 Room"
        }
        self.assertEqual(address, correct_answer)
