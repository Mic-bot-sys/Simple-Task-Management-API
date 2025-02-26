

from django.core.exceptions import ValidationError


def validate_task_data(data):
    if 'title' not in data or not isinstance(data['title'], str):
        raise ValidationError("Title is required and must be a string.")
    if 'status' not in data or data['status'] not in ['pending', 'in progress', 'completed']:
        raise ValidationError("Status is required and must be one of 'pending', 'in progress', or 'completed'.")
