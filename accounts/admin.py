from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
# Register your models here.
@admin.register(CustomUser)

class CustomUserAdmin(UserAdmin):
    list_display = [
        'email',
        # First column — clickable to open the user detail view
        'username',
        'full_name',
        'user_type',
        # Shows the stored value ('normal', 'owner' etc)
        # NOT the human-readable label — we fix this below
        # by using list_display with a custom method if needed
        'is_active',
        # Django admin shows BooleanFields as tick/cross icons
        'is_staff',
        'created_at',

    ]
    list_filter = [
        'user_type',
        # Creates a filter sidebar on the right with:
        # Normal User | Guest Owner | Verified Owner
        'is_active',
        'is_staff',
        'created_at',
        # DateTimeField filters show:
        # Any date | Today | Past 7 days | This month | This year
    ]

    search_fields = ['email', 'username', 'full_name', 'phone_number']
    # Powers the search bar at the top of the list view.
    # Django performs case-insensitive LIKE queries:
    # WHERE email ILIKE '%query%' OR username ILIKE '%query%'
    # Be careful adding too many fields here — each field
    # adds another LIKE condition which can slow down search
    # on large datasets. These four are reasonable for now.

    ordering = ['-created_at']
    # Overrides model Meta.ordering specifically for admin.
    # Newest users first in the list.

    # =========================================
    # DETAIL VIEW
    # Controls the edit page for an existing user
    # =========================================

    fieldsets = (
        # Format: ('Section Title', {'fields': (field_names,)})
        # Each tuple becomes a collapsible section in the form.
        # Sections display in the order listed here.

        ('Login Credentials', {
            'fields': ('email', 'username', 'password')
            # 'password' is special in UserAdmin — it displays
            # the stored hash as read-only text plus a link:
            # "Raw passwords are not stored. Change password."
            # Clicking the link opens a separate password
            # change form with proper hashing.
            # This is correct — never expose an editable
            # plain-text password field.
        }),

        ('Personal Information', {
            'fields': ('full_name', 'phone_number', 'profile_photo')
        }),

        ('Account Type & Verification', {
            'fields': ('user_type', 'guest_id')
            # guest_id is in readonly_fields below so it
            # displays but cannot be edited.
        }),

        ('Permissions', {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions',
                # groups and user_permissions come from PermissionsMixin
                # They show as multi-select widgets in admin
            ),
            'classes': ('collapse',),
            # 'collapse' makes this section collapsed by default.
            # Permissions are rarely changed — hiding them
            # reduces visual clutter for day-to-day admin work.
            # Click the section header to expand it.
        }),

        ('Important Dates', {
            'fields': ('last_login', 'created_at'),
            # Both are in readonly_fields — displayed but not editable
            # last_login: managed automatically by Django's auth system
            # created_at: auto_now_add, can never be changed
        }),
    )

    readonly_fields = ['created_at', 'last_login', 'guest_id']
    # readonly_fields renders these as plain text (not form inputs).
    # created_at: auto_now_add=True — Django ignores manual changes
    # last_login: managed by Django's auth machinery automatically
    # guest_id: editable=False on the model, should match here.
    #   Even though editable=False normally hides a field from
    #   admin, since we explicitly added it to fieldsets above
    #   we need readonly_fields to make it display-only.

    # =========================================
    # ADD VIEW
    # Controls the "Add User" creation form
    # =========================================

    add_fieldsets = (
        # Simpler than fieldsets — only what's needed for
        # creation. The detail fieldsets are for editing.
        ('Create New User', {
            'classes': ('wide',),
            # 'wide' is a built-in Django admin CSS class
            # that makes the form fields wider — better UX
            # for typing long emails and names.
            'fields': (
                'email',
                'username',
                'full_name',
                'user_type',
                'password1',
                # password1 and password2 are UserAdmin's
                # field names for the creation form.
                # UserAdmin renders these as a password
                # pair with confirmation and handles hashing.
                'password2',
            ),
        }),
    )