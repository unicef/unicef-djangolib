from django.urls import reverse


def admin_reverse(model, page="changelist"):
    return reverse(f"admin:{model._meta.app_label}_{model._meta.model_name}_{page}")
