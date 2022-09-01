class FormControlMixin:
    """
    Adding form-control clss to all form fields
    ignore_fields: provides ignoring fields for adding form-control class
    """

    ignore_fields = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            if visible.name not in self.ignore_fields:
                if 'class' in visible.field.widget.attrs:
                    visible.field.widget.attrs['class'] += ' form-control'
                else:
                    visible.field.widget.attrs['class'] = 'form-control'

