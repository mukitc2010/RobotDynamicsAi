import pytest
from training import train_ppo, evaluate


def test_training_config_loading():
    cfg = train_ppo.load_config()
    assert "total_timesteps" in cfg


def test_evaluate_no_model(tmp_path):
    # evaluating without a real model should raise an error
    with pytest.raises(Exception):
        evaluate.evaluate("nonexistent.zip", episodes=1)
