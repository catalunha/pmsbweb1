from django.test import SimpleTestCase
from django.urls import resolve, reverse

from questionarios import views


class TestUrls(SimpleTestCase):

    def test_index(self):
        url = reverse('questionarios:list')
        self.assertEquals(resolve(url).func.view_class, views.QuestionarioListView)
