from django.db import models


class User(models.Model):
    # Define the choices for the role
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('User', 'User'),
    ]

    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=128)
    confirm_password = models.CharField(max_length=128)
    mail_id = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15, unique=True)
    roles = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = "user"

    # def save(self, *args, **kwargs):
    #     # Automatically enforce roles validity and other logic
    #     if self.password != self.confirm_password:
    #         raise ValueError("Password and Confirm Password do not match.")
    #     super(User, self).save(*args, **kwargs)

class Login(models.Model):
        # Define the choices for the role


        id = models.AutoField(primary_key=True)
        username = models.CharField(max_length=50, unique=True)
        password = models.CharField(max_length=128)
        confirm_password = models.CharField(max_length=128)
        mail_id = models.EmailField(unique=True)

        class Meta:
            db_table = "login_table"




