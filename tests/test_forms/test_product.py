from django.test import TestCase
from tests.factories.products import CategoryFactory
from product.forms import ProductAddForm


class ProductAddFormTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.category = CategoryFactory.create()

    def setUp(self) -> None:
        self.data = {"name": "Mac Book",
                     "category": self.category.pk,
                     "stock": 11,
                     "price": 11,
                     "available": True}

    def test_fields_required(self):
        self.data.pop("available")
        form = ProductAddForm(data={})
        self.assertEqual(len(self.data),
                         len(form.errors))
        for k, v in self.data.items():
            self.assertEqual(form.errors[k],
                             ["Обязательное поле."])

    def test_category_exists(self):
        self.data.update({"category": 56})
        form = ProductAddForm(data=self.data)
        self.assertEqual(form.errors["category"],
                         ["Выберите корректный вариант. "
                          "Вашего варианта нет "
                          "среди допустимых значений."])

    def test_form_valid(self):
        form = ProductAddForm(data=self.data)
        valid = form.is_valid()
        self.assertTrue(valid)
        self.assertEqual(form.errors, {})
