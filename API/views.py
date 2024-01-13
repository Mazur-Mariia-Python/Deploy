from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.utils import json
from django.http import JsonResponse

from gift_finder.models import SelectedGift
from .functions import process_gift_picking
from rest_framework import status
import json
from pydantic import ValidationError

from .serializers import SelectedGiftSerializer
from .validators import QuestionnaireAnswers


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


@api_view(["GET"])
# @permission_classes([IsAuthenticated])
def selected_gifts_list(request):
    if request.method == "GET":
        # # Checking if the user is authenticated
        # if not request.user.is_authenticated:
        #     return Response({"error": "Access denied. User is not authenticated."},
        #                     status=status.HTTP_403_FORBIDDEN)

        # Receiving selected gifts for a specific user
        selected_gifts = SelectedGift.objects.filter(user=request.user)
        serializer = SelectedGiftSerializer(selected_gifts, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
