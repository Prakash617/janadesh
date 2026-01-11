from rest_framework import serializers
from organization.models import Organization, Leadership, MembershipRegistration, Policy, Donation

# ------------------------
# Organization Serializer
# ------------------------
class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = "__all__"


# ------------------------
# Leadership Serializer
# ------------------------
class LeadershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leadership
        fields = "__all__"


# ------------------------
# MembershipRegistration Serializer
# ------------------------
class MembershipRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for membership registration
    """
    user_details = serializers.SerializerMethodField(read_only=True)
    full_name = serializers.CharField(source='get_full_name', read_only=True)
    full_address = serializers.CharField(source='get_full_address', read_only=True)
    
    class Meta:
        model = MembershipRegistration
        fields = [
            'id',
            # 'user',
            'user_details',
            'membership_type',
            'first_name',
            'last_name',
            'full_name',
            'father_name',
            'date_of_birth',
            'gender',
            'phone_number',
            'email',
            'province',
            'district',
            'municipality',
            'ward_number',
            'village_settlement',
            'address',
            'full_address',
            'citizenship_number',
            'passport_photo',
            'citizenship_copy',
            'occupation',
            'motivation',
            'terms_accepted',
            'status',
            'approved_by',
            'approved_at',
            'rejection_reason',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'id',
            'status',
            'approved_by',
            'approved_at',
            'created_at',
            'updated_at',
        ]
    
    def get_user_details(self, obj):
        return {
            'id': obj.user.id,
            'username': obj.user.username,
            'email': obj.user.email,
        }
    
    def validate(self, attrs):
        if not attrs.get('terms_accepted'):
            raise serializers.ValidationError({
                "terms_accepted": "You must accept the terms and conditions."
            })
        return attrs
    
    def validate_passport_photo(self, value):
        if value.size > 2 * 1024 * 1024:  # 2MB
            raise serializers.ValidationError(
                "Passport photo size must not exceed 2MB."
            )
        
        # Validate file extension
        valid_extensions = ['.jpg', '.jpeg', '.png', '.gif']
        ext = value.name.lower().split('.')[-1]
        if f'.{ext}' not in valid_extensions:
            raise serializers.ValidationError(
                "Only JPG, PNG, and GIF files are allowed."
            )
        
        return value
    
    def validate_citizenship_copy(self, value):
        if value.size > 5 * 1024 * 1024:  # 5MB
            raise serializers.ValidationError(
                "Citizenship copy size must not exceed 5MB."
            )
        
        # Validate file extension
        valid_extensions = ['.pdf', '.jpg', '.jpeg', '.png']
        ext = value.name.lower().split('.')[-1]
        if f'.{ext}' not in valid_extensions:
            raise serializers.ValidationError(
                "Only PDF and image files are allowed."
            )
        
        return value


# ------------------------
# Policy Serializer
# ------------------------
class PolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = Policy
        fields = "__all__"


# ------------------------
# Donation Serializer
# ------------------------
class DonationSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source="user.get_full_name", read_only=True)

    class Meta:
        model = Donation
        fields = [
            "id",
            "user",
            "user_name",
            "donor_name",
            "donor_email",
            "donor_phone",
            "amount",
            "currency",
            "payment_method",
            "transaction_id",
            "status",
            "message",
            "is_anonymous",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]
