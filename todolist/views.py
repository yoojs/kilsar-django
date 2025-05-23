from todolist.models import Todo, TodoItem
from django.db.models import Max, F
from rest_framework import permissions, filters
from todolist.serializers import TodoSerializer, TodoItemSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from todolist.tasks import send_mail_task
from todolist.permissions import IsOwnerOrReadOnly
class TodosAPIView(ListCreateAPIView):
    serializer_class = TodoSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    filterset_fields = ['id', 'title', 'desc', ]
    search_fields = ['id', 'title', 'desc']
    ordering_fields = ['id', 'title', 'desc']

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

    def get_queryset(self):
        print(Todo.objects.all())
        return Todo.objects.filter(owner=self.request.user)


class TodoDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = TodoSerializer
    permission_classes = (IsAuthenticated,IsOwnerOrReadOnly)
    lookup_field = "id"

    def get_queryset(self):
        return Todo.objects.filter(owner=self.request.user)
    
class TodoItemsAPIView(ListCreateAPIView):
    serializer_class = TodoItemSerializer
    permission_classes = (IsAuthenticated,IsOwnerOrReadOnly)
    lookup_field = "todo_list"
    filterset_fields = ['id', 'desc', 'is_complete', 'order',]
    search_fields = ['id', 'desc', 'is_complete', 'order',]
    ordering_fields = ['order']

    def perform_create(self, serializer):
        latest_order = TodoItem.objects.filter(
            todo_list = self.kwargs['todo_list']
        ).aggregate(
            Max('order')
        )['order__max']
        order = 1 if latest_order is None else latest_order + 1
        self.is_complete = False
        return serializer.save(owner=self.request.user, order=order, is_complete=False)

    def get_queryset(self):
        return TodoItem.objects.filter(owner=self.request.user, todo_list=self.kwargs['todo_list'])


class TodoItemDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = TodoItemSerializer
    permission_classes = (IsAuthenticated,IsOwnerOrReadOnly)
    lookup_field = "id"

    def perform_update(self, serializer):
        instance = self.get_object()
        new_order = serializer.validated_data.get('order')
        is_complete = serializer.validated_data.get('is_complete')
        
        if new_order and instance.order != new_order:
            # Get all items from the same todo_list
            items = TodoItem.objects.filter(todo_list=instance.todo_list)
            
            if new_order > instance.order:
                # Moving item to a higher position
                # Decrease order of items between old and new position
                items.filter(
                    order__gt=instance.order,
                    order__lte=new_order
                ).update(order=F('order') - 1)
            else:
                # Moving item to a lower position
                # Increase order of items between new and old position
                items.filter(
                    order__gte=new_order,
                    order__lt=instance.order
                ).update(order=F('order') + 1)
        if is_complete is None:
            is_complete = instance.is_complete
        saved = serializer.save()
        
        if is_complete and instance.is_complete != is_complete:
            # Update the is_complete field
            # email user subject, message, email_from, recepient_list
            subject = "Todo item completed"
            message = f"Your todo item '{instance.desc}' in \nTo Do List: '{instance.todo_list.title}' has been marked as complete."
            recepient_list = [instance.owner.email]
            send_mail_task.delay_on_commit(subject, message, recepient_list)
        return saved        

    def perform_destroy(self, instance):
        # Update orders after deletion
        TodoItem.objects.filter(
            todo_list=instance.todo_list,
            order__gt=instance.order
        ).update(order=F('order') - 1)
        instance.delete()
        return instance

    def get_queryset(self):
        return TodoItem.objects.filter(
            owner=self.request.user,
            todo_list=self.kwargs['todo_list']
        ).order_by('order')