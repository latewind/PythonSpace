from django.contrib import admin
from .models import Question, Choice


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date']})
    ]


# Register your models here.
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
