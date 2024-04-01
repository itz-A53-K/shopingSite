from django.contrib.auth.base_user import BaseUserManager


#manager to manage custom user model
class customUserManager(BaseUserManager):
    use_in_migrations = True


    def create_user(self, email, password, **extra_fields):

        if not email:
            raise ValueError("ph_No is required")
        
        # email= self.normalize_email(email)
        user= self.model(email=email , **extra_fields)
        user.set_password(password)
        user.save(using= self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(('Super user must have is_staff=True'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        
        return self.create_user(email, password, **extra_fields)