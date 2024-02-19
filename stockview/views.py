from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import Stock
from .serializers import StockSerializer
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings

import requests
import json

class StockListView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    # 1. List all
    def get(self, request, *args, **kwargs):
        '''
        List all the stock items for given requested user
        '''
        stock = Stock.objects.filter(user = request.user.id)
        serializer = StockSerializer(stock, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 2. Create
    def post(self, request, *args, **kwargs):
        '''
        Create the Stock with given stock data
        '''
        data = {
            'name': request.data.get('name'), 
            'price': request.data.get('price'), 
            'user': request.user.id
        }
        serializer = StockSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class StockDetailView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, stock_name, user_id):
        '''
        Helper method to get the object with given stock name and user_id
        '''
        try:
            return Stock.objects.get(name=stock_name, user = user_id)
        except Stock.DoesNotExist:
            return None

    # 3. Retrieve
    def get(self, request, stock_name, *args, **kwargs):
        '''
        Retrieves the Stock with given stock_name
        '''
        stock_instance = self.get_object(stock_name, request.user.id)
        if not stock_instance:
            return Response(
                {"res": "Object with stock name does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = StockSerializer(stock_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 4. Update
    def put(self, request, stock_name, *args, **kwargs):
        '''
        Updates the stock item with given stock_name if exists
        '''
        stock_instance = self.get_object(stock_name, request.user.id)
        if not stock_instance:
            return Response(
                {"res": "Object with stock name does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {
            'name': request.data.get('name'), 
            'price': request.data.get('price'), 
            'user': request.user.id
        }
        serializer = StockSerializer(instance = stock_instance, data=data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 5. Delete
    def delete(self, request, stock_name, *args, **kwargs):
        '''
        Deletes the stock item with given stock_name if exists
        '''
        stock_instance = self.get_object(stock_name, request.user.id)
        if not stock_instance:
            return Response(
                {"res": "Object with stock name does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        stock_instance.delete()
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )
    
    
class RetrieveExternalStock(APIView):
    """ This view make and external api call, save the result and return 
        the data generated as json object """
    # Only authenticated user can make request on this view
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, format=None):
        # The url is like https://localhost:8000/api/?results=40
        symbol = self.request.query_params.get('name')
        response = {}
        if not symbol:
            response['status'] = 400
            response['message'] = 'no stock name provided'
            response['credentials'] = {}
            return Response(response)
        url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=' + str(symbol) + '&interval=5min&apikey=' + str(settings.ALPHAVANTAGE_API_KEY)
        # Make an external api request ( use auth if authentication is required for the external API)
        r = requests.get(url)
        r_status = r.status_code
        # If it is a success
        if r_status == 200:
            try:
                data = r.json()
                response['status'] = 200
                response['message'] = 'success'
                response['stock_data'] = data
                return Response(response)

            except:
                response['status'] = 502
                response['message'] = 'Server has encountered an error retrieving data'
                response['stock_data'] = data
                return Response(response)
            # # Loop through the credentials and save them
            # # But it is good to avoid that each user request create new 
            # # credentials on top of the existing one
            # # ( you can retrieve and delete the old one and save the news credentials )
            # for c in data:
            #     credential = Credential(user = self.request.user, value=c)
            #     credential.save()
        else:
            response['status'] = r.status_code
            response['message'] = 'error'
            response['credentials'] = {}
            return Response(response)

    



def index(request):
    return HttpResponse("Hello, world! This is the index page.")

def about(request):
    return HttpResponse("This is the about page.")