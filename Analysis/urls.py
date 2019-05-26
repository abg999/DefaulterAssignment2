from django.urls import path
from .views import Scatter, GetAttributes, BarPlot, PieChart, WordCloudAPI, BoxPlot

urlpatterns = [
    path('attributes/', GetAttributes.as_view(), name='get_attributes'),
    path('scatter/', Scatter.as_view(), name='scatter'),
    path('bar/', BarPlot.as_view(), name='bar_plot'),
    path('pie/', PieChart.as_view(), name='pie_chart'),
    path('wordcloud/', WordCloudAPI.as_view(), name='wordcloud'),
    path('boxplot/', BoxPlot.as_view(), name='boxplot'),
]