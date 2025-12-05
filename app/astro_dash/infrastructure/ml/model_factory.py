from typing import Optional
from astro_dash.infrastructure.ml.classifiers.base import BaseClassifier
from astro_dash.infrastructure.ml.classifiers.dash_classifier import DashClassifier
from astro_dash.infrastructure.ml.classifiers.transformer_classifier import TransformerClassifier
from astro_dash.infrastructure.ml.classifiers.user_classifier import UserClassifier
from astro_dash.core.exceptions import ModelConfigurationException
from astro_dash.infrastructure.storage.model_storage import ModelStorage

class ModelFactory:
    """
    Factory for creating classifier instances based on model type and user model ID.
    """
    def __init__(self, config=None):
        self.config = config

    def get_classifier(
        self,
        model_type: str,
        user_model_id: Optional[str] = None
    ) -> BaseClassifier:
        if user_model_id:
            # Create a ModelStorage instance using configured user_model_dir
            base_dir = getattr(self.config, 'user_model_dir', '/mnt/astrodash-data/user_models') if self.config else '/mnt/astrodash-data/user_models'
            model_storage = ModelStorage(base_dir)
            return UserClassifier(user_model_id, model_storage, self.config)
        if model_type == "dash":
            return DashClassifier(self.config)
        elif model_type == "transformer":
            return TransformerClassifier(self.config)
        else:
            raise ModelConfigurationException(f"Unknown model type: {model_type}")
