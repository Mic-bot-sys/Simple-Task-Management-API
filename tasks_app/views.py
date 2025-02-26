from django.http import JsonResponse
from django.views import View
import json
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
import random

from utils.custom_validations import validate_task_data

# This is how I implement the use of the In-memory data store
tasks = {}
task_id_counter = random.randint(11111, 99999)


@method_decorator(csrf_exempt, name='dispatch')
class TaskView(View):
    def post(self, request):
        global task_id_counter
        try:
            data = json.loads(request.body)
            validate_task_data(data)
            task = {
                'id': task_id_counter,
                'title': data['title'],
                'description': data.get('description', ''),
                'status': data['status'],
                'due_date': data.get('due_date', None)
            }
            tasks[task_id_counter] = task
            task_id_counter += 1
            return JsonResponse(task, status=201)
        except (json.JSONDecodeError, ValidationError) as e:
            return JsonResponse({'error': str(e)}, status=400)

    def get(self, request, id=None):
        if id is None:
            status_filter = request.GET.get('status')
            if status_filter:
                filtered_tasks = {k: v for k, v in tasks.items() if v['status'] == status_filter}
                return JsonResponse(list(filtered_tasks.values()), safe=False)
            return JsonResponse(list(tasks.values()), safe=False)

        if int(id) in tasks:
            return JsonResponse(tasks[int(id)])
        return JsonResponse({'error': 'Task not found.'}, status=404)

    def put(self, request, id):
        if int(id) not in tasks:
            return JsonResponse({'error': 'Task not found.'}, status=404)

        try:
            data = json.loads(request.body)
            validate_task_data(data)
            task = tasks[int(id)]
            task['title'] = data['title']
            task['description'] = data.get('description', task['description'])
            task['status'] = data['status']
            task['due_date'] = data.get('due_date', task['due_date'])
            return JsonResponse(task)
        except (json.JSONDecodeError, ValidationError) as e:
            return JsonResponse({'error': str(e)}, status=400)

    def delete(self, request, id):
        if int(id) not in tasks:
            return JsonResponse({'error': 'Task not found.'}, status=404)

        del tasks[int(id)]
        return JsonResponse({'message': 'Task deleted successfully.'}, status=204)