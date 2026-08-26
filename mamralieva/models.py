from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse


class BlogPost(models.Model):
    TYPE_INTERNAL = 'internal'
    TYPE_EXTERNAL = 'external'
    TYPE_CHOICES = [
        (TYPE_INTERNAL, 'Статья на сайте'),
        (TYPE_EXTERNAL, 'Внешняя ссылка'),
    ]

    post_type = models.CharField('Тип записи', max_length=10, choices=TYPE_CHOICES, default=TYPE_INTERNAL)

    title = models.CharField('Заголовок', max_length=250)
    slug = models.SlugField('Slug', unique=True, max_length=250, help_text='Латиница, для ссылки')
    cover_image = models.ImageField('Обложка', upload_to='blog/', blank=True, null=True)
    excerpt = models.TextField('Краткое описание', max_length=400, help_text='Показывается в списке и в превью для соцсетей')

    content = models.TextField('Текст статьи', blank=True, help_text='Только для типа "Статья на сайте"')
    external_url = models.URLField('Ссылка на источник', max_length=500, blank=True,
                                    help_text='Только для типа "Внешняя ссылка" — куда ведёт кнопка "Подробнее"')

    published_at = models.DateTimeField('Дата публикации')
    order = models.PositiveIntegerField('Порядок', default=0, help_text='Внутри одной даты — меньше значит выше')
    is_active = models.BooleanField('Опубликовано', default=True)

    class Meta:
        verbose_name = 'Статья блога'
        verbose_name_plural = 'Блог'
        ordering = ['-published_at', 'order']

    def __str__(self):
        return self.title

    def clean(self):
        if self.post_type == self.TYPE_EXTERNAL and not self.external_url:
            raise ValidationError({'external_url': 'Укажите ссылку для записи типа "Внешняя ссылка".'})
        if self.post_type == self.TYPE_INTERNAL and not self.content:
            raise ValidationError({'content': 'Укажите текст статьи для записи типа "Статья на сайте".'})

    def get_absolute_url(self):
        return reverse('mamralieva:blog_detail', args=[self.slug])

    def get_link_url(self):
        """Куда должна вести кнопка "Читать"/"Подробнее" в карточке."""
        if self.post_type == self.TYPE_EXTERNAL:
            return self.external_url
        return self.get_absolute_url()

    @property
    def is_external(self):
        return self.post_type == self.TYPE_EXTERNAL
