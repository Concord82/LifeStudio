import django_tables2 as tables
from django.utils.html import format_html
from .models import Clients



class PersonTable(tables.Table):
    last_name = tables.Column(verbose_name='Фамилия Имя Отчество')
    phone = tables.Column(verbose_name='Телефон')
    comment = tables.Column()
    def render_phone(self, record):
        return format_html("{}", record.get_phone_number())


    def render_last_name(self, record):
        return format_html('<a href="/work/clients/{}">{}</a>  ', record.id, record.get_full_name())

    def render_comment(self, value, record):
        print (record.id)
        if record.comment_preview() != record.comment:
            return format_html('<span id="text-tooltip" rel="tooltip" title="{}"> {} ... </span>', value, record.comment_preview())
        else:
            return format_html("{}", value)

    class Meta:
        attrs = {"class": "table table-striped"}
        model = Clients
        template_name = "django_tables2/bootstrap4.html"
        fields = ("last_name", "phone", "address", "comment" )