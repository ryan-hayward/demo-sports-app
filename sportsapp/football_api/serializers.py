from rest_framework import serializers
from .models import Game, PlayerBio, Coach

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = "__all__"

class CoachSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coach
        fields = "__all__"

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayerBio
        fields = "__all__"