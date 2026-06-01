from django.core.paginator import Paginator

PROJECTS_PER_PAGE = 12
USERS_PER_PAGE = 12


def paginate(queryset, per_page, request):
    paginator = Paginator(queryset, per_page)
    page_number = request.GET.get("page")
    return paginator.get_page(page_number)
