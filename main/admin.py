from django.contrib import admin
from modeltranslation.admin import TranslationAdmin, TranslationTabularInline
from .models import (
    CompanyInfo, Statistic, Service, Testimonial,
    EmploymentCountry, CountryBenefit, JobListing,
    UniversityCountry, University,
    LanguageCourse, VisaType,
    TourDestination, TourDeal,
    LegalService, CompanyPackage, PackageFeature,
)


@admin.register(CompanyInfo)
class CompanyInfoAdmin(TranslationAdmin):
    fieldsets = (
        ('Основное', {'fields': ('address', 'phone', 'email', 'work_hours', 'description')}),
    )

    def has_add_permission(self, request):
        return not CompanyInfo.objects.exists()


@admin.register(Statistic)
class StatisticAdmin(TranslationAdmin):
    list_display = ('value', 'label', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_display_links = ('value',)


@admin.register(Service)
class ServiceAdmin(TranslationAdmin):
    list_display = ('title', 'subtitle', 'url', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_display_links = ('title',)


@admin.register(Testimonial)
class TestimonialAdmin(TranslationAdmin):
    list_display = ('name', 'category', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_display_links = ('name',)


class CountryBenefitInline(TranslationTabularInline):
    model = CountryBenefit
    extra = 1
    fields = ('text', 'order')


class JobListingInline(TranslationTabularInline):
    model = JobListing
    extra = 1
    fields = ('role', 'salary', 'order')


@admin.register(EmploymentCountry)
class EmploymentCountryAdmin(TranslationAdmin):
    list_display = ('flag_emoji', 'name', 'slug', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_display_links = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    inlines = [CountryBenefitInline, JobListingInline]


class UniversityInline(TranslationTabularInline):
    model = University
    extra = 1
    fields = ('name', 'slug', 'location', 'description', 'image', 'order', 'is_active')


@admin.register(UniversityCountry)
class UniversityCountryAdmin(TranslationAdmin):
    list_display = ('flag_emoji', 'name', 'slug', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_display_links = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    inlines = [UniversityInline]


@admin.register(University)
class UniversityAdmin(TranslationAdmin):
    list_display = ('name', 'country', 'location', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_display_links = ('name',)
    list_filter = ('country',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(LanguageCourse)
class LanguageCourseAdmin(TranslationAdmin):
    list_display = ('name', 'category', 'duration', 'badge', 'certificate', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_display_links = ('name',)


@admin.register(VisaType)
class VisaTypeAdmin(TranslationAdmin):
    list_display = ('name', 'countries', 'price_from', 'processing_time', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_display_links = ('name',)


class TourDealInline(admin.TabularInline):
    model = TourDeal
    extra = 1
    fields = ('hotel_name', 'discount_percent', 'price', 'original_price', 'nights', 'is_active')


@admin.register(TourDestination)
class TourDestinationAdmin(TranslationAdmin):
    list_display = ('name', 'cities', 'badge', 'price_from', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_display_links = ('name',)
    inlines = [TourDealInline]


@admin.register(TourDeal)
class TourDealAdmin(TranslationAdmin):
    list_display = ('hotel_name', 'destination', 'discount_percent', 'price', 'nights', 'is_active')
    list_editable = ('is_active',)
    list_display_links = ('hotel_name',)
    list_filter = ('destination',)


@admin.register(LegalService)
class LegalServiceAdmin(TranslationAdmin):
    list_display = ('title', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_display_links = ('title',)


class PackageFeatureInline(TranslationTabularInline):
    model = PackageFeature
    extra = 1
    fields = ('text', 'is_included', 'order')


@admin.register(CompanyPackage)
class CompanyPackageAdmin(TranslationAdmin):
    list_display = ('name', 'price', 'currency', 'badge', 'is_popular', 'order', 'is_active')
    list_editable = ('order', 'is_active', 'is_popular')
    list_display_links = ('name',)
    inlines = [PackageFeatureInline]
