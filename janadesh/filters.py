from rest_framework.filters import BaseFilterBackend

class LimitFilter(BaseFilterBackend):
    """
    Adds global ?limit=N support to all ViewSets.
    """
    def filter_queryset(self, request, queryset, view):
        limit = request.query_params.get("limit")
        if limit is not None:
            try:
                limit = int(limit)
                return queryset[:limit]
            except ValueError:
                return queryset
        return queryset
