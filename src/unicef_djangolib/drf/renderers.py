from rest_framework_csv.renderers import CSVRenderer


class FriendlyCSVRenderer(CSVRenderer):

    def flatten_item(self, item):
        if isinstance(item, bool):
            return {'': {True: 'Yes', False: ''}[item]}
        return super().flatten_item(item)
