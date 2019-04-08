from demo.sample.forms import DemoForm


def test_auto_size_text_forms():
    form_data = {'name': 'test'}
    form = DemoForm(data=form_data)
    assert form.is_valid()
