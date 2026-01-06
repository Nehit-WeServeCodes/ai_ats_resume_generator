from rest_framework.permissions import BasePermi

class IsAccountActive(BasePermission):
    """
    Allows access only to active user accounts.
    """
    message = "Accout is inactive or desabled."

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.is_active
        )

class IsSubscriptionValid(BasePermission):
    """
    Placeholder for subscription enforcement.
    """

    message = "Active subscription required."

    def has_permission(self, request, view):
        return True

class HasUsageQuota(BasePermission):
    """
    Placeholder for rate / uasage limits.
    """

    message = "Usage quota exceeded."

    def has_permission(self, request, view):
        return True