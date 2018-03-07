from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.serializers import ValidationError

from accounts.models import Profile, ProfileImage
from items.api.serializers import ItemSerializer

User = get_user_model()


class UserSerializer(serializers.HyperlinkedModelSerializer):
    profile = serializers.HyperlinkedRelatedField(view_name='api:profile-details', read_only=True)

    class Meta:
        model = User
        fields = ('username',
                  'email',
                  'password',
                  'last_login',
                  'profile',)
        read_only_fields = ('last_login',)
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']
        password = validated_data['password']
        user_obj = User(
            username = username,
            email = email
        )
        user_obj.set_password(password)
        user_obj.save()
        return user_obj


class UserSearchSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id',
                  'username',
                  'name',)

    def get_name(self, obj):
        return obj.profile.name


class UserLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField()

    class Meta:
        model = User
        fields = ('username', 'password',)
        extra_kwargs = {
            "password": {
                "write_only": True
            }
        }

    def validate(self, data):
        username = data.get('username')
        password = data['password']
        if not username:
            raise ValidationError('유저 아이디를 적어주세요.')
        user_qs = User.objects.filter(username=username)
        if user_qs.exists():
            user = user_qs.first()
            if not user.check_password(password):
                raise ValidationError('잘못된 비밀번호입니다. 다시 시도해주세요.')
            else:
                return data
        else:
            raise ValidationError('없는 유저 아이디입니다.')


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ('user',
                  'name',
                  'phone',
                  'address',
                  'status_msg',
                  'updated',)


class ProfileImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileImage
        fields = ('id',
                  'profile',
                  'image',
                  'created',
                  'updated',)
        read_only_fields = ('profile',)


class UserProfileImageSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer(read_only=True)
    profile_images = ProfileImageSerializer(many=True)

    class Meta:
        model = Profile
        fields = ('user', 'profile_images',)


class UserItemSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    items = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ('user', 'items',)

    def get_items(self, obj):
        return [item.id for item in obj.items_list]


class FollowerSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')
    following_users = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    followed_by_users = serializers.SerializerMethodField()
    followed_by_count = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ('username',
                  'following_users',
                  'following_count',
                  'followed_by_users',
                  'followed_by_count')

    def get_following_users(self, obj):
        return [user.username for user in obj.following_list]

    def get_following_count(self, obj):
        return obj.following_list.count()

    def get_followed_by_users(self, obj):
        return [profile.user.username for profile in obj.followed_by_list]

    def get_followed_by_count(self, obj):
        return obj.followed_by_list.count()


class AddFollowerSerializer(serializers.ModelSerializer):
    follow = serializers.CharField(source='following', label='Follow')

    class Meta:
        model = Profile
        fields = ('follow',)
        extra_kwargs = {
            'follow': {
                'write_only': True
            },
        }

    def validate(self, data):
        follow = data.get('following')
        user_qs = User.objects.filter(username=follow)
        if not user_qs.exists():
            raise ValidationError('없는 유저 아이디입니다.')
        return data
