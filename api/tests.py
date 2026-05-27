from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import Note
import json

class NoteModelTest(TestCase):
    def test_note_creation(self):
        note = Note.objects.create(body="Test note body")
        self.assertEqual(note.body, "Test note body")
        self.assertEqual(str(note), "Test note body")

class NoteAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.note1 = Note.objects.create(body="First test note")
        self.note2 = Note.objects.create(body="Second test note")

    def test_get_routes(self):
        response = self.client.get(reverse('routes'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)

    def test_get_notes(self):
        response = self.client.get(reverse('notes'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_note(self):
        response = self.client.get(reverse('note', args=[self.note1.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['body'], "First test note")

    def test_create_note(self):
        payload = {'body': "New note created via API"}
        response = self.client.post(
            reverse('create-note'),
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['body'], "New note created via API")
        self.assertEqual(Note.objects.count(), 3)

    def test_update_note(self):
        payload = {'body': "Updated first test note"}
        response = self.client.put(
            reverse('update-note', args=[self.note1.id]),
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.note1.refresh_from_db()
        self.assertEqual(self.note1.body, "Updated first test note")

    def test_delete_note(self):
        response = self.client.delete(reverse('delete-note', args=[self.note1.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Note.objects.count(), 1)
