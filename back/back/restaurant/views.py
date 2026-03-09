from django.shortcuts import render
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
from .models import Contact, Reservation

@csrf_exempt
@require_POST
def contact_form(request):
    try:
        data = json.loads(request.body)
        name = data.get('name')
        email = data.get('email')
        subject = data.get('subject')
        message = data.get('message')

        # Save to database
        contact = Contact.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message
        )

        # Send email to admin
        admin_email = getattr(settings, 'ADMIN_EMAIL', 'admin@abwab-el-mansour.com')
        send_mail(
            f'Contact Form: {subject}',
            f'Name: {name}\nEmail: {email}\n\nMessage:\n{message}',
            settings.DEFAULT_FROM_EMAIL,
            [admin_email],
            fail_silently=False,
        )

        # Send confirmation email to user
        send_mail(
            'Votre message a été bien transmis',
            f'Cher/Chère {name},\n\nVotre message a été bien transmis. Nous vous contacterons bientôt.\n\nCordialement,\nL\'équipe d\'Abwab El Mansour',
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )

        return JsonResponse({
            'success': True,
            'message': 'Votre message a été bien transmis'
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': 'Une erreur s\'est produite. Veuillez réessayer.'
        }, status=400)

@csrf_exempt
@require_POST
def reservation_form(request):
    try:
        data = json.loads(request.body)
        name = data.get('name')
        email = data.get('email')
        phone = data.get('phone')
        date = data.get('date')
        time = data.get('time')
        guests = data.get('guests')
        message = data.get('message', '')

        # Save to database
        reservation = Reservation.objects.create(
            name=name,
            email=email,
            phone=phone,
            date=date,
            time=time,
            guests=guests,
            message=message
        )

        # Send email to admin
        admin_email = getattr(settings, 'ADMIN_EMAIL', 'admin@abwab-el-mansour.com')
        send_mail(
            f'New Reservation: {name}',
            f'Name: {name}\nEmail: {email}\nPhone: {phone}\nDate: {date}\nTime: {time}\nGuests: {guests}\n\nMessage:\n{message}',
            settings.DEFAULT_FROM_EMAIL,
            [admin_email],
            fail_silently=False,
        )

        # Send confirmation email to user
        send_mail(
            'Votre réservation a été bien notée',
            f'Cher/Chère {name},\n\nVotre réservation pour le {date} à {time} pour {guests} personne(s) a été bien notée.\n\nNous vous attendons avec impatience !\n\nCordialement,\nL\'équipe d\'Abwab El Mansour',
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )

        return JsonResponse({
            'success': True,
            'message': 'Votre réservation a été bien notée'
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': 'Une erreur s\'est produite. Veuillez réessayer.'
        }, status=400)
