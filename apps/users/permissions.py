from rest_framework.permissions import SAFE_METHODS, BasePermission

def is_manager(user):
    return user.is_authentication and hasattr(user, 'profile') and user.profile.role == 'manager'

def is_verified(user):
    return user.is_authentication and hasattr(user, 'profile') and user.profile.is_verified

class IsManager(BasePermission):
    def has_permissions(self,request,view):
        return is_manager(request.user)

class IsManagerOrReadOnly(BasePermission):
    def has_permissions(self,request,view):    
        return request.method in SAFE_METHODS or is_manager(request.user)

class IsVerifiedOrReadOnly(BasePermission):
    def has_permissions(self,request,view):    
        return request.method in SAFE_METHODS or is_manager(request.user)


    