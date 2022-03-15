from django.db.models import Aggregate, FloatField


class Percentile(Aggregate):
    function = 'PERCENTILE_CONT'
    output_field = FloatField()
    template = '%(function)s(%(p)s) WITHIN GROUP (ORDER BY %(expressions)s)'

    def __init__(self, expression, **extra):
        super().__init__(expression,  **extra)
