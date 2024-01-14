from django.core.mail import send_mail
from django.template.loader import get_template
from Tobi import settings
from gift_finder.functions import recommend_product_categories, get_list_product_data
from gift_finder.models import SelectedGift


def process_gift_picking(questionnaire_answers):
    product_categories = recommend_product_categories(questionnaire_answers)
    list_of_product_data = get_list_product_data(product_categories, int(questionnaire_answers['budget']))

    return list_of_product_data


def convert_to_cents(dollar_string):
    dollars = float(dollar_string)
    cents = int(dollars * 100)
    return cents


def fulfill_order(consumption_data):
    consumpted_gift = SelectedGift.objects.create(
        name=consumption_data['name'],
        price=consumption_data['price'],
        image_url=consumption_data['image_url'],
        link=consumption_data['link'],
        is_bought=True,
    )

    consumpted_gift.save()

    return None


def send_confirmation_email(user, token):
    data = {
        'user_id': str(user.id),
        'token_id': str(token.id),
    }
    message = get_template('confirmation_email.txt').render(data)
    send_mail(
        subject='Please confirm Email',
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user.email],
        fail_silently=False
    )
