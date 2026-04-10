import pytest
import os

@pytest.fixture
def env_prefix():
    return os.getenv("ENV_PREFIX")

@pytest.fixture
def base_url():
    return os.getenv("BASE_URL")