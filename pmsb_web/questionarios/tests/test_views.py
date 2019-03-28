from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from questionarios.models import Questionario

User = get_user_model()


class TestViews(TestCase):

    def setUp(self) -> None:
        self.client = Client()
        self.user_test = User.objects.create_user(
            username='12312312312',
            email='test@test.com',
            password='1234567o',
        )

        self.questionario_test = Questionario.objects.create(
            usuario = self.user_test,
            nome='Questionario Test'
        )

    def test_list(self):
        url = reverse("questionarios:list")
        response = self.client.get(url)

        self.assertEquals(response.status_code, 302)

        self.assertTrue(self.client.login(username = '12312312312', password='1234567o'))

        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "questionarios/list.html")

    def test_criar_pergunta_tipo(self):
        url = reverse("questionarios:create_pergunta_tipo", args=[self.questionario_test.pk])
        response = self.client.get(url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'questionarios/pergunta_create.html')
