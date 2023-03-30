from django.contrib import admin

# Register your models here.
from base.models import (
    Collectible,
    Reading,
    Baranggay,
    CustomUser,
    Notification,
    Transaction,
    PasswordResetRequest,
    Projection
)

admin.site.register(CustomUser)
admin.site.register(Collectible)
admin.site.register(Reading)
admin.site.register(Baranggay)
admin.site.register(Notification)
admin.site.register(Transaction)
admin.site.register(PasswordResetRequest)
admin.site.register(Projection)


