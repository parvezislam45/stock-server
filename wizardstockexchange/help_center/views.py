from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import ContactMessage
from .serializers import ContactMessageSerializer
from rest_framework.decorators import api_view
from .models import LiveChatMessage
from .serializers import LiveChatMessageSerializer
from django.utils import timezone

@api_view(['POST'])
def live_chat(request):
    if request.method == 'POST':
        sender_name = request.data.get('sender_name', '')
        message_text = request.data.get('message', '')

        # Create a new live chat message
        live_chat_message = LiveChatMessage.objects.create(
            sender_name=sender_name,
            message=message_text,
            timestamp=timezone.now()
        )

        # Serialize the response
        serializer = LiveChatMessageSerializer(live_chat_message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response({'error': 'Invalid HTTP method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

# @api_view(['POST'])
# def help_center(request):
#     if request.method == 'POST':
#         serializer = ContactMessageSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class HelpCenterViewSet(viewsets.ModelViewSet):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
    def create(self, request):
        serializer = ContactMessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ContactMessageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
