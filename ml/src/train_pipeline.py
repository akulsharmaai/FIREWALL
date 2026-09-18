import os
import sys
import json
import joblib
import pandas as pd
import numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import FeatureUnion
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, precision_recall_curve, auc, confusion_matrix, classification_report
)

def run_ml_pipeline():
    print("=== HUMAN FIREWALL ML ITERATIVE PIPELINE ===")
    
    # 1. Load Split Data
    train_df = pd.read_csv('data/FINAL_MASTER_DATASET_SPLIT.csv')
    
    df_train = train_df[train_df['split'] == 'train'].copy()
    df_val = train_df[train_df['split'] == 'val'].copy()
    df_test = train_df[train_df['split'] == 'test'].copy()
    
    print(f"Data Split Loaded: Train={len(df_train)}, Val={len(df_val)}, Test={len(df_test)}")
    
    X_train_raw = df_train['text'].fillna('').astype(str).tolist()
    y_train = df_train['manipulation_detected'].astype(int).values
    
    X_val_raw = df_val['text'].fillna('').astype(str).tolist()
    y_val = df_val['manipulation_detected'].astype(int).values
    
    X_test_raw = df_test['text'].fillna('').astype(str).tolist()
    y_test = df_test['manipulation_detected'].astype(int).values
    
    # Track Iterations
    iterations_report = []
    
    # ==========================================
    # ITERATION 1: Baseline TF-IDF (Word n-grams) + Logistic Regression
    # ==========================================
    print("\n[ITERATION 1] Word TF-IDF + Logistic Regression")
    vec_word_v1 = TfidfVectorizer(ngram_range=(1, 2), max_features=10000, lowercase=True)
    X_tr_v1 = vec_word_v1.fit_transform(X_train_raw)
    X_val_v1 = vec_word_v1.transform(X_val_raw)
    
    clf_v1 = LogisticRegression(C=1.0, max_iter=1000, random_state=42)
    clf_v1.fit(X_tr_v1, y_train)
    
    y_val_prob_v1 = clf_v1.predict_proba(X_val_v1)[:, 1]
    y_val_pred_v1 = (y_val_prob_v1 >= 0.5).astype(int)
    
    acc1 = accuracy_score(y_val, y_val_pred_v1)
    prec1 = precision_score(y_val, y_val_pred_v1)
    rec1 = recall_score(y_val, y_val_pred_v1)
    f1_1 = f1_score(y_val, y_val_pred_v1)
    roc1 = roc_auc_score(y_val, y_val_prob_v1)
    
    print(f"  Val Accuracy: {acc1:.4f} | Prec: {prec1:.4f} | Rec: {rec1:.4f} | F1: {f1_1:.4f} | ROC-AUC: {roc1:.4f}")
    iterations_report.append({
        'iteration': 1,
        'model': 'TF-IDF (Word 1-2) + LogisticRegression (default threshold 0.5)',
        'val_acc': acc1, 'val_prec': prec1, 'val_rec': rec1, 'val_f1': f1_1, 'val_roc': roc1
    })

    # ==========================================
    # ITERATION 2: Combined Word + Char N-Grams + LinearSVC / Logistic Regression
    # ==========================================
    print("\n[ITERATION 2] Word + Char N-Grams + Logistic Regression (C=2.0, class_weight='balanced')")
    feature_union = FeatureUnion([
        ('word', TfidfVectorizer(ngram_range=(1, 3), max_features=15000, sublinear_tf=True)),
        ('char', TfidfVectorizer(ngram_range=(2, 5), analyzer='char', max_features=25000, sublinear_tf=True))
    ])
    
    X_tr_v2 = feature_union.fit_transform(X_train_raw)
    X_val_v2 = feature_union.transform(X_val_raw)
    
    clf_v2 = LogisticRegression(C=2.0, max_iter=1000, class_weight='balanced', random_state=42)
    clf_v2.fit(X_tr_v2, y_train)
    
    y_val_prob_v2 = clf_v2.predict_proba(X_val_v2)[:, 1]
    y_val_pred_v2 = (y_val_prob_v2 >= 0.5).astype(int)
    
    acc2 = accuracy_score(y_val, y_val_pred_v2)
    prec2 = precision_score(y_val, y_val_pred_v2)
    rec2 = recall_score(y_val, y_val_pred_v2)
    f1_2 = f1_score(y_val, y_val_pred_v2)
    roc2 = roc_auc_score(y_val, y_val_prob_v2)
    
    print(f"  Val Accuracy: {acc2:.4f} | Prec: {prec2:.4f} | Rec: {rec2:.4f} | F1: {f1_2:.4f} | ROC-AUC: {roc2:.4f}")
    iterations_report.append({
        'iteration': 2,
        'model': 'Word+Char TF-IDF + LogisticRegression (balanced, C=2.0)',
        'val_acc': acc2, 'val_prec': prec2, 'val_rec': rec2, 'val_f1': f1_2, 'val_roc': roc2
    })

    # ==========================================
    # ITERATION 3: Threshold Tuning for High Precision (Low FP requirement for Human Firewall)
    # ==========================================
    print("\n[ITERATION 3] Threshold Optimization for Precision & Precision-Recall AUC")
    
    precisions, recalls, thresholds = precision_recall_curve(y_val, y_val_prob_v2)
    pr_auc = auc(recalls, precisions)
    
    # Search threshold that achieves highest F1 while maintaining precision >= 0.90
    best_thresh = 0.5
    best_f1_thresh = 0.0
    for t_val in np.arange(0.40, 0.85, 0.02):
        preds = (y_val_prob_v2 >= t_val).astype(int)
        p = precision_score(y_val, preds, zero_division=0)
        r = recall_score(y_val, preds, zero_division=0)
        f = f1_score(y_val, preds, zero_division=0)
        if f > best_f1_thresh and p >= 0.90:
            best_f1_thresh = f
            best_thresh = t_val
            
    if best_thresh == 0.5 and best_f1_thresh == 0.0:
        # Fallback to best overall F1 threshold
        best_thresh = 0.60
        
    y_val_pred_v3 = (y_val_prob_v2 >= best_thresh).astype(int)
    acc3 = accuracy_score(y_val, y_val_pred_v3)
    prec3 = precision_score(y_val, y_val_pred_v3)
    rec3 = recall_score(y_val, y_val_pred_v3)
    f1_3 = f1_score(y_val, y_val_pred_v3)
    
    print(f"  Selected Optimal Threshold: {best_thresh:.2f}")
    print(f"  Val Accuracy: {acc3:.4f} | Prec: {prec3:.4f} | Rec: {rec3:.4f} | F1: {f1_3:.4f} | PR-AUC: {pr_auc:.4f}")
    iterations_report.append({
        'iteration': 3,
        'model': f'Word+Char TF-IDF + LogisticReg (Threshold={best_thresh:.2f})',
        'val_acc': acc3, 'val_prec': prec3, 'val_rec': rec3, 'val_f1': f1_3, 'val_roc': roc2, 'pr_auc': pr_auc
    })

    # ==========================================
    # FINAL EVALUATION ON UNTOUCHED HELD-OUT TEST SET
    # ==========================================
    print("\n=== FINAL TEST EVALUATION (BINARY DETECTOR) ===")
    X_test_v2 = feature_union.transform(X_test_raw)
    y_test_prob = clf_v2.predict_proba(X_test_v2)[:, 1]
    y_test_pred = (y_test_prob >= best_thresh).astype(int)
    
    test_acc = accuracy_score(y_test, y_test_pred)
    test_prec = precision_score(y_test, y_test_pred)
    test_rec = recall_score(y_test, y_test_pred)
    test_f1 = f1_score(y_test, y_test_pred)
    test_roc = roc_auc_score(y_test, y_test_prob)
    
    p_test, r_test, _ = precision_recall_curve(y_test, y_test_prob)
    test_pr_auc = auc(r_test, p_test)
    
    cm = confusion_matrix(y_test, y_test_pred)
    tn, fp, fn, tp = cm.ravel()
    
    print(f"Test Accuracy  : {test_acc:.4f}")
    print(f"Test Precision : {test_prec:.4f}")
    print(f"Test Recall    : {test_rec:.4f}")
    print(f"Test F1-Score  : {test_f1:.4f}")
    print(f"Test ROC-AUC   : {test_roc:.4f}")
    print(f"Test PR-AUC    : {test_pr_auc:.4f}")
    print(f"Confusion Matrix:\n  TN: {tn}, FP: {fp}\n  FN: {fn}, TP: {tp}")

    # ==========================================
    # SECONDARY MODEL: Multi-class Manipulation Type Classifier (Positive Samples Only)
    # ==========================================
    print("\n=== SECONDARY MODEL: MANIPULATION TYPE CLASSIFIER ===")
    df_train_pos = df_train[df_train['manipulation_detected'] == 1].copy()
    df_val_pos = df_val[df_val['manipulation_detected'] == 1].copy()
    df_test_pos = df_test[df_test['manipulation_detected'] == 1].copy()
    
    X_tr_pos = df_train_pos['text'].fillna('').astype(str).tolist()
    y_tr_type = df_train_pos['manipulation_type'].tolist()
    
    X_val_pos = df_val_pos['text'].fillna('').astype(str).tolist()
    y_val_type = df_val_pos['manipulation_type'].tolist()
    
    X_te_pos = df_test_pos['text'].fillna('').astype(str).tolist()
    y_te_type = df_test_pos['manipulation_type'].tolist()
    
    sec_union = FeatureUnion([
        ('word', TfidfVectorizer(ngram_range=(1, 2), max_features=10000, sublinear_tf=True)),
        ('char', TfidfVectorizer(ngram_range=(3, 5), analyzer='char', max_features=15000, sublinear_tf=True))
    ])
    
    X_tr_sec = sec_union.fit_transform(X_tr_pos)
    X_te_sec = sec_union.transform(X_te_pos)
    
    clf_sec = LogisticRegression(C=3.0, max_iter=1000, class_weight='balanced', random_state=42)
    clf_sec.fit(X_tr_sec, y_tr_type)
    
    y_te_type_pred = clf_sec.predict(X_te_sec)
    
    sec_acc = accuracy_score(y_te_type, y_te_type_pred)
    sec_macro_f1 = f1_score(y_te_type, y_te_type_pred, average='macro', zero_division=0)
    sec_weighted_f1 = f1_score(y_te_type, y_te_type_pred, average='weighted', zero_division=0)
    
    print(f"Secondary Model Test Accuracy    : {sec_acc:.4f}")
    print(f"Secondary Model Macro F1-Score   : {sec_macro_f1:.4f}")
    print(f"Secondary Model Weighted F1-Score: {sec_weighted_f1:.4f}")
    
    sec_report = classification_report(y_te_type, y_te_type_pred, output_dict=True, zero_division=0)

    # Save Models and Artifacts
    os.makedirs('ml/models', exist_ok=True)
    joblib.dump(clf_v2, 'ml/models/binary_classifier.pkl')
    joblib.dump(feature_union, 'ml/models/binary_vectorizer.pkl')
    joblib.dump(clf_sec, 'ml/models/secondary_classifier.pkl')
    joblib.dump(sec_union, 'ml/models/secondary_vectorizer.pkl')
    
    config = {
        'threshold': float(best_thresh),
        'binary_accuracy': float(test_acc),
        'binary_precision': float(test_prec),
        'binary_recall': float(test_rec),
        'binary_f1': float(test_f1),
        'binary_roc_auc': float(test_roc),
        'binary_pr_auc': float(test_pr_auc),
        'secondary_accuracy': float(sec_acc),
        'secondary_macro_f1': float(sec_macro_f1),
        'secondary_weighted_f1': float(sec_weighted_f1)
    }
    
    with open('ml/models/config.json', 'w') as f:
        json.dump(config, f, indent=2)
        
    print("\nArtifacts successfully saved to ml/models/")

if __name__ == '__main__':
    run_ml_pipeline()
