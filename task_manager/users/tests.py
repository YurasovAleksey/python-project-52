import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
class TestUserCRUD:
    def setup_method(self):
        self.user1 = User.objects.create_user(
            username="user1",
            password="testpass123",
            first_name="Иван",
            last_name="Иванов",
        )
        self.user2 = User.objects.create_user(
            username="user2",
            password="testpass123",
            first_name="Петр",
            last_name="Петров",
        )
        self.admin = User.objects.create_superuser(
            username="admin",
            password="adminpass123",
            first_name="Админ",
            last_name="Админов",
        )

    def test_user_list_view_authenticated(self, client):
        client.force_login(self.user1)
        response = client.get("/users/")

        assert response.status_code == 200
        assert "users" in response.context
        assert len(response.context["users"]) == 3

    def test_user_list_view_unauthenticated(self, client):
        response = client.get("/users/")
        assert response.status_code == 200

    def test_user_create_view_get(self, client):
        response = client.get("/users/create/")
        assert response.status_code == 200
        assert "form" in response.context

    def test_user_create_success(self, client):
        data = {
            "username": "newuser",
            "first_name": "Новый",
            "last_name": "Пользователь",
            "password1": "TestPass123!",
            "password2": "TestPass123!",
        }

        response = client.post("/users/create/", data=data, follow=True)

        assert response.status_code == 200
        assert User.objects.filter(username="newuser").exists()

        user = User.objects.get(username="newuser")
        assert user.first_name == "Новый"
        assert user.last_name == "Пользователь"

    def test_user_create_invalid_data(self, client):
        data = {
            "username": "",
            "first_name": "Новый",
            "last_name": "Пользователь",
            "password1": "pass",
            "password2": "pass",
        }

        response = client.post("/users/create/", data=data)
        assert response.status_code == 200
        assert "form" in response.context
        assert response.context["form"].errors

    def test_user_update_success(self, client):
        client.force_login(self.user1)

        data = {
            "username": "updateduser",
            "first_name": "Обновленное",
            "last_name": "Имя",
            "password1": "NewPass123!",
            "password2": "NewPass123!",
        }

        response = client.post(
            f"/users/{self.user1.id}/update/", data=data, follow=True
        )

        assert response.status_code == 200
        self.user1.refresh_from_db()
        assert self.user1.first_name == "Обновленное"
        assert self.user1.last_name == "Имя"

    def test_user_update_other_user(self, client):
        client.force_login(self.user1)

        data = {
            "username": "user2updated",
            "first_name": "Чужое",
            "last_name": "Имя",
        }

        response = client.post(
            f"/users/{self.user2.id}/update/", data=data, follow=True
        )

        assert response.status_code in [403, 302, 200]
        self.user2.refresh_from_db()
        assert self.user2.first_name == "Петр"

    def test_user_delete_view_get(self, client):
        client.force_login(self.user1)
        response = client.get(f"/users/{self.user1.id}/delete/")

        assert response.status_code == 200
        assert response.context["object"] == self.user1

    def test_user_delete_success(self, client):
        client.force_login(self.user1)

        response = client.post(f"/users/{self.user1.id}/delete/", follow=True)

        assert response.status_code == 200
        assert not User.objects.filter(id=self.user1.id).exists()

    def test_user_delete_other_user(self, client):
        client.force_login(self.user1)

        response = client.post(f"/users/{self.user2.id}/delete/", follow=True)

        assert response.status_code in [403, 200]
        assert User.objects.filter(id=self.user2.id).exists()
