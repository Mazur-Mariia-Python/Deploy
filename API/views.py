import stripe
from django.views.decorators.csrf import csrf_exempt
from rest_framework.utils import json
from django.http import JsonResponse
from gift_finder.models import SelectedGift
from .functions import process_gift_picking
from rest_framework import status
import json
from pydantic import ValidationError
from .serializers import SelectedGiftSerializer
from .validators import QuestionnaireAnswers
from django.conf import settings
from django.http import HttpResponse
from .functions import convert_to_cents, fulfill_order
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserSerializer, UserCreationSerializer
from rest_framework.authtoken.models import Token
from .models import CustomUser
from django.shortcuts import get_object_or_404
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import EmailConfirmationToken
from django.db import IntegrityError


@api_view(['POST'])
def api_load_response_data(request):
    try:
        questionnaire_answers_json = request.data["_content"]

        # Parse the JSON data into a Python dictionary
        questionnaire_answers = json.loads(questionnaire_answers_json)

        # Validate questionnaire_answers using Pydantic
        try:
            QuestionnaireAnswers(**questionnaire_answers)
            picked_gifts = process_gift_picking(questionnaire_answers)
            return JsonResponse(picked_gifts, status=status.HTTP_200_OK, safe=False)
        except ValidationError as e:
            print("Validation error:", e)
            return JsonResponse({'Validation error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


stripe.api_key = settings.STRIPE_SECRET_KEY


@api_view(['POST'])
def api_create_checkout_session(request):
    try:
        product_data_json = request.data["_content"]

        # Parse the JSON data into a Python dictionary
        product_data = json.loads(product_data_json)

        try:
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        'price_data': {
                            'currency': 'usd',
                            'unit_amount': convert_to_cents(product_data['price']),
                            'product_data': {
                                'name': product_data['name'],
                                'images': [product_data['image_url'], ]
                            },
                        },
                        'quantity': 1
                    }
                ],
                metadata={
                    'image_url': product_data['image_url'],
                    'name': product_data['name'],
                    'price': product_data['price'],
                    'link': product_data['link']
                },
                mode='payment',
                # success_url=request.build_absolute_uri('/success/'),
                success_url='https://team-2-backend-dn.vercel.app/api/get_gifts/',
                cancel_url=request.build_absolute_uri('/cancel/'),
                automatic_tax={'enabled': False},
            )
        except Exception as e:
            return str(e)
        return JsonResponse({'link': str(checkout_session.url)}, status=status.HTTP_200_OK)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
def stripe_webhook_view(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        # Retrieve the session. If you require line items in the response, you may include them by expanding line_items.
        session = stripe.checkout.Session.retrieve(
            event['data']['object']['id'],
            expand=['line_items'],
        )
        consumption_data = session.get('metadata', {})

        # Fulfill the purchase...
        fulfill_order(consumption_data)

    # Passed signature verification
    return HttpResponse(status=200)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def selected_gifts_list(request):
    if request.method == "GET":
        # Checking if the user is authenticated
        if not request.user.is_authenticated:
            return Response({"error": "Access denied. User is not authenticated."}, status=403)

        # Receiving selected gifts for a specific user
        selected_gifts = SelectedGift.objects.filter(user=request.user)
        serializer = SelectedGiftSerializer(selected_gifts, many=True)

        return Response(serializer.data, status=200)

@api_view(['POST'])
def api_create_user(request):
    try:
        serializer = UserCreationSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            token = Token.objects.create(user=user)
            return Response({"token": token.key, "user": serializer.data}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except IntegrityError as e:
        # Handle the IntegrityError for duplicate email
        return Response({"detail": "This email address already in use."}, status=status.HTTP_409_CONFLICT)


@api_view(['POST'])
def api_login(request):
    try:
        user = get_object_or_404(CustomUser, email=request.data['email'])
    except CustomUser.DoesNotExist:
        return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    if not user.check_password(request.data['password']):
        return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(instance=user)

    return Response({"token": token.key, "user": serializer.data}, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def api_check_authentication(request):
    authenticated = True
    if authenticated:
        user = request.user
        serializer = UserSerializer(instance=user)
        return Response({"authenticated": authenticated, "user": serializer.data}, status=status.HTTP_200_OK)
    else:
        return Response({"authenticated": authenticated}, status=status.HTTP_200_OK)


def confirm_email_view(request):
    token_id = request.GET.get('token_id', None)
    try:
        token = EmailConfirmationToken.objects.get(pk=token_id)
        user = token.user
        user.is_email_confirmed = True
        user.save()
        return HttpResponse('Success', status=status.HTTP_200_OK)
    except EmailConfirmationToken.DoesNotExist:
        return HttpResponse('Error', status=status.HTTP_400_BAD_REQUEST)
