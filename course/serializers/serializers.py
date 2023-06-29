from rest_framework import serializers
from course.models import Course, Lesson


class CourseSerializers(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = (
            'name',
            'preview',
            'description',
        )


class LessonSerializers(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"
