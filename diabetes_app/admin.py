from django.contrib import admin
# from .models import Prediction


admin.site.site_header = "Diabetes Predictor Admin"
admin.site.site_title = "Diabetes Predictor Portal"
admin.site.index_title = "Welcome to the Diabetes Predictor Administration"
# Register your models here.

# class PredictionAdmin(admin.ModelAdmin):
#     list_display = ('user', 'result', 'date_created')
#     list_filter = ('result', 'date_created')
#     search_fields = ('user__username', 'result')

# admin.site.register(Prediction, PredictionAdmin)
