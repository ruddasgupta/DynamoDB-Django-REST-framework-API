from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status

from . import book_service as dynamodb
from rest_framework.decorators import api_view


@api_view(['GET'])
def create_table(request):
    try:
        dynamodb.create_table_book()
        return JsonResponse('Table Created', status=status.HTTP_201_CREATED, safe=False)
    except:
        return JsonResponse('Error while creating table', status=status.HTTP_500_INTERNAL_SERVER_ERROR, safe=False)


@api_view(['POST'])
def upvote_book(request, pk):
    response = dynamodb.upvote_a_book(pk)
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        return JsonResponse({'message': 'Upvotes the book successfully',
                             'Upvotes': response['Attributes']['upvotes']
                             })
    return JsonResponse({
        'message': 'Some error occured',
        'response': response
    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def book_list(request):
    if request.method == 'POST':
        book_data = JSONParser().parse(request)
        try:
            response = dynamodb.read_from_book(book_data['id'])
            if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                if 'Item' in response:
                    return JsonResponse({'message': 'The book does already exists'}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    book = dynamodb.write_to_book(book_data['id'], book_data['title'], book_data['description'],
                                                  book_data['author'],
                                                  book_data['publisher'], book_data['year'], book_data['isbn'])

                    if book['ResponseMetadata']['HTTPStatusCode'] == 200:
                        return JsonResponse({'message': 'Book Added'}, status=status.HTTP_201_CREATED)
        except:
            return JsonResponse({'message': 'Error while fetching item'},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR, )


@api_view(['GET', 'PUT', 'DELETE'])
def book_detail(request, pk):
    try:
        response = dynamodb.read_from_book(pk)
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            if 'Item' not in response:
                return JsonResponse({'message': 'The book does not exist'}, status=status.HTTP_404_NOT_FOUND)
    except:
        return JsonResponse({'message': 'Error while fetching item'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR, )

    if request.method == 'GET':
        return JsonResponse({'Item': response['Item']})

    elif request.method == 'PUT':
        book_data = JSONParser().parse(request)
        book = dynamodb.update_in_book(pk, book_data)
        if book['ResponseMetadata']['HTTPStatusCode'] == 200:
            return JsonResponse({'message': 'Updated successfully', 'ModifiedAttributes': book["Attributes"]},
                                status=status.HTTP_202_ACCEPTED)
        return JsonResponse({'message': 'Error while updating'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    elif request.method == 'DELETE':
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            return JsonResponse({'message': 'Book was deleted successfully!', 'Item': response['Item']},
                                status=status.HTTP_204_NO_CONTENT)
        return JsonResponse({'message': 'Error while deletion'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
