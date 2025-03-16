import logging
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.core.paginator import Paginator
from .models import Event
from .serializers import EventSerializer
from .permissions import RoleBasedPermission

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EventViewSet(viewsets.ViewSet):
    permission_classes = [RoleBasedPermission]

    def list(self, request):
        logger.info("Received request to list events")
        page = request.GET.get('page', 1)
        per_page = request.GET.get('per_page', 10)
        
        try:
            events = Event.objects.all()
            paginator = Paginator(events, per_page)
            serialized_events = EventSerializer(paginator.get_page(page), many=True)
            logger.info(f"Returning {len(serialized_events.data)} events")
            return Response(serialized_events.data)
        except Exception as e:
            logger.error(f"Error listing events: {str(e)}")
            return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, pk=None):
        logger.info(f"Received request to retrieve event with ID {pk}")
        try:
            event = Event.objects.get(pk=pk)
            logger.info(f"Event {pk} retrieved successfully")
            return Response(EventSerializer(event).data)
        except Event.DoesNotExist:
            logger.warning(f"Event {pk} not found")
            return Response({'error': 'Event not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error retrieving event {pk}: {str(e)}")
            return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request):
        logger.info("Received request to create a new event")
        serializer = EventSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            logger.info("Event created successfully")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.warning("Invalid event data received")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        logger.info(f"Received request to update event {pk}")
        try:
            event = Event.objects.get(pk=pk)
            serializer = EventSerializer(event, data=request.data)
            if serializer.is_valid():
                serializer.save()
                logger.info(f"Event {pk} updated successfully")
                return Response(serializer.data)
            logger.warning(f"Invalid data for event {pk}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Event.DoesNotExist:
            logger.warning(f"Event {pk} not found for update")
            return Response({'error': 'Event not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error updating event {pk}: {str(e)}")
            return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, pk=None):
        logger.info(f"Received request to delete event {pk}")
        try:
            event = Event.objects.get(pk=pk)
            event.delete()
            logger.info(f"Event {pk} deleted successfully")
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Event.DoesNotExist:
            logger.warning(f"Event {pk} not found for deletion")
            return Response({'error': 'Event not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error deleting event {pk}: {str(e)}")
            return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)