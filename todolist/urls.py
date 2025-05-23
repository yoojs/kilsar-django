from todolist.views import TodosAPIView, TodoDetailAPIView, TodoItemsAPIView, TodoItemDetailAPIView
from django.urls import path

urlpatterns = [
    path("", TodosAPIView.as_view(), name="todo_list"),
    path("<int:id>/", TodoDetailAPIView.as_view(), name="todo"),
    path("<int:todo_list>/items/", TodoItemsAPIView.as_view(), name="todo_items"),
    path("<int:todo_list>/items/<int:id>/", TodoItemDetailAPIView.as_view(), name="todo_item"),
]