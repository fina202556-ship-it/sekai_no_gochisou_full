from django.contrib import admin
from django.utils.html import format_html
from .models import Food, CustomerOrder, Reservation


@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "image_preview",
        "category",
        "price",
        "description",
        "is_available",
        "created_at",
    )
    list_filter = ("category", "is_available")
    search_fields = ("name", "description")
    list_editable = ("price", "is_available")
    readonly_fields = ("image_preview", "created_at")
    fieldsets = (
        (None, {"fields": ("name", "description", "price", "category")}),
        ("Photo and availability", {"fields": ("image", "image_preview", "is_available")}),
        ("Registration", {"fields": ("created_at",)}),
    )

    @admin.display(description="Photo")
    def image_preview(self, obj):
        if obj and obj.image:
            return format_html(
                '<img src="{}" style="max-height: 80px; max-width: 120px;" />',
                obj.image.url,
            )
        return "No photo uploaded"


@admin.register(CustomerOrder)
class CustomerOrderAdmin(admin.ModelAdmin):
    list_display = ("id", "customer_name", "email", "total", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("customer_name", "email", "phone")
    list_editable = ("status",)


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ("customer_name", "reservation_date", "reservation_time", "guests", "phone")
    list_filter = ("reservation_date", "guests")
    search_fields = ("customer_name", "email", "phone")
