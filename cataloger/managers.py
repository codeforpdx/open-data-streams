from django.contrib.auth.models import UserManager

class ProfileManager(UserManager):
    def create_user(self, username, email=None, password=None, department=None, office=None, **extra_fields):
        """
        Creates and saves a User with the given username, email, password, department, and office.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            username = username,
            email=self.normalize_email(email),
            department = department,
            office = office,
        )

        user.set_password(password)
        user.save()
        return user
