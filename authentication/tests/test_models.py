import uuid

from django.test import TestCase

from ..models import CustomUser


class CustomUserTest(TestCase):
    """ Test module for CustomUser model """

    def setUp(self):
        self.uuid1 = uuid.uuid4()
        self.uuid2 = uuid.uuid4()
        self.username1 = 'test-username'
        self.username2 = 'maams-ppl-2024'

        CustomUser.objects.create(
            uuid=self.uuid1,
            username=self.username1,
            password="test-password",
            email="test@email.com"
        )
        CustomUser.objects.create(
            uuid=self.uuid2,
            username=self.username2,
            password="maams-ppl",
            email="maams@cs.ui.ac.id"
        )

    def test_custom_user(self):
        """
        Test if model is created and stored in database.
        """
        test_user1 = CustomUser.objects.get(uuid=self.uuid1)
        test_user2 = CustomUser.objects.get(uuid=self.uuid2)

        self.assertEqual(
            str(test_user1), f"User {self.username1} with UUID {self.uuid1}")
        self.assertEqual(
            str(test_user2), f"User {self.username2} with UUID {self.uuid2}")