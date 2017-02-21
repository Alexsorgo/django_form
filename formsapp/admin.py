from django.contrib import admin
from models import proj, req, res


class ProjectModelAdmin(admin.ModelAdmin):
    class Meta:
        model = proj
    list_display = ["project", "created"]
    list_filter = ["created"]
    search_fields = ["project"]


class RequestModelAdmin(admin.ModelAdmin):
    class Meta:
        model = req
    list_display = ["tag", "created"]
    list_filter = ["created"]
    search_fields = ["tag"]


class ResponseModelAdmin(admin.ModelAdmin):
    class Meta:
        model = res
    list_display = ["tag", "created"]
    list_filter = ["created"]
    search_fields = ["tag"]


admin.site.register(proj, ProjectModelAdmin)
admin.site.register(req, RequestModelAdmin)
admin.site.register(res, ResponseModelAdmin)
