from rest_framework import serializers
from .models import Habit


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = '__all__'

    def validate_duration_seconds(self, value):
        if value > 120:
            raise serializers.ValidationError("Время выполнения не может превышать 120 секунд.")
        return value

    def validate_period_days(self, value):
        if value > 7:
            raise serializers.ValidationError("Периодичность не может быть больше 7 дней.")
        return value

    def validate(self, attrs):
        reward = attrs.get('reward')
        linked_habit = attrs.get('linked_habit')
        is_pleasant = attrs.get('is_pleasant')

        # Проверка связанной привычки и вознаграждения
        if reward and linked_habit:
            raise serializers.ValidationError("Нельзя указывать одновременно reward и linked_habit.")

        # Проверка приятной привычки
        if is_pleasant:
            if reward or linked_habit:
                raise serializers.ValidationError("Приятная привычка не может иметь reward или linked_habit.")

        # Проверка связанной привычки на is_pleasant
        if linked_habit and not linked_habit.is_pleasant:
            raise serializers.ValidationError("Связанная привычка должна быть приятной.")

        return attrs
