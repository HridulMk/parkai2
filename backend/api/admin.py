from django.contrib import admin
from .models import User, ParkingSpace, ParkingSlot, Reservation, Gate, CCTVFeed

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'phone', 'user_type', 'is_active']
    list_filter = ['user_type', 'is_active']
    actions = ['activate_users', 'deactivate_users']

    @admin.action(description='Activate selected users')
    def activate_users(self, request, queryset):
        queryset.update(is_active=True)

    @admin.action(description='Deactivate selected users')
    def deactivate_users(self, request, queryset):
        queryset.update(is_active=False)

@admin.register(ParkingSpace)
class ParkingSpaceAdmin(admin.ModelAdmin):
    list_display = ['name', 'vendor', 'total_slots', 'is_active']
    list_filter = ['is_active', 'vendor']
    actions = ['activate_spaces', 'deactivate_spaces']

    @admin.action(description='Activate selected parking spaces')
    def activate_spaces(self, request, queryset):
        queryset.update(is_active=True)

    @admin.action(description='Deactivate selected parking spaces')
    def deactivate_spaces(self, request, queryset):
        queryset.update(is_active=False)

@admin.register(ParkingSlot)
class ParkingSlotAdmin(admin.ModelAdmin):
    list_display = ['slot_id', 'label', 'space', 'is_occupied', 'is_active']
    list_filter = ['is_occupied', 'space', 'is_active']
    actions = ['activate_slots', 'deactivate_slots']

    @admin.action(description='Activate selected slots')
    def activate_slots(self, request, queryset):
        queryset.update(is_active=True)

    @admin.action(description='Deactivate selected slots')
    def deactivate_slots(self, request, queryset):
        queryset.update(is_active=False)

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ['reservation_id', 'user', 'slot', 'is_paid', 'amount']

@admin.register(Gate)
class GateAdmin(admin.ModelAdmin):
    list_display = ['name', 'space', 'is_active', 'access_count']

@admin.register(CCTVFeed)
class CCTVFeedAdmin(admin.ModelAdmin):
    list_display = ['name', 'space', 'camera_id', 'is_active']
