from django.db import models
from django.contrib.auth.models import User

# Create your models here.from django.db import models

#festival database
class Event(models.Model):
    name = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    date = models.DateField()
    description = models.TextField(null=True, blank=True)


    def __str__(self):
        return self.name

class Participant(models.Model):
    name = models.CharField(max_length=100)
    region = models.CharField(max_length=100, null=True, blank=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True, blank=True)


    def __str__(self):
        return self.name

class Resource(models.Model):
    event = models.ForeignKey(Event, related_name='resources', on_delete=models.CASCADE, default=None)
    category = models.CharField(max_length=50)  
    name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return self.name

class UserDiwaliInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    region = models.CharField(max_length=100, default="Unknown")  # Example default value
    special_sweets = models.CharField(max_length=100, default="Unknown Sweet")
    celebration_description = models.TextField()

    def __str__(self):
        return f"{self.user.username}'s Diwali Info"




#sweet_shop page
class Sweet(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    image = models.ImageField(upload_to='sweets/', blank=True, null=True)  # Image field

    def __str__(self):
        return self.name

class Sale(models.Model):
    sweet = models.ForeignKey(Sweet, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    sale_date = models.DateTimeField(auto_now_add=True)  # auto set to the time of sale

    def __str__(self):
        return f"{self.sweet.name} - {self.quantity} sold"

#diwali wish page       
class DiwaliWish(models.Model):
    name = models.CharField(max_length=100)
    favorite_sweet = models.CharField(max_length=100)
    wish = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Wish for {self.name}"
    
class DiwaliCelebration(models.Model):
    region = models.CharField(max_length=100)
    special_sweets = models.CharField(max_length=100)
    celebration_description = models.TextField()

    def __str__(self):
        return self.region
    
class Diya(models.Model):
    latitude = models.FloatField(default=0.0)  # Default value added
    longitude = models.FloatField(default=0.0)  # Default value added
    status = models.BooleanField(default=False)

    def __str__(self):
        return f"Diya at ({self.latitude}, {self.longitude}) - {'Lit' if self.status else 'Unlit'}"
    
#trivia quiz page
class Question(models.Model):
    question_text = models.CharField(max_length=255)
    option_a = models.CharField(max_length=100)
    option_b = models.CharField(max_length=100)
    option_c = models.CharField(max_length=100)
    option_d = models.CharField(max_length=100)
    correct_answer = models.CharField(max_length=1)  # A, B, C, or D

    def __str__(self):
        return self.question_text


