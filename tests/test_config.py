from nfcu_sentinel.utils.config import ConfigLoader


def test_load_merges_env_override() -> None:
    loader = ConfigLoader(root="config")
    config = loader.load("pipelines", env="dev")
    assert config["environment"] == "dev"
    assert "pipelines" in config
