import uuid
from django.db import models
from django.utils.text import slugify
from django.conf import settings



class Establishment(models.Model):
   

    CATEGORY_CHOICES = [
        ('food', 'Food & Dining'),
        ('clothing', 'Clothing & Fashion'),
        ('grocery', 'Grocery & Supermarket'),
        ('electronics', 'Electronics & Tech'),
        ('health', 'Health & Pharmacy'),
        ('beauty', 'Beauty & Salon'),
        ('fitness', 'Fitness & Gym'),
        ('education', 'Education & Coaching'),
        ('entertainment', 'Entertainment & Events'),
        ('services', 'Services & Repair'),
        ('other', 'Other'),
    ]
   

    owner = models.ForeignKey( settings.AUTH_USER_MODEL,on_delete=models.CASCADE, related_name='establishments',)


    name = models.CharField(max_length=200,)

    slug = models.SlugField(
        max_length=250,
        unique=True,
        blank=True,
    )

    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        default='other',
    )

    description = models.TextField(
        blank=True,
    )

    address = models.CharField(
        max_length=500,
        blank=True,
      
    )

    city = models.CharField(
        max_length=100,
        default='',
    )

    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
    )

    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
   
    )

    contact_phone = models.CharField(
        max_length=15,
        blank=True,
    )

    contact_email = models.EmailField(
        blank=True,
    
    )

    photo = models.ImageField(
        upload_to='establishment_photos/',
        null=True,
        blank=True,
    
    )


    is_active = models.BooleanField(
        default=True,
  
    )

    is_verified = models.BooleanField(
        default=False,
    
    )



    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
 

    class Meta:
        verbose_name = 'Establishment'
        verbose_name_plural = 'Establishments'
        ordering = ['-created_at']


    def save(self, *args, **kwargs):
        if not self.slug:
           
            base_slug = slugify(self.name)
        

            slug = base_slug
            counter = 1

            while Establishment.objects.filter(slug=slug).exists():
                slug = f'{base_slug}-{counter}'
                counter += 1
        

            self.slug = slug

        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name} ({self.city})'

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('establishments:detail', kwargs={'slug': self.slug})


class OwnerOTP(models.Model):


    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='otps',
      
    )

    establishment = models.ForeignKey(
        Establishment,
        on_delete=models.CASCADE,
        related_name='otps',
        null=True,
        blank=True,
      
    )

    otp_code = models.CharField(
        max_length=6,
        
    )

    created_at = models.DateTimeField(auto_now_add=True)

    is_used = models.BooleanField(
        default=False,
    )

    expires_at = models.DateTimeField(
    )

    class Meta:
        verbose_name = 'Owner OTP'
        verbose_name_plural = 'Owner OTPs'
        ordering = ['-created_at']

    def __str__(self):
        return f'OTP for {self.user.email} — {"Used" if self.is_used else "Active"}'

    def is_valid(self):
      
        from django.utils import timezone
        return not self.is_used and timezone.now() < self.expires_at
       
# Create your models here.
