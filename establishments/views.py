import random
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from .models import Establishment, OwnerOTP
from django.contrib.auth import get_user_model

User = get_user_model()

@login_required
def owner_register(request):

   
    if request.user.user_type == 'owner':
        messages.info(request, 'You are already a verified owner.')
        return redirect('establishments:dashboard')


    if request.method == 'POST':

        # Extract form data from POST
        name = request.POST.get('name', '').strip()
        category = request.POST.get('category', 'other')
        description = request.POST.get('description', '').strip()
        address = request.POST.get('address', '').strip()
        city = request.POST.get('city', '').strip()
        contact_phone = request.POST.get('contact_phone', '').strip()
        contact_email = request.POST.get('contact_email', '').strip()
        latitude = request.POST.get('latitude', '').strip()
        longitude = request.POST.get('longitude', '').strip()
        photo = request.FILES.get('photo')
      

        errors = []

        if not name:
            errors.append('Establishment name is required.')

        if not latitude or not longitude:
            errors.append('Please select your establishment location on the map.')
      

        if errors:
           
            return render(request, 'establishments/register.html', {
                'errors': errors,
                'form_data': request.POST,
                'categories': Establishment.CATEGORY_CHOICES,
            })

        # ---- Create Establishment ----
        establishment = Establishment.objects.create(
            owner=request.user,
            name=name,
            category=category,
            description=description,
            address=address,
            city=city,
            contact_phone=contact_phone,
            contact_email=contact_email,
            latitude=latitude,
            longitude=longitude,
            photo=photo,
            is_verified=False,
            # Not verified yet — OTP step comes next
        )
        

        # ---- Update User Type ----
        request.user.user_type = 'guest_owner'
        request.user.save()
      
        otp_code = str(random.randint(100000, 999999))
       

        # Invalidate any existing unused OTPs for this user
        OwnerOTP.objects.filter(
            user=request.user,
            is_used=False
        ).update(is_used=True)
       

        # Create new OTP record
        OwnerOTP.objects.create(
            user=request.user,
            establishment=establishment,
            otp_code=otp_code,
            expires_at=timezone.now() + timedelta(minutes=30),
           
        )

        # ---- Send OTP Email ----
        from django.core.mail import send_mail
     

        send_mail(
            subject='LocalEves — Your Owner Verification OTP',
            message=f'''
Hello {request.user.get_full_name()},

Your establishment "{name}" has been registered on LocalEves.

Your verification OTP is: {otp_code}

This OTP expires in 30 minutes.

Enter this OTP at: http://127.0.0.1:8000/establishments/verify-otp/

If you did not register on LocalEves, please ignore this email.

— The LocalEves Team
            ''',
            from_email='noreply@localeves.in',
            recipient_list=[request.user.email],
            fail_silently=False,
        )

        messages.success(
            request,
            f'Establishment registered! Check your email for the OTP.'
        )

        return redirect('establishments:verify_otp')

    # GET request — show the empty form
    return render(request, 'establishments/register.html', {
        'categories': Establishment.CATEGORY_CHOICES,
    
    })


@login_required
def verify_otp(request):
   

    # Already verified — no need to be here
    if request.user.user_type == 'owner':
        return redirect('establishments:dashboard')

    # Not even a guest owner — redirect to registration
    if request.user.user_type == 'normal':
        messages.warning(request, 'Please register your establishment first.')
        return redirect('establishments:register')

    if request.method == 'POST':
        entered_otp = request.POST.get('otp_code', '').strip()

        if not entered_otp:
            messages.error(request, 'Please enter the OTP.')
            return render(request, 'establishments/verify_otp.html')

        # Find the most recent unused OTP for this user
        try:
            otp = OwnerOTP.objects.filter(
                user=request.user,
                is_used=False,
            ).latest('created_at')
     
        except OwnerOTP.DoesNotExist:
            messages.error(request, 'No active OTP found. Please register again.')
            return redirect('establishments:register')

        # Check validity using our model method
        if not otp.is_valid():
            messages.error(request, 'This OTP has expired. Please request a new one.')
            return render(request, 'establishments/verify_otp.html')

        # Check if entered code matches stored code
        if otp.otp_code != entered_otp:
            messages.error(request, 'Incorrect OTP. Please try again.')
            return render(request, 'establishments/verify_otp.html')

        # ---- OTP is valid — complete verification ----

        # Mark OTP as used so it can't be reused
        otp.is_used = True
        otp.save(update_fields=['is_used'])

        # Mark establishment as verified
        if otp.establishment:
            otp.establishment.is_verified = True
            otp.establishment.save(update_fields=['is_verified'])

        # Upgrade user to verified owner
        request.user.user_type = 'owner'
        request.user.save(update_fields=['user_type'])

        messages.success(
            request,
            f'Congratulations! Your establishment is now verified on LocalEves.'
        )
        return redirect('establishments:dashboard')

    # GET request — show the OTP entry form
    return render(request, 'establishments/verify_otp.html')


@login_required
def owner_dashboard(request):
  
    if request.user.user_type == 'normal':
        messages.info(request, 'Register your establishment to access the dashboard.')
        return redirect('establishments:register')

   
    establishments = Establishment.objects.filter(owner=request.user)
  

    return render(request, 'establishments/dashboard.html', {
        'establishments': establishments,
        'is_guest': request.user.user_type == 'guest_owner',
        # Tell the template if user is still pending verification
    })


