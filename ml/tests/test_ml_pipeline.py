import pytest
import os
import sys
import pandas as pd

# Add ml/src to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from predict import HumanFirewallPredictor, predict

def test_dataset_loading_and_split():
    split_file = 'data/FINAL_MASTER_DATASET_SPLIT.csv'
    assert os.path.exists(split_file), "FINAL_MASTER_DATASET_SPLIT.csv does not exist"
    df = pd.read_csv(split_file)
    assert 'split' in df.columns
    assert set(df['split'].unique()) == {'train', 'val', 'test'}
    assert len(df) == 8241

def test_model_loading():
    predictor = HumanFirewallPredictor(model_dir='ml/models')
    assert predictor.binary_clf is not None
    assert predictor.binary_vec is not None
    assert predictor.sec_clf is not None
    assert predictor.sec_vec is not None

def test_prediction_schema_and_types():
    res_pos = predict("Hurry! Only 2 items left in stock!")
    assert isinstance(res_pos, dict)
    assert "manipulation_detected" in res_pos
    assert "confidence" in res_pos
    assert "manipulation_type" in res_pos
    assert isinstance(res_pos["manipulation_detected"], bool)
    assert isinstance(res_pos["confidence"], float)
    assert res_pos["manipulation_detected"] is True
    assert res_pos["manipulation_type"] == "artificial_scarcity"

    res_neg = predict("This is a normal paragraph about privacy settings.")
    assert res_neg["manipulation_detected"] is False
    assert res_neg["manipulation_type"] == "none"

def test_edge_cases():
    # Empty string
    res_empty = predict("")
    assert res_empty["manipulation_detected"] is False
    assert res_empty["manipulation_type"] == "none"
    
    # Very short input
    res_short = predict("a")
    assert isinstance(res_short["manipulation_detected"], bool)
    
    # Very long text
    long_text = "Free sale! " * 500
    res_long = predict(long_text)
    assert isinstance(res_long["manipulation_detected"], bool)
    
    # Confirmshaming test
    res_shame = predict("No thanks, I don't want to save money")
    assert res_shame["manipulation_detected"] is True
    assert res_shame["manipulation_type"] == "deceptive_choice"

if __name__ == '__main__':
    pytest.main([__file__])
