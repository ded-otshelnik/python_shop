from django.db import models


class User(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

    @classmethod
    def create_user(cls, username, email, password):
        """
        Create a new user instance.

        :param username: The username for the new user.
        :param email: The email for the new user.
        :param password: The password for the new user.
        :return: User object if created successfully, None otherwise.
        """
        user = cls(username=username, email=email, password=password)
        user.save()
        return user
