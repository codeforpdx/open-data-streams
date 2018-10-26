from django.contrib.auth.models import UserManager

class ProfileManager(UserManager):
    """
    ProfileManager facilitates the creation of users based on Django's UserManager

    Note:
        This class is based off of the Django UserManager, which in turn is
        based off of the BaseUserManager object.
        https://docs.djangoproject.com/en/2.1/ref/contrib/auth/#manager-methods
    """
    def create_user(self, username, email=None, password=None, bureau=None, division=None, office=None, **extra_fields):
        """
        Creates and saves a Profile with the given username, email, password, and office.
            
        Attributes:
            username (str): username of the user being created
            email (str): e-mail address provided by the user
            password (str): password provided by the user
            bureau (str): bureau provided by user
            division (str): division provided by user
            office (str): office provided by user
            
        Returns:
            Profile: the Profile object that has been created
            
        Raises:
            ValueError: if e-mail address is None
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
