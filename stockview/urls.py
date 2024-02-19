from django.urls import path
from .views import (
    index,
    StockListView,
    StockDetailView,
    RetrieveExternalStock
)
urlpatterns = [
    path('', index, name='index'),  # Map the root URL to views.index function
    path('api/stocks', StockListView.as_view(), name='stocks'), 
    path('api/retrieve-external-stocks', RetrieveExternalStock.as_view(), name='externalStocks'),  
    # Add more URL patterns as needed
]