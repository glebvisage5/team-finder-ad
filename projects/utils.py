from django.core.paginator import Paginator
from .constants import PROJECTS_PER_PAGE, USERS_PER_PAGE


def paginate(queryset, per_page, request):
    paginator = Paginator(queryset, per_page)
    page_number = request.GET.get("page")
    return paginator.get_page(page_number)
