from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(RawGitHubData)
admin.site.register(RawLinkedInData)
admin.site.register(RawManualData)
admin.site.register(RawResumeData)
admin.site.register(ProfileSectionRaw)