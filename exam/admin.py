from django.contrib import admin

from .models import Answer, ExamAttempt, Question, Subject


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "slug", "created_at")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("name",)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("id", "subject", "question_text", "correct_option", "created_at")
    list_filter = ("subject", "correct_option", "created_at")
    search_fields = (
        "subject__name",
        "question_text",
        "option_1",
        "option_2",
        "option_3",
        "option_4",
    )
    ordering = ("id",)


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 0
    readonly_fields = ("question", "selected_option", "is_correct", "created_at")
    can_delete = False


@admin.register(ExamAttempt)
class ExamAttemptAdmin(admin.ModelAdmin):
    list_display = ("id", "subject", "created_at")
    list_filter = ("subject", "created_at")
    ordering = ("-created_at",)
    inlines = [AnswerInline]
