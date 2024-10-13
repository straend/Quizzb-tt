from django.contrib import admin

from .models import Exam, Question, Choice, ExamScore

class ExamScoreInline(admin.TabularInline):
    model = ExamScore
    fields = ["user", "score"]
    readonly_fields = ["user", "score"]
    extra = 0
    can_delete = False
    show_change_link = False

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    model = Exam
    ordering = ['-pub_date']
    readonly_fields = ["name", "pub_date", "uuid"]
    date_hierarchy = "pub_date"
    list_display = ["name", "pub_date", "score_count"]
    #inlines = [ExamScoreInline]

@admin.register(ExamScore)
class ExamScoreAdmin(admin.ModelAdmin):
    model = ExamScore
    ordering = ['taken']
    list_filter = ["user", "exam", "guild_id"]
    list_display = ["user", "exam", "score", "taken"]
    readonly_fields = ["user", "exam", "score", "taken"]
    date_hierarchy = "taken"

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    model = Question
    list_filter = ["exam"]
    readonly_fields = ["exam", "order", "question_text", "correct"]

@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    model = Choice
    list_filter = ["question__exam"]
    readonly_fields = ["question", "choice_text"]
