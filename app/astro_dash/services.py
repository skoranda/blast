"""Service locator for AstroDash Django integration."""
from __future__ import annotations

from functools import lru_cache

from astro_dash.config.settings import get_settings, Settings
from astro_dash.domain.services.template_analysis_service import TemplateAnalysisService
from astro_dash.domain.services.line_list_service import LineListService
from astro_dash.domain.services.spectrum_processing_service import SpectrumProcessingService
from astro_dash.domain.services.classification_service import ClassificationService
from astro_dash.domain.services.spectrum_service import SpectrumService
from astro_dash.domain.services.model_service import ModelService
from astro_dash.domain.services.batch_processing_service import BatchProcessingService
from astro_dash.domain.services.redshift_service import RedshiftService
from astro_dash.infrastructure.storage.file_spectrum_repository import FileSpectrumRepository, OSCSpectrumRepository
from astro_dash.infrastructure.storage.model_storage import ModelStorage
from astro_dash.infrastructure.ml.templates import create_spectrum_template_handler
from astro_dash.infrastructure.django_repositories import DjangoSpectrumRepository, DjangoModelRepository
from astro_dash.infrastructure.ml.model_factory import ModelFactory


@lru_cache()
def get_config() -> Settings:
    return get_settings()


@lru_cache()
def get_template_analysis_service() -> TemplateAnalysisService:
    handler = create_spectrum_template_handler('dash')
    return TemplateAnalysisService(handler)


@lru_cache()
def get_line_list_service() -> LineListService:
    return LineListService()


@lru_cache()
def get_spectrum_processing_service() -> SpectrumProcessingService:
    return SpectrumProcessingService(get_config())


@lru_cache()
def get_file_repo() -> FileSpectrumRepository:
    return FileSpectrumRepository(get_config())


@lru_cache()
def get_osc_repo() -> OSCSpectrumRepository:
    return OSCSpectrumRepository(get_config())


@lru_cache()
def get_db_repo() -> DjangoSpectrumRepository:
    return DjangoSpectrumRepository()


@lru_cache()
def get_spectrum_service() -> SpectrumService:
    return SpectrumService(
        file_repo=get_file_repo(),
        osc_repo=get_osc_repo(),
        db_repo=get_db_repo(),
        settings=get_config(),
    )


@lru_cache()
def get_model_factory() -> ModelFactory:
    return ModelFactory(config=get_config())


@lru_cache()
def get_classification_service() -> ClassificationService:
    return ClassificationService(get_model_factory(), settings=get_config())


@lru_cache()
def get_model_storage() -> ModelStorage:
    return ModelStorage(get_config().user_model_dir)


@lru_cache()
def get_model_service() -> ModelService:
    return ModelService(DjangoModelRepository(), model_storage=get_model_storage())


@lru_cache()
def get_batch_processing_service() -> BatchProcessingService:
    return BatchProcessingService(
        spectrum_service=get_spectrum_service(),
        classification_service=get_classification_service(),
        processing_service=get_spectrum_processing_service(),
    )


@lru_cache()
def get_redshift_service() -> RedshiftService:
    return RedshiftService(get_config())
