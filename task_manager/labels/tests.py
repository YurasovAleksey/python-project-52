import pytest
from django.contrib.auth import get_user_model

from task_manager.labels.models import Label

User = get_user_model()


@pytest.mark.django_db
class TestLabelCRUD:
    def setup_method(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        self.label = Label.objects.create(name="Тестовая метка")

    def test_label_create_success(self, client):
        client.force_login(self.user)

        data = {"name": "Новая метка"}
        response = client.post("/labels/create/", data=data, follow=True)

        assert response.status_code == 200
        assert Label.objects.filter(name="Новая метка").exists()

    def test_label_list_view(self, client):
        client.force_login(self.user)
        response = client.get("/labels/")

        assert response.status_code == 200
        assert "labels" in response.context

    def test_label_update_success(self, client):
        client.force_login(self.user)

        data = {"name": "Обновленная метка"}
        response = client.post(
            f"/labels/{self.label.id}/update/", data=data, follow=True
        )

        assert response.status_code == 200
        self.label.refresh_from_db()
        assert self.label.name == "Обновленная метка"

    def test_label_delete_success(self, client):
        client.force_login(self.user)

        response = client.post(f"/labels/{self.label.id}/delete/", follow=True)

        assert response.status_code == 200
        assert not Label.objects.filter(id=self.label.id).exists()
