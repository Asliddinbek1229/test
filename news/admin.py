    from django.contrib import admin

from .models import Category, News, ContactUs, Comment


# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = [
        'category',
        'title',
        'slug',
        'publish_time',
        'status'
    ]
    list_filter = ['status', 'publish_time', 'created_time']
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ['title', 'publish_time', 'status']
    date_hierarchy = 'publish_time'
    ordering = ['status', 'publish_time']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'body', 'created_time', 'active']
    list_filter = ['created_time', 'active']
    search_fields = ['user', 'body']
    actions = ['disable_comment', 'activate_comment']

    def disable_comment(self, request, queryset):
        queryset.update(active=False)

    def activate_comment(self, request, queryset):
        queryset.update(active=True)


admin.site.register(ContactUs)