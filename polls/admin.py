from django.contrib import admin
from polls.models import Poll, Choice

# Register your models here.
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

class PollAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Poll',  {'fields': ['question']}),
        ('Image', {'fields': ['image']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('question', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date', 'question']
    search_fields = ['question']

admin.site.register(Poll, PollAdmin)