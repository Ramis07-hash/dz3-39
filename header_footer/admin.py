from django.contrib import admin

from .models import Header, Footer, FooterText


@admin.register(Header)
class HeaderAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'followers', 'users', 'like')


@admin.register(FooterText)
class FooterTextAdmin(admin.ModelAdmin):
    list_display = ('id', 'title1', 'title2', 'title3', 'title4')


@admin.register(Footer)
class FooterAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'logo', 'footer_text')
