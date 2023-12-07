
class TableFilterMixin:
    """
    Mixin for ListViews that want to add dynamica pagination, ordering and search filters.
    The mixin expects paginate_by, ordering and search_filter in the request.GET parameter.
    """
    paginate_by = None
    ordering = []
    search_filter = None

    def search_filter(self, queryset):
        """
        Override this funtion in the ListView to filter wanted fields for the model
        defined in the ListView
        """
        # Override funtion in List View to filter wanted model fields
        return queryset

    def set_paginate_by(self):
        """
        Set the self.paginate_by variable from the Pagination Class in the ListView
        """
        if self.request.GET.get('paginate_by'):
            self.paginate_by = self.request.GET.get('paginate_by')

    def set_ordering(self):
        """
        Sets a ordering list that can be intrepreted by the order_by() query method.
        """
        self.ordering = []
        if self.request.GET.get('ordering', []):
            self.ordering = [order for order in self.request.GET.get('ordering', []).split(',') if order]

    def get_search_filter_queryset(self, queryset):
        """
        If search_filter is in the request.GET parameters it will call search_filter and return
        a queryset object.
        """
        if self.request.GET.get('search_filter'):
            return self.search_filter(queryset)
        return queryset

    def get_queryset(self):
        queryset = super().get_queryset()

        self.set_paginate_by()

        self.set_ordering()

        queryset = self.get_search_filter_queryset(queryset)

        return queryset.order_by(*self.ordering)