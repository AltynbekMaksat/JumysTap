from django.test import TestCase

from .models import JobCategory

class JobCategoryModelTests(TestCase):
    def test_category_string_representation(self):
        category = JobCategory.objects.create(name="Flutter Development")
        self.assertEqual(str(category), "Flutter Development")

    def test_category_name_is_required(self):
        field = JobCategory._meta.get_field("name")
        self.assertEqual(field.max_length, 100)
        self.assertTrue(field.unique)