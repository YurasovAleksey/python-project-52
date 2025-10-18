import pytest
from django.contrib.auth import get_user_model
from task_manager.tasks.models import Task
from task_manager.statuses.models import Status
from task_manager.labels.models import Label

User = get_user_model()


@pytest.mark.django_db
class TestTaskCRUD:
    def setup_method(self):
        self.user1 = User.objects.create_user(
            username='testuser1',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='testuser2', 
            password='testpass123'
        )
        
        self.status_new = Status.objects.create(name='Новый')
        self.status_done = Status.objects.create(name='Завершен')
        
        self.label_bug = Label.objects.create(name='Баг')
        self.label_feature = Label.objects.create(name='Функция')
        
        self.task = Task.objects.create(
            name='Тестовая задача',
            description='Описание тестовой задачи',
            status=self.status_new,
            author=self.user1,
            executor=self.user2
        )
        self.task.labels.add(self.label_bug)
    
    def test_task_create_view_get(self, client):
        client.force_login(self.user1)
        response = client.get('/tasks/create/')
        
        assert response.status_code == 200
        assert 'form' in response.context

    def test_task_create_success(self, client):
        client.force_login(self.user1)
        
        data = {
            'name': 'Новая задача',
            'description': 'Описание новой задачи',
            'status': self.status_new.id,
            'executor': self.user2.id,
            'labels': [self.label_bug.id]
        }
        
        response = client.post('/tasks/create/', data=data, follow=True) 
        
        assert response.status_code == 200
        assert Task.objects.filter(name='Новая задача').exists()
        
        task = Task.objects.get(name='Новая задача')
        assert task.author == self.user1
        assert task.executor == self.user2
        assert task.status == self.status_new

    def test_task_create_unauthenticated(self, client):
        data = {
            'name': 'Новая задача',
            'status': self.status_new.id,
        }
        
        response = client.post('/tasks/create/', data=data)
        assert response.status_code == 302
        assert '/login/' in response.url
    
    def test_task_detail_view(self, client):
        client.force_login(self.user1)
        response = client.get(f'/tasks/{self.task.id}/')
        
        assert response.status_code == 200
        assert response.context['task'] == self.task

    def test_task_detail_view_unauthenticated(self, client):
        response = client.get(f'/tasks/{self.task.id}/')
        assert response.status_code == 302
        assert '/login/' in response.url
    
    def test_task_update_view_get(self, client):
        client.force_login(self.user1)
        response = client.get(f'/tasks/{self.task.id}/update/')
        
        assert response.status_code == 200
        assert 'form' in response.context
        assert response.context['object'] == self.task

    def test_task_update_success(self, client):
        client.force_login(self.user1)
        
        data = {
            'name': 'Обновленная задача',
            'description': 'Новое описание',
            'status': self.status_done.id,
            'executor': self.user1.id,
            'labels': [self.label_feature.id]
        }
        
        response = client.post(f'/tasks/{self.task.id}/update/', data=data, follow=True)
        
        assert response.status_code == 200
        self.task.refresh_from_db()
        assert self.task.name == 'Обновленная задача'
        assert self.task.status == self.status_done

    def test_task_update_unauthenticated(self, client):
        data = {'name': 'Новое название', 'status': self.status_new.id}
        response = client.post(f'/tasks/{self.task.id}/update/', data=data)
        assert response.status_code == 302
        assert '/login/' in response.url
    
    def test_task_delete_view_get(self, client):
        client.force_login(self.user1)
        response = client.get(f'/tasks/{self.task.id}/delete/')
        
        assert response.status_code == 200
        assert response.context['object'] == self.task

    def test_task_delete_by_author(self, client):
        client.force_login(self.user1)
        
        response = client.post(f'/tasks/{self.task.id}/delete/', follow=True)
        
        assert response.status_code == 200
        assert not Task.objects.filter(id=self.task.id).exists()

    def test_task_delete_by_non_author(self, client):
        client.force_login(self.user2)
        
        response = client.post(f'/tasks/{self.task.id}/delete/', follow=True)
        
        assert response.status_code == 200
        assert Task.objects.filter(id=self.task.id).exists()

    def test_task_delete_unauthenticated(self, client):
        response = client.post(f'/tasks/{self.task.id}/delete/')
        assert response.status_code == 302
        assert '/login/' in response.url
