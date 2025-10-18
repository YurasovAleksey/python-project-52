import pytest
from django.contrib.auth import get_user_model

from task_manager.statuses.models import Status

User = get_user_model()


@pytest.mark.django_db
class TestStatusCRUD:
    def setup_method(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        self.status = Status.objects.create(name="Тестовый статус")

    def test_status_create_success(self, client):
        client.force_login(self.user)

        data = {"name": "Новый статус"}
        response = client.post("/statuses/create/", data=data, follow=True)

        assert response.status_code == 200
        assert Status.objects.filter(name="Новый статус").exists()

    def test_status_list_view(self, client):
        client.force_login(self.user)
        response = client.get("/statuses/")

        assert response.status_code == 200
        assert "statuses" in response.context

    def test_status_update_success(self, client):
        client.force_login(self.user)

        data = {"name": "Обновленный статус"}
        response = client.post(
            f"/statuses/{self.status.id}/update/", data=data, follow=True
        )

        assert response.status_code == 200
        self.status.refresh_from_db()
        assert self.status.name == "Обновленный статус"

    def test_status_delete_success(self, client):
        client.force_login(self.user)

        response = client.post(
            f"/statuses/{self.status.id}/delete/", follow=True
        )

        assert response.status_code == 200
        assert not Status.objects.filter(id=self.status.id).exists()
