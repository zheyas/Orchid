from django.contrib import admin
from django.utils.html import format_html
from .models import Doctor


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = (
        'photo_preview',  # мини-превью
        'last_name',
        'first_name',
        'patronymic',
        'qualification',
        'experience_years',
        'email',
        'phone',
        'is_active',
        'detail_link',  # ссылка на детальную страницу
    )
    list_filter = ('qualification', 'is_active')
    search_fields = ('last_name', 'first_name', 'patronymic', 'qualification', 'email', 'phone')
    readonly_fields = ('created_at', 'updated_at', 'photo_preview')

    fieldsets = (
        (None, {
            'fields': (
                ('last_name', 'first_name', 'patronymic'),
                ('birth_date', 'photo', 'photo_preview'),
                ('qualification', 'experience_years'),
                ('education', 'place_of_work', 'position', 'specializations'),
                'email',
                'phone',
                'certificates',
                'bio',
                'achievements',
                'consultation_price',
                'is_active',
                'created_at',
                'updated_at',
            )
        }),
    )

    def photo_preview(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="width:50px; height:50px; object-fit:cover; border-radius:50%;" />',
                               obj.photo.url)
        return '-'

    photo_preview.short_description = 'Фото'

    def detail_link(self, obj):
        return format_html('<a href="/doctors/{}/" target="_blank">Просмотр</a>', obj.id)

    detail_link.short_description = 'Детали'
