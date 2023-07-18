from rest_framework.pagination import PageNumberPagination


class CoursePagination(PageNumberPagination):
    """Пагинатор страниц для модели Course"""
    page_size = 4  # Количество элементов на странице
    page_size_query_param = 'page_size'  # Параметр запроса для указания количества элементов на странице
    max_page_size = 100  # Максимальное количество элементов на странице


class LessonPagination(PageNumberPagination):
    """Пагинатор страниц для модели Lesson"""
    page_size = 2  # Количество элементов на странице
    page_size_query_param = 'page_size'  # Параметр запроса для указания количества элементов на странице
    max_page_size = 50  # Максимальное количество элементов на странице
