from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
def send_subscription_confirmation_email(email):
    """
    Function to send subscription confirmation email with an HTML template.
    """
    # Define context for the email template
    context = {
        'email': email,
    }

    # Render the HTML email template with the context
    html_message = render_to_string('newsletter_subscription_email.html', context)  # Make sure this template exists
    plain_message = strip_tags(html_message)  # Convert HTML to plain text

    subject = "Welcome to MoreTrek's Newsletter!"
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = email

    # Send the email
    send_mail(
        subject,
        plain_message,  # Plain-text version of the message
        from_email,
        [to_email],
        html_message=html_message  # HTML version of the message
    )