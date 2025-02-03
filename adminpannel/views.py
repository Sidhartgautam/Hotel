from rest_framework import generics, status
from rest_framework.views import APIView
from core.utils.response import PrepareResponse
from core.utils.permissions import IsHotelAndHotelOwnerPermission
from property.models import (Property,
                             ParkingInfo,
                             BreakfastInfo,
                             Policy,
                             PropertyAmenities,
                             PropertyImage,
                             CancellationPolicy
                             
)

from rooms.models import (
    RoomAmenities,
    RoomType,
    RoomBed,
    Price,
    RoomImages


)

from offers.models import WeeklyOffer
from .serializers import (PropertySerializer,
                          ParkingInfoSerializer,
                          BreakfastInfoSerializer,
                          BulkPropertyAmenitiesSerializer,
                          BulkPropertyImageSerializer,
                          PolicySerializer,
                          PropertyAmenityUpdateSerializer,
                          PropertyImageSerializer,
                          BulkRoomImagesSerializer,
                          RoomAmenitiesSerializer,
                          RoomTypeSerializer,
                          RoomBedSerializer,
                          PriceSerializer,
                          RoomImagesSerializer,
                          CancellationPolicySerializer,
                          WeeklyOfferSerializer,
                          PropertyFAQCreateSerializer

)


#########################PropertyCreationApi###################################

class PropertyCreateView(generics.CreateAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    permission_classes = [IsHotelAndHotelOwnerPermission] 

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            property_instance = serializer.save()
            return PrepareResponse(
                success=True,
                message="Property created successfully",
                data=serializer.data,
            ).send(200)
        except Exception as e:
            return PrepareResponse(
                success=False,
                message="Failed to create property",
                errors=str(e),
            ).send(400)

class ParkingInfoCreateView(generics.CreateAPIView):
    queryset = ParkingInfo.objects.all()
    serializer_class = ParkingInfoSerializer
    permission_classes = [IsHotelAndHotelOwnerPermission] 

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            parking_info_instance = serializer.save()
            return PrepareResponse(
                success=True,
                message="Parking information added successfully",
                data=serializer.data,
            ).send(200)
            
        except Exception as e:
            return PrepareResponse(
                success=False,
                message="Failed to add parking information",
                errors=str(e),
            ).send(400)
        
class BreakfastInfoCreateView(generics.CreateAPIView):
    queryset = BreakfastInfo.objects.all()
    serializer_class = BreakfastInfoSerializer
    permission_classes = [IsHotelAndHotelOwnerPermission]  # Add custom permission

    def create(self, request, *args, **kwargs):
        """
        Overrides the default create method to use PrepareResponse for custom responses.
        """
        serializer = self.get_serializer(data=request.data)
        try:

            serializer.is_valid(raise_exception=True)
            breakfast_info_instance = serializer.save()
            return PrepareResponse(
                success=True,
                message="Breakfast information added successfully",
                data=serializer.data,
            ).send(201)
            
        except Exception as e:
            return PrepareResponse(
                success=False,
                message="Failed to add breakfast information",
                errors=str(e),
            ).send(400)
            
class PropertyAmenitiesCreateView(generics.CreateAPIView):
    serializer_class = BulkPropertyAmenitiesSerializer
    permission_classes = [IsHotelAndHotelOwnerPermission]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            property_amenities = serializer.save()

            return PrepareResponse(
                success=True,
                message="Property amenities added successfully",
                data={
                    "added_amenities": [
                        {
                            "amenity_id": amenity.amenity.id,
                            "amenity_name": amenity.amenity.name,
                            "property_name": amenity.property.property_name,
                        }
                        for amenity in property_amenities
                    ]
                },
            ).send(200)
        except Exception as e:
            return PrepareResponse(
                success=False,
                message="Failed to add property amenities",
                errors=str(e),
            ).send(400)
        

class PropertyImageCreateView(generics.CreateAPIView):
    serializer_class = BulkPropertyImageSerializer
    permission_classes = [IsHotelAndHotelOwnerPermission]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            # Validate and save the images
            serializer.is_valid(raise_exception=True)
            property_images = serializer.save()

            return PrepareResponse(
                success=True,
                message="Property images added successfully",
                data={
                    "added_images": [
                        {
                            "id": image.id,
                            "property": image.property.id,
                            "image_url": image.image.url,
                        }
                        for image in property_images
                    ]
                },
            ).send(201)
           
        except Exception as e:
            return PrepareResponse(
                success=False,
                message="Failed to add property images",
                errors=str(e),
            ).send(400)
        
class PolicyCreateView(generics.CreateAPIView):
    queryset = Policy.objects.all()
    serializer_class = PolicySerializer
    permission_classes = [IsHotelAndHotelOwnerPermission]

    def create(self, request, *args, **kwargs):
        """
        Overrides the default create method to use PrepareResponse for custom responses.
        """
        serializer = self.get_serializer(data=request.data)
        try:
            # Validate the request data
            serializer.is_valid(raise_exception=True)
            policy_instance = serializer.save()

            # Prepare a successful response
            return PrepareResponse(
                success=True,
                message="Policy added successfully",
                data=serializer.data,
            ).send(201)
            
        except Exception as e:
            return PrepareResponse(
                success=False,
                message="Failed to add policy",
                errors=str(e),
            ).send(400)
class CancellationPolicyCreateView(generics.CreateAPIView):
    queryset = CancellationPolicy.objects.all()
    serializer_class = CancellationPolicySerializer
    permission_classes = [IsHotelAndHotelOwnerPermission]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            cancellation_policy = serializer.save()
            return PrepareResponse(
                success=True,
                message="Cancellation policy created successfully",
                data=serializer.data
            ).send(status.HTTP_201_CREATED)
        except Exception as e:
            return PrepareResponse(
                success=False,
                message="Failed to create cancellation policy",
                errors=str(e)
            ).send(status.HTTP_400_BAD_REQUEST)
###############################PropertyUpdateApi#######################################
class PropertyUpdateDeleteView(generics.GenericAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    permission_classes = [IsHotelAndHotelOwnerPermission]

    def patch(self, request, *args, **kwargs):
        """
        Handles partial updates of a property.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        try:
            serializer.is_valid(raise_exception=True)
            updated_instance = serializer.save()
            return PrepareResponse(
                success=True,
                message="Property updated successfully",
                data=serializer.data,
            ).send(200)
        except Exception as e:
            return PrepareResponse(
                success=False,
                message="Failed to update property",
                errors=str(e),
            ).send(400)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            instance.delete()
            return PrepareResponse(
                success=True,
                message="Property deleted successfully",
                data={},
            ).send(200)
        except Exception as e:
            return PrepareResponse(
                success=False,
                message="Failed to delete property",
                errors=str(e),
            ).send(400)

class ParkingInfoUpdateDeleteView(generics.GenericAPIView):
    queryset = ParkingInfo.objects.all()
    serializer_class = ParkingInfoSerializer
    permission_classes = [IsHotelAndHotelOwnerPermission]

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        try:
            serializer.is_valid(raise_exception=True)
            updated_instance = serializer.save()
            return PrepareResponse(
                success=True,
                message="Parking info updated successfully",
                data=serializer.data,
            ).send(200)
        except Exception as e:
            return PrepareResponse(
                success=False,
                message="Failed to update parking info",
                errors=str(e),
            ).send(400)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            instance.delete()
            return PrepareResponse(
                success=True,
                message="Parking info deleted successfully",
                data={},
            ).send(200)
        except Exception as e:
            return PrepareResponse(
                success=False,
                message="Failed to delete parking info",
                errors=str(e),
            ).send(400)
        
class BreakfastInfoUpdateDeleteView(generics.GenericAPIView):
    queryset = BreakfastInfo.objects.all()
    serializer_class = BreakfastInfoSerializer
    permission_classes = [IsHotelAndHotelOwnerPermission]

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        try:
            serializer.is_valid(raise_exception=True)
            updated_instance = serializer.save()
            return PrepareResponse(
                success=True,
                message="Breakfast info updated successfully",
                data=serializer.data,
            ).send(200)
        except Exception as e:
            return PrepareResponse(
                success=False,
                message="Failed to update breakfast info",
                errors=str(e),
            ).send(400)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            instance.delete()
            return PrepareResponse(
                success=True,
                message="Breakfast info deleted successfully",
                data={},
            ).send(200)
        except Exception as e:
            return PrepareResponse(
                success=False,
                message="Failed to delete breakfast info",
                errors=str(e),
            ).send(400)

class PolicyUpdateDeleteView(generics.GenericAPIView):
    queryset = Policy.objects.all()
    serializer_class = PolicySerializer
    permission_classes = [IsHotelAndHotelOwnerPermission]

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        try:
            serializer.is_valid(raise_exception=True)
            updated_instance = serializer.save()
            return PrepareResponse(
                success=True,
                message="Policy updated successfully",
                data=serializer.data,
            ).send(200)
        except Exception as e:
            return PrepareResponse(
                success=False,
                message="Failed to update policy",
                errors=str(e),
            ).send(400)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            instance.delete()
            return PrepareResponse(
                success=True,
                message="Policy deleted successfully",
                data={},
            ).send(200)
        except Exception as e:
            return PrepareResponse(
                success=False,
                message="Failed to delete policy",
                errors=str(e),
            ).send(400)
        
class PropertyAmenitiesUpdateDeleteView(generics.GenericAPIView):
    queryset = PropertyAmenities.objects.all()
    serializer_class = PropertyAmenityUpdateSerializer
    permission_classes = [IsHotelAndHotelOwnerPermission]

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()  # Fetch the PropertyAmenities instance using the URL `pk`
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        try:
            serializer.is_valid(raise_exception=True)
            updated_instance = serializer.save()
            return PrepareResponse(
                success=True,
                message="Property amenity updated successfully",
                data={
                    "id": updated_instance.id,
                    "amenity": updated_instance.amenity.id,
                    "property": updated_instance.property.id,
                    "is_available": updated_instance.is_available,
                },
            ).send(status.HTTP_200_OK)
        except Exception as e:
            return PrepareResponse(
                success=False,
                message="Failed to update property amenity",
                errors=str(e),
            ).send(status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            instance.delete()
            return PrepareResponse(
                success=True,
                message="Property amenity deleted successfully",
                data={},
            ).send(status.HTTP_200_OK)
        except Exception as e:
            return PrepareResponse(
                success=False,
                message="Failed to delete property amenity",
                errors=str(e),
            ).send(status.HTTP_400_BAD_REQUEST)
        
class PropertyImageUpdateDeleteView(generics.GenericAPIView):
    queryset = PropertyImage.objects.all()
    serializer_class = PropertyImageSerializer
    permission_classes = [IsHotelAndHotelOwnerPermission]

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()  # Fetch the PropertyImage instance using the URL `pk`
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        try:
            serializer.is_valid(raise_exception=True)
            updated_instance = serializer.save()
            return PrepareResponse(
                success=True,
                message="Property image updated successfully",
                data={
                    "id": updated_instance.id,
                    "property": updated_instance.property.id,
                    "image": updated_instance.image.url if updated_instance.image else None,
                },
            ).send(status.HTTP_200_OK)
        except Exception as e:
            return PrepareResponse(
                success=False,
                message="Failed to update property image",
                errors=str(e),
            ).send(status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object() 
        try:
            instance.delete()
            return PrepareResponse(
                success=True,
                message="Property image deleted successfully",
                data={},
            ).send(status.HTTP_200_OK)
        except Exception as e:
            return PrepareResponse(
                success=False,
                message="Failed to delete property image",
                errors=str(e),
            ).send(status.HTTP_400_BAD_REQUEST)
        
class CancellationPolicyUpdateDeleteView(APIView):
    """
    View for updating and deleting a cancellation policy.
    """
    permission_classes = [IsHotelAndHotelOwnerPermission]

    def get_object(self, pk):
        try:
            return CancellationPolicy.objects.get(pk=pk)
        except CancellationPolicy.DoesNotExist:
            return None

    def patch(self, request, pk, *args, **kwargs):
        """
        Partially update a cancellation policy.
        """
        policy = self.get_object(pk)
        if not policy:
            return PrepareResponse(
                success=False,
                message="Cancellation policy not found",
                errors={"id": "Invalid cancellation policy ID"}
            ).send(status.HTTP_404_NOT_FOUND)

        serializer = CancellationPolicySerializer(policy, data=request.data, partial=True)
        try:
            serializer.is_valid(raise_exception=True)
            updated_policy = serializer.save()
            return PrepareResponse(
                success=True,
                message="Cancellation policy updated successfully",
                data=serializer.data
            ).send(status.HTTP_200_OK)
        except Exception as e:
            return PrepareResponse(
                success=False,
                message="Failed to update cancellation policy",
                errors=str(e)
            ).send(status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        policy = self.get_object(pk)
        if not policy:
            return PrepareResponse(
                success=False,
                message="Cancellation policy not found",
                errors={"id": "Invalid cancellation policy ID"}
            ).send(status.HTTP_404_NOT_FOUND)

        try:
            policy.delete()
            return PrepareResponse(
                success=True,
                message="Cancellation policy deleted successfully",
                data={}
            ).send(status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return PrepareResponse(
                success=False,
                message="Failed to delete cancellation policy",
                errors=str(e)
            ).send(status.HTTP_400_BAD_REQUEST)
        
#########################Roomtype createSerializer###################################
class RoomImagesBulkCreateView(generics.CreateAPIView):
    serializer_class = BulkRoomImagesSerializer
    permission_classes = [IsHotelAndHotelOwnerPermission]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            room_images = serializer.save()
            return PrepareResponse(
                success=True,
                message="Room images uploaded successfully",
                data={
                    "uploaded_images": [
                        {"id": image.id, "room_type": image.room_type.id, "image_url": image.image.url}
                        for image in room_images
                    ]
                },
            ).send(201)
        except Exception as e:
            return PrepareResponse(
                success=False,
                message="Failed to upload room images",
                errors=str(e),
            ).send(400)
        
class RoomAmenitiesCreateView(generics.CreateAPIView):
    queryset = RoomAmenities.objects.all()
    serializer_class = RoomAmenitiesSerializer
    permission_classes = [IsHotelAndHotelOwnerPermission]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            room_amenities = serializer.save()
            return PrepareResponse(
                success=True,
                message="Room amenities created successfully",
                data=serializer.data,
            ).send(status.HTTP_201_CREATED)
        except Exception as e:
            return PrepareResponse(
                success=False,
                message="Failed to create room amenities",
                errors=str(e),
            ).send(status.HTTP_400_BAD_REQUEST)
        
class RoomTypeCreateView(generics.CreateAPIView):
    queryset = RoomType.objects.all()
    serializer_class = RoomTypeSerializer
    permission_classes = [IsHotelAndHotelOwnerPermission]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            room_type = serializer.save()
            return PrepareResponse(
                success=True,
                message="Room type created successfully",
                data=serializer.data,
            ).send(status.HTTP_201_CREATED)
        except Exception as e:
            return PrepareResponse(
                success=False,
                message="Failed to create room type",
                errors=str(e),
            ).send(status.HTTP_400_BAD_REQUEST)
        
class RoomBedCreateView(generics.CreateAPIView):
    queryset = RoomBed.objects.all()
    serializer_class = RoomBedSerializer
    permission_classes = [IsHotelAndHotelOwnerPermission]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            room_bed = serializer.save()
            return PrepareResponse(
                success=True,
                message="Room bed created successfully",
                data=serializer.data,
            ).send(status.HTTP_201_CREATED)
        except Exception as e:
            return PrepareResponse(
                success=False,
                message="Failed to create room bed",
                errors=str(e),
            ).send(status.HTTP_400_BAD_REQUEST)
        
class PriceCreateView(generics.CreateAPIView):
    queryset = Price.objects.all()
    serializer_class = PriceSerializer
    permission_classes = [IsHotelAndHotelOwnerPermission]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            price = serializer.save()
            return PrepareResponse(
                success=True,
                message="Price created successfully",
                data=serializer.data,
            ).send(status.HTTP_201_CREATED)
        except Exception as e:
            return PrepareResponse(
                success=False,
                message="Failed to create price",
                errors=str(e),
            ).send(status.HTTP_400_BAD_REQUEST)

###############Roomtype update##############################################
class RoomAmenitiesUpdateDeleteView(generics.GenericAPIView):
    queryset = RoomAmenities.objects.all()
    serializer_class = RoomAmenitiesSerializer
    permission_classes = [IsHotelAndHotelOwnerPermission]

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        try:
            serializer.is_valid(raise_exception=True)
            updated_instance = serializer.save()
            return PrepareResponse(
                success=True,
                message="Room amenities updated successfully",
                data=serializer.data,
            ).send(status.HTTP_200_OK)
        except Exception as e:
            return PrepareResponse(
                success=False,
                message="Failed to update room amenities",
                errors=str(e),
            ).send(status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            instance.delete()
            return PrepareResponse(
                success=True,
                message="Room amenities deleted successfully",
                data={},
            ).send(status.HTTP_200_OK)
        except Exception as e:
            return PrepareResponse(
                success=False,
                message="Failed to delete room amenities",
                errors=str(e),
            ).send(status.HTTP_400_BAD_REQUEST)
        

class RoomTypeUpdateDeleteView(generics.GenericAPIView):
    queryset = RoomType.objects.all()
    serializer_class = RoomTypeSerializer
    permission_classes = [IsHotelAndHotelOwnerPermission]

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        try:
            serializer.is_valid(raise_exception=True)
            updated_instance = serializer.save()
            return PrepareResponse(
                success=True,
                message="Room type updated successfully",
                data=serializer.data,
            ).send(status.HTTP_200_OK)
        except Exception as e:
            return PrepareResponse(
                success=False,
                message="Failed to update room type",
                errors=str(e),
            ).send(status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            instance.delete()
            return PrepareResponse(
                success=True,
                message="Room type deleted successfully",
                data={},
            ).send(status.HTTP_200_OK)
        except Exception as e:
            return PrepareResponse(
                success=False,
                message="Failed to delete room type",
                errors=str(e),
            ).send(status.HTTP_400_BAD_REQUEST)
        
class RoomImagesUpdateDeleteView(generics.GenericAPIView):
    queryset = RoomImages.objects.all()
    serializer_class = RoomImagesSerializer
    permission_classes = [IsHotelAndHotelOwnerPermission]

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        try:
            serializer.is_valid(raise_exception=True)
            updated_instance = serializer.save()
            return PrepareResponse(
                success=True,
                message="Room image updated successfully",
                data={
                    "id": updated_instance.id,
                    "room_type": updated_instance.room_type.id,
                    "image": updated_instance.image.url if updated_instance.image else None,
                },
            ).send(status.HTTP_200_OK)
        except Exception as e:
            return PrepareResponse(
                success=False,
                message="Failed to update room image",
                errors=str(e),
            ).send(status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            instance.delete()
            return PrepareResponse(
                success=True,
                message="Room image deleted successfully",
                data={},
            ).send(status.HTTP_200_OK)
        except Exception as e:
            return PrepareResponse(
                success=False,
                message="Failed to delete room image",
                errors=str(e),
            ).send(status.HTTP_400_BAD_REQUEST)
        
class RoomBedUpdateDeleteView(generics.GenericAPIView):
    queryset = RoomBed.objects.all()
    serializer_class = RoomBedSerializer
    permission_classes = [IsHotelAndHotelOwnerPermission]

    def patch(self, request, *args, **kwargs):
        """
        Handles partial updates for room beds.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        try:
            serializer.is_valid(raise_exception=True)
            updated_instance = serializer.save()
            return PrepareResponse(
                success=True,
                message="Room bed updated successfully",
                data=serializer.data,
            ).send(status.HTTP_200_OK)
        except Exception as e:
            return PrepareResponse(
                success=False,
                message="Failed to update room bed",
                errors=str(e),
            ).send(status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        """
        Handles deletion of room beds.
        """
        instance = self.get_object()
        try:
            instance.delete()
            return PrepareResponse(
                success=True,
                message="Room bed deleted successfully",
                data={},
            ).send(status.HTTP_200_OK)
        except Exception as e:
            return PrepareResponse(
                success=False,
                message="Failed to delete room bed",
                errors=str(e),
            ).send(status.HTTP_400_BAD_REQUEST)
        
class PriceUpdateDeleteView(generics.GenericAPIView):
    queryset = Price.objects.all()
    serializer_class = PriceSerializer
    permission_classes = [IsHotelAndHotelOwnerPermission]

    def patch(self, request, *args, **kwargs):
        """
        Handles partial updates for pricing.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        try:
            serializer.is_valid(raise_exception=True)
            updated_instance = serializer.save()
            return PrepareResponse(
                success=True,
                message="Price updated successfully",
                data=serializer.data,
            ).send(status.HTTP_200_OK)
        except Exception as e:
            return PrepareResponse(
                success=False,
                message="Failed to update price",
                errors=str(e),
            ).send(status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        """
        Handles deletion of pricing.
        """
        instance = self.get_object()
        try:
            instance.delete()
            return PrepareResponse(
                success=True,
                message="Price deleted successfully",
                data={},
            ).send(status.HTTP_200_OK)
        except Exception as e:
            return PrepareResponse(
                success=False,
                message="Failed to delete price",
                errors=str(e),
            ).send(status.HTTP_400_BAD_REQUEST)
        

#####################################Weekly offers###########################################

class WeeklyOfferCreateView(generics.CreateAPIView):
    queryset = WeeklyOffer.objects.all()
    serializer_class = WeeklyOfferSerializer
    permission_classes = [IsHotelAndHotelOwnerPermission]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            offer_instance = serializer.save()
            return PrepareResponse(
                success=True,
                message="Weekly offer created successfully",
                data=serializer.data,
            ).send(200)
        except Exception as e:
            return PrepareResponse(
                success=False,
                message="Failed to create weekly offer",
                errors=str(e),
            ).send(400)
        
class WeeklyOfferListView(generics.ListAPIView):
    queryset = WeeklyOffer.objects.all()
    serializer_class = WeeklyOfferSerializer
    permission_classes = [IsHotelAndHotelOwnerPermission]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return PrepareResponse(
            success=True,
            message="Weekly offers retrieved successfully",
            data=serializer.data,
        ).send(200)

############################Property Faq#############################################
class PropertyFAQCreateView(generics.GenericAPIView):
    serializer_class = PropertyFAQCreateSerializer
    permission_classes = [IsHotelAndHotelOwnerPermission]

    def post(self, request, *args, **kwargs):
        property_slug = self.kwargs.get('property_slug')

        try:
            property_instance = Property.objects.get(slug=property_slug)
        except Property.DoesNotExist:
            return PrepareResponse(success=False, message="Property not found").send(404)
        if request.user != property_instance.user.is_hotel_owner:
            return PrepareResponse(success=False, message="Only the property owner can add FAQs").send(403)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(property=property_instance, user=request.user)
            return PrepareResponse(success=True, data=serializer.data, message="Property FAQ added").send(201)

        return PrepareResponse(success=False, data=serializer.errors, message="Failed to add FAQ").send(400)



