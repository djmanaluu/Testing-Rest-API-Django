from rest_framework import filters, status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.views import APIView

from profile_api import models
from profile_api import permissions
from profile_api import serializers

class HelloApiView(APIView):
    serializer_class = serializers.HelloSerializer

    def get(self, request, format=None):
        an_appview = [
            
        ]

        return Response({
            "message": "Hello",
            "an_appview": an_appview,
        })
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f"Hello {name}"
            return Response({
                "message": message,
            })
        else:
            return Response(
                serializer.errors, 
                status=status.HTTP_400_BAD_REQUEST
            )

    def put(self, request, pk=None):
        return Response({"method": "Put"})

    def patch(self, request, pk=None):
        return Response({"method": "Patch"})

    def delete(self, request, pk=None):
        return Response({"method": "Delete"})

class HelloViewSet(viewsets.ViewSet):
    serializer_class = serializers.HelloSerializer

    def list(self, request):
        an_appview = [
            
        ]

        return Response({
            "message": "Hello",
            "an_appview": an_appview,
        }) 

    def create(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f"Hello {name}"
            return  Response({
                "message": message
            })
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    def retrieve(self, request, pk=None):
        return Response({
            "http_method": "GET"
        })

    def update(self, request, pk=None):
        return Response({
            "http_method": "PUT"
        })

    def partial_update(self, request, pk=None):
        return Response({
            "http_method": "PATCH"
        })

    def destroy(self, request, pk=None):
        return Response({
            "http_method": "DELETE"
        })

class UserProfileViewSet(viewsets.ModelViewSet):
    """Handle creating and updating profiles"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)
    queryset = models.UserProfile.objects.all()
    serializer_class = serializers.UserProfileSerializer
    
    # search profile
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name", "email")

class UserLoginAPIView(ObtainAuthToken):
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

class UserProfileFeedViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (
        permissions.UpdateOwnStatus,
        IsAuthenticatedOrReadOnly
    )
    queryset = models.ProfileFeedItem.objects.all()
    serializer_class = serializers.ProfileFeedItemSerializer
    
    def perform_create(self, serializer):
        serializer.save(user_profile=self.request.user)