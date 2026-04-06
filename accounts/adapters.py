# File: accounts/adapters.py

from allauth.socialaccount.adapter import DefaultSocialAccountAdapter


class SocialAccountAdapter(DefaultSocialAccountAdapter):

    def pre_social_login(self, request, sociallogin):
        """
        Called after a user successfully authenticates via a social provider
        but before they are logged in. We can use this to link social accounts
        to existing email-matching local accounts.
        """
        pass

    def is_auto_signup_allowed(self, request, sociallogin):
        """
        Allow auto-signup for social logins (no extra form required).
        """
        return True