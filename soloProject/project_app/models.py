from django.db import models
import re
import bcrypt
# Create your models here.
EMAIL_REGEX = re.compile('^[_a-z0-9-]+(.[_a-z0-9-]+)@[a-z0-9-]+(.[a-z0-9-]+)(.[a-z]{2,4})$')
class UserManager(models.Manager):
    def registration_validator(self, post_data):
        errors = {}
        existing_users = User.objects.filter(email=post_data['email'])
        #length of the first name
        if len(post_data['first_name']) < 2:
            errors['first_name'] = "First name must be 2 characters or more"
        # length of last NameError
        if len(post_data['last_name']) < 2:
            errors['last_name'] = "Last name must be 2 characters or more"
        # email matches format
        # email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-z]+$')
        if len(post_data['email'])==0:
            errors['email'] = "You must enter an email"
        if not EMAIL_REGEX.match(post_data['email']):
            errors['email'] = "Must be a valid email"
        # email is unique
        current_users = User.objects.filter(email = post_data['email'])
        if len(current_users) > 0:
            errors['duplicate'] = "Email already in use"
        # password was entered
        if len(post_data['password']) < 8:
            errors['password'] = "Password must be at least 8 characters long"
        #matches
        if post_data['password'] != post_data['confirm_password']:
            errors['nonmatch'] = "Your password does not match"
        return errors
    
    def login_validator(self, post_data):
        errors = {}
        existing_user = User.objects.filter(email=post_data['email'])
        if len(existing_user) == None:
            errors['email'] = "Email not registered yet"
            return errors
        if len(post_data['email']) == 0:
            errors['email'] = "Enter email"
        if len(post_data['password']) < 8:
            errors['password'] = "Enter 8 character password"
        if not EMAIL_REGEX.match(post_data['email']):
            errors['email'] = "Must be a valid email"
        elif bcrypt.checkpw(post_data['password'].encode(), existing_user[0].password.encode()) != True:
            errors['nonmatch'] = "Email and password do not match"
        return errors
    
    def update_validator(self, post_data):
        errors = {}
        if len(post_data['first_name']) == 0:
            errors['first_name'] = "Please enter a first name!"
        if len(post_data['last_name']) == 0:
            errors['last_name'] = "Please enter a last name!"
        if len(post_data['email']) == 0:
            errors['email'] = "Enter email"
        elif not EMAIL_REGEX.match(post_data['email']):
            errors['email'] = "Must be a valid email"
        return errors

class TaskManager(models.Manager):
    def task_validator(self, post_data):
        errors = {}
        existing_task = Task.objects.filter(task_name=post_data['task_name'])
        if len(post_data['task_name']) < 2:
            errors['task_name'] = "Task name must be 2 characters or more"
        if len(post_data['description']) < 2:
            errors['description'] = "Description must be at least 2 characters"
        if len(post_data['task_name']) == 0:
            errors['task_name'] = "Please enter a name for the task"
        if len(post_data['description']) == 0:
            errors['task_name'] = "Please enter a description for the task"
        if len(existing_task) > 0:
            errors['duplicate'] = "Task name already in use"
        if post_data['due'] == '':
            errors['date'] = "Please enter a Due Date"
        return errors

    def update_task_validator(self, post_data):
        errors = {}
        existing_task = Task.objects.filter(task_name=post_data['task_name'])
        if len(existing_task) > 1:
            errors['duplicate'] = "Task name already in use"
        if len(post_data['task_name']) < 2:
            errors['task_name'] = "Task name must be 2 characters or more"
        if len(post_data['description']) < 2:
            errors['description'] = "Description must be at least 2 characters"
        if len(post_data['task_name']) == 0:
            errors['task_name'] = "Please enter a name for the task"
        if len(post_data['description']) == 0:
            errors['task_name'] = "Please enter a description for the task"
        if post_data['due'] == '':
            errors['date'] = "Please enter a Due Date"
        return errors



class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    skill1 = models.CharField(max_length=50)
    skill2 = models.CharField(max_length=50)
    skill3 = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)

class Task(models.Model):
    task_name = models.CharField(max_length=255)
    description = models.CharField(max_length=750)
    hours = models.CharField(max_length=3)
    due = models.DateField()
    completed = models.BooleanField(default=False)
    assigned = models.ManyToManyField(User, related_name='assigned_tasks')
    creator = models.ForeignKey(User, related_name='tickets', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TaskManager()
    def __str__(self):
        return '%s %s' % (self.task_name, self.description)