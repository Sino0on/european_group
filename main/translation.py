from modeltranslation.translator import register, TranslationOptions
from .models import (
    CompanyInfo, Statistic, Service, Testimonial,
    EmploymentCountry, CountryBenefit, JobListing,
    UniversityCountry, University,
    LanguageCourse, VisaType,
    TourDestination, TourDeal,
    LegalService, CompanyPackage, PackageFeature,
    HeroSlide,
)


@register(CompanyInfo)
class CompanyInfoTranslationOptions(TranslationOptions):
    fields = ('address', 'phone', 'email', 'work_hours', 'description')


@register(Statistic)
class StatisticTranslationOptions(TranslationOptions):
    fields = ('label',)


@register(Service)
class ServiceTranslationOptions(TranslationOptions):
    fields = ('title', 'subtitle', 'description')


@register(Testimonial)
class TestimonialTranslationOptions(TranslationOptions):
    fields = ('name', 'category', 'text')


@register(EmploymentCountry)
class EmploymentCountryTranslationOptions(TranslationOptions):
    fields = ('name', 'description')


@register(CountryBenefit)
class CountryBenefitTranslationOptions(TranslationOptions):
    fields = ('text',)


@register(JobListing)
class JobListingTranslationOptions(TranslationOptions):
    fields = ('role', 'salary')


@register(UniversityCountry)
class UniversityCountryTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(University)
class UniversityTranslationOptions(TranslationOptions):
    fields = ('name', 'location', 'description')


@register(LanguageCourse)
class LanguageCourseTranslationOptions(TranslationOptions):
    fields = ('name', 'category', 'description', 'duration', 'badge')


@register(VisaType)
class VisaTypeTranslationOptions(TranslationOptions):
    fields = ('name', 'countries', 'visa_subtypes', 'price_from', 'processing_time')


@register(TourDestination)
class TourDestinationTranslationOptions(TranslationOptions):
    fields = ('name', 'cities', 'badge', 'price_from')


@register(TourDeal)
class TourDealTranslationOptions(TranslationOptions):
    fields = ('hotel_name',)


@register(LegalService)
class LegalServiceTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


@register(CompanyPackage)
class CompanyPackageTranslationOptions(TranslationOptions):
    fields = ('name', 'badge')


@register(PackageFeature)
class PackageFeatureTranslationOptions(TranslationOptions):
    fields = ('text',)


@register(HeroSlide)
class HeroSlideTranslationOptions(TranslationOptions):
    fields = ('title', 'subtitle', 'description', 'button_primary_text', 'button_secondary_text')
