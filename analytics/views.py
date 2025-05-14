from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import PropertyView, SearchQuery, Feedback
from .serializers import PropertyViewSerializer, SearchQuerySerializer, FeedbackSerializer

# PropertyView APIs
class PropertyViewListCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        views = PropertyView.objects.all().order_by('-viewed_at')
        serializer = PropertyViewSerializer(views, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data.copy()
        data['user'] = request.user.id
        serializer = PropertyViewSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# SearchQuery APIs
class SearchQueryListCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        queries = SearchQuery.objects.all().order_by('-timestamp')
        serializer = SearchQuerySerializer(queries, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data.copy()
        data['user'] = request.user.id
        serializer = SearchQuerySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Feedback APIs
class FeedbackListCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        feedbacks = Feedback.objects.all().order_by('-submitted_at')
        serializer = FeedbackSerializer(feedbacks, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data.copy()
        data['user'] = request.user.id
        serializer = FeedbackSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# from django.shortcuts import render, redirect
# from django.contrib.auth.decorators import login_required
# from .models import PropertyView, SearchQuery, Feedback
# from .forms import FeedbackForm
# from django.http import HttpResponse

# @login_required
# def property_view_list(request):
#     views = PropertyView.objects.filter(user=request.user)
#     return render(request, 'propertyview_list.html', {'views': views})

# @login_required
# def search_query_list(request):
#     queries = SearchQuery.objects.filter(user=request.user)
#     return render(request, 'searchquery_list.html', {'queries': queries})

# @login_required
# def feedback_create(request):
#     if request.method == 'POST':
#         form = FeedbackForm(request.POST)
#         if form.is_valid():
#             feedback = form.save(commit=False)
#             feedback.user = request.user
#             feedback.save()
#             return redirect('feedback_thankyou')
#     else:
#         form = FeedbackForm()
#     return render(request, 'feedback_form.html', {'form': form})



# #remove when connected to template
# @login_required
# def property_view_list(request):
#     views = PropertyView.objects.filter(user=request.user)
#     return HttpResponse(f"Property Views Count: {views.count()}")

# @login_required
# def search_query_list(request):
#     queries = SearchQuery.objects.filter(user=request.user)
#     return HttpResponse(f"Search Queries Count: {queries.count()}")

# @login_required
# def feedback_create(request):
#     if request.method == 'POST':
#         feedback_type = request.POST.get('feedback_type')
#         property_id = request.POST.get('property')
#         message = request.POST.get('message')

#         Feedback.objects.create(
#             user=request.user,
#             feedback_type=feedback_type,
#             property_id=property_id if property_id else None,
#             message=message
#         )
#         return HttpResponse("Feedback submitted successfully.")
#     return HttpResponse("Submit feedback using POST.")

