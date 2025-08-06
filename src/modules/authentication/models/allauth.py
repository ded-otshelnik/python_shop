from .user import UserProfile as User

from allauth.account.models import EmailAddress
from django.contrib.auth import get_user_model
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

from utils import Logger

log = Logger.get_instance()

class MyAccountAdapter(DefaultSocialAccountAdapter):
    def new_user(self, request, sociallogin):
        User = get_user_model()
        return User()
    
    def populate_email_address(self, request, sociallogin):
        """
        Override to ensure email address is created for the user.
        """
        email = sociallogin.account.extra_data.get("email")
        verified = sociallogin.account.extra_data.get("verified_email", True)
        primary = sociallogin.account.extra_data.get("primary", True)
        if email:
            EmailAddress.objects.get_or_create(
                user=sociallogin.user,
                email=email,
                verified=verified,
                primary=primary
            )    
        
    def populate_user(self, request, sociallogin, data):
        """
        Override to populate the user with additional data.
        """
        user = sociallogin.user
        user.email = data.get("email", user.email)
        user.realname = data.get("name", user.realname)
        if not user.realname:
            user.realname = data.get("first_name", "") + " " + data.get("last_name", "")
            user.realname = user.realname.strip() or "No real name"
        
        return user
    
    def save_user(self, request, sociallogin, form=None):
        # Create user and populate it with data from the social login
        user = super().save_user(request, sociallogin, form)
        user = self.populate_user(request, sociallogin, sociallogin.account.extra_data)
        log.debug(f"User {user.id} created/updated via social login.")
        user.save()
        
        # Ensure email address is created and associated with the user
        self.populate_email_address(request, sociallogin)
        return user
    