from django.contrib.auth.models import UserManager

class ProfileManager(UserManager):
    def create_user(self, username, email=None, password=None, bureau=None, division=None, office=None, **extra_fields):
        """
        Creates and saves a User with the given username, email, password, and office.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            username = username,
            email=self.normalize_email(email),
            bureau = bureau,
            division = division,
            office = office,
        )

        user.set_password(password)
        user.save()
        return user
