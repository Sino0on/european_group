from django.db import models


class CompanyInfo(models.Model):
    address = models.CharField('Адрес', max_length=500)
    phone = models.CharField('Телефон', max_length=100)
    email = models.EmailField('Email')
    work_hours = models.CharField('Часы работы', max_length=200)
    description = models.TextField('Описание компании', blank=True)

    class Meta:
        verbose_name = 'Контактная информация'
        verbose_name_plural = 'Контактная информация'

    def __str__(self):
        return 'Контактная информация'

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class Statistic(models.Model):
    value = models.CharField('Значение', max_length=50, help_text='Например: 98%, 500+, 12')
    label = models.CharField('Подпись', max_length=200)
    order = models.PositiveIntegerField('Порядок', default=0)
    is_active = models.BooleanField('Активен', default=True)

    class Meta:
        verbose_name = 'Статистика'
        verbose_name_plural = 'Статистика'
        ordering = ['order']

    def __str__(self):
        return f'{self.value} — {self.label}'


class Service(models.Model):
    title = models.CharField('Название', max_length=200)
    subtitle = models.CharField('Подзаголовок', max_length=200, help_text='Например: Литва, Польша, Германия...')
    description = models.TextField('Описание')
    icon_svg = models.TextField('SVG иконка', blank=True)
    url = models.CharField('Ссылка', max_length=200, blank=True)
    order = models.PositiveIntegerField('Порядок', default=0)
    is_active = models.BooleanField('Активен', default=True)

    class Meta:
        verbose_name = 'Направление / Услуга'
        verbose_name_plural = 'Направления / Услуги'
        ordering = ['order']

    def __str__(self):
        return self.title


class Testimonial(models.Model):
    name = models.CharField('Имя клиента', max_length=200, help_text='Например: Алина, 20 лет')
    category = models.CharField('Категория', max_length=200, help_text='Например: Студентка (Корея)')
    text = models.TextField('Текст отзыва')
    avatar_letter = models.CharField('Буква аватара', max_length=5, help_text='Первая буква имени')
    avatar_bg_color = models.CharField('Цвет фона аватара', max_length=100, default='bg-pink-100',
                                       help_text='Tailwind-класс фона, например: bg-pink-100')
    avatar_text_color = models.CharField('Цвет текста аватара', max_length=100, default='text-pink-500',
                                         help_text='Tailwind-класс цвета текста')
    order = models.PositiveIntegerField('Порядок', default=0)
    is_active = models.BooleanField('Активен', default=True)

    class Meta:
        verbose_name = 'Отзыв клиента'
        verbose_name_plural = 'Отзывы клиентов'
        ordering = ['order']

    def __str__(self):
        return self.name


class EmploymentCountry(models.Model):
    name = models.CharField('Название страны', max_length=200)
    slug = models.SlugField('Slug', unique=True, help_text='Латиница: lithuania, poland...')
    flag_emoji = models.CharField('Флаг (эмодзи)', max_length=10)
    description = models.TextField('Описание')
    order = models.PositiveIntegerField('Порядок', default=0)
    is_active = models.BooleanField('Активен', default=True)

    class Meta:
        verbose_name = 'Страна трудоустройства'
        verbose_name_plural = 'Страны трудоустройства'
        ordering = ['order']

    def __str__(self):
        return self.name


class CountryBenefit(models.Model):
    country = models.ForeignKey(EmploymentCountry, on_delete=models.CASCADE,
                                related_name='benefits', verbose_name='Страна')
    text = models.CharField('Преимущество', max_length=300)
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        verbose_name = 'Преимущество страны'
        verbose_name_plural = 'Преимущества стран'
        ordering = ['order']

    def __str__(self):
        return self.text


class JobListing(models.Model):
    country = models.ForeignKey(EmploymentCountry, on_delete=models.CASCADE,
                                related_name='jobs', verbose_name='Страна')
    role = models.CharField('Должность', max_length=200)
    salary = models.CharField('Зарплата', max_length=100)

    description = models.TextField('Описание вакансии', blank=True)
    requirements = models.TextField('Требования', blank=True, help_text='Каждое требование с новой строки')
    duties = models.TextField('Обязанности', blank=True, help_text='Каждая обязанность с новой строки')
    conditions = models.TextField('Условия работы', blank=True, help_text='Каждое условие с новой строки')
    image = models.ImageField('Фото / Иллюстрация', upload_to='jobs/', blank=True, null=True)

    order = models.PositiveIntegerField('Порядок', default=0)
    is_active = models.BooleanField('Активен', default=True)

    class Meta:
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'
        ordering = ['order']

    def __str__(self):
        return f'{self.role} ({self.country.name})'


class UniversityCountry(models.Model):
    name = models.CharField('Название страны', max_length=200)
    slug = models.SlugField('Slug', unique=True, help_text='Латиница: korea, usa...')
    flag_emoji = models.CharField('Флаг (эмодзи)', max_length=10)
    order = models.PositiveIntegerField('Порядок', default=0)
    is_active = models.BooleanField('Активна', default=True)

    class Meta:
        verbose_name = 'Страна (университеты)'
        verbose_name_plural = 'Страны (университеты)'
        ordering = ['order']

    def __str__(self):
        return self.name


class University(models.Model):
    country = models.ForeignKey(UniversityCountry, on_delete=models.CASCADE,
                                related_name='universities', verbose_name='Страна')
    name = models.CharField('Название', max_length=200)
    slug = models.SlugField('Slug', unique=True)
    location = models.CharField('Город', max_length=200)
    description = models.TextField('Описание')
    image = models.ImageField('Фото', upload_to='universities/', blank=True)
    order = models.PositiveIntegerField('Порядок', default=0)
    is_active = models.BooleanField('Активен', default=True)

    class Meta:
        verbose_name = 'Университет'
        verbose_name_plural = 'Университеты'
        ordering = ['order']

    def __str__(self):
        return self.name


class LanguageCourse(models.Model):
    name = models.CharField('Язык', max_length=200)
    category = models.CharField('Категория', max_length=200, help_text='Например: Иностранные языки')
    description = models.TextField('Описание курса')
    duration = models.CharField('Длительность', max_length=100, help_text='Например: 3-6 месяцев')
    certificate = models.BooleanField('Сертификат', default=True)
    badge = models.CharField('Бейдж', max_length=100, blank=True, help_text='Например: Top Choice, Popular')
    image = models.ImageField('Фото', upload_to='courses/', blank=True)
    order = models.PositiveIntegerField('Порядок', default=0)
    is_active = models.BooleanField('Активен', default=True)

    class Meta:
        verbose_name = 'Языковой курс'
        verbose_name_plural = 'Языковые курсы'
        ordering = ['order']

    def __str__(self):
        return self.name


class VisaType(models.Model):
    name = models.CharField('Название визы', max_length=200)
    countries = models.CharField('Страны', max_length=300, help_text='Например: 27 стран Шенгена')
    visa_subtypes = models.CharField('Типы визы', max_length=300, help_text='Например: Туризм / Бизнес / Гости')
    price_from = models.CharField('Цена от', max_length=100, help_text='Например: от €150')
    processing_time = models.CharField('Срок оформления', max_length=100, help_text='Например: ~15 дней')
    order = models.PositiveIntegerField('Порядок', default=0)
    is_active = models.BooleanField('Активен', default=True)

    class Meta:
        verbose_name = 'Тип визы'
        verbose_name_plural = 'Типы виз'
        ordering = ['order']

    def __str__(self):
        return self.name


class TourDestination(models.Model):
    name = models.CharField('Направление', max_length=200)
    cities = models.CharField('Города', max_length=300, help_text='Например: Пхукет, Паттайя, Самуи')
    badge = models.CharField('Бейдж', max_length=100, blank=True, help_text='Например: Хит продаж')
    price_from = models.CharField('Цена от', max_length=100, help_text='Например: от $850')
    image = models.ImageField('Фото', upload_to='tours/', blank=True)
    order = models.PositiveIntegerField('Порядок', default=0)
    is_active = models.BooleanField('Активен', default=True)

    class Meta:
        verbose_name = 'Туристическое направление'
        verbose_name_plural = 'Туристические направления'
        ordering = ['order']

    def __str__(self):
        return self.name


class TourDeal(models.Model):
    hotel_name = models.CharField('Название отеля', max_length=200)
    destination = models.ForeignKey(TourDestination, on_delete=models.CASCADE,
                                    related_name='deals', verbose_name='Направление')
    discount_percent = models.PositiveIntegerField('Скидка (%)')
    price = models.PositiveIntegerField('Цена со скидкой ($)')
    original_price = models.PositiveIntegerField('Оригинальная цена ($)')
    nights = models.PositiveIntegerField('Ночей')
    is_active = models.BooleanField('Активен', default=True)

    class Meta:
        verbose_name = 'Горящий тур'
        verbose_name_plural = 'Горящие туры'

    def __str__(self):
        return f'{self.hotel_name} — {self.destination.name}'


class LegalService(models.Model):
    title = models.CharField('Название', max_length=200)
    description = models.TextField('Описание')
    icon_svg = models.TextField('SVG иконка', blank=True)
    order = models.PositiveIntegerField('Порядок', default=0)
    is_active = models.BooleanField('Активен', default=True)

    class Meta:
        verbose_name = 'Юридическая услуга'
        verbose_name_plural = 'Юридические услуги'
        ordering = ['order']

    def __str__(self):
        return self.title


class CompanyPackage(models.Model):
    name = models.CharField('Название пакета', max_length=200)
    badge = models.CharField('Бейдж', max_length=100, blank=True, help_text='Например: Популярный')
    price = models.PositiveIntegerField('Цена')
    currency = models.CharField('Валюта', max_length=10, default='с')
    is_popular = models.BooleanField('Выделить как популярный', default=False)
    order = models.PositiveIntegerField('Порядок', default=0)
    is_active = models.BooleanField('Активен', default=True)

    class Meta:
        verbose_name = 'Пакет регистрации компании'
        verbose_name_plural = 'Пакеты регистрации компании'
        ordering = ['order']

    def __str__(self):
        return self.name


class PackageFeature(models.Model):
    package = models.ForeignKey(CompanyPackage, on_delete=models.CASCADE,
                                related_name='features', verbose_name='Пакет')
    text = models.CharField('Описание опции', max_length=300)
    is_included = models.BooleanField('Включено', default=True)
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        verbose_name = 'Опция пакета'
        verbose_name_plural = 'Опции пакета'
        ordering = ['order']

    def __str__(self):
        return self.text


class Partner(models.Model):
    name = models.CharField('Название партнёра', max_length=200)
    logo = models.ImageField('Логотип', upload_to='partners/')
    website = models.URLField('Сайт партнёра', blank=True)
    order = models.PositiveIntegerField('Порядок', default=0)
    is_active = models.BooleanField('Активен', default=True)

    class Meta:
        verbose_name = 'Партнёр'
        verbose_name_plural = 'Партнёры'
        ordering = ['order']

    def __str__(self):
        return self.name


class HeroSlide(models.Model):
    title = models.CharField('Заголовок', max_length=250)
    subtitle = models.CharField('Подзаголовок', max_length=250, blank=True)
    description = models.TextField('Описание', blank=True)

    button_primary_text = models.CharField('Текст основной кнопки', max_length=100, blank=True)
    button_primary_url = models.CharField('Ссылка основной кнопки', max_length=250, default='#finder', blank=True)

    button_secondary_text = models.CharField('Текст дополнительной кнопки', max_length=100, blank=True)
    button_secondary_url = models.CharField('Ссылка дополнительной кнопки', max_length=250, default='#directions', blank=True)

    background_image = models.ImageField(
        'Фоновое изображение',
        upload_to='hero/',
        blank=True,
        null=True,
        help_text='Если не задано, будет использован стандартный темно-синий фон с абстрактным градиентом'
    )

    order = models.PositiveIntegerField('Порядок', default=0)
    is_active = models.BooleanField('Активен', default=True)

    class Meta:
        verbose_name = 'Слайд главного экрана'
        verbose_name_plural = 'Слайды главного экрана'
        ordering = ['order']

    def __str__(self):
        return self.title
