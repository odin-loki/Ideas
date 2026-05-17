#!/usr/bin/env python3
"""
extract_function.py
═══════════════════

Phase 5 of the NN-based prime meta-pattern study.

For each trained MLP, distil the learned function into two
human-inspectable surrogate models, then quantify how faithfully
each surrogate reproduces the NN's decisions.

  (a) decision tree, max_depth=8, fit on the NN's *predicted
      probabilities* on the training set (NN-as-teacher);
  (b) sparse L1-regularised logistic regression
      (C = 0.1, scaled features), same teacher targets.

For every distillation we report:

  * agreement with NN on the held-out test set
  * test accuracy and test AUC of the distilled model
  * top features (by importance for the tree, by |coefficient|
    for the logistic) with their feature-group label
  * for the tree: the top decision splits as readable rules

Output files
  artifacts/distillation.json
  reports/nn_distillation.md
  artifacts/distilled_tree_s{scale}.pkl
  artifacts/distilled_logit_s{scale}.pkl
"""

from __future__ import annotations

import json
import pickle
from pathlib import Path
from typing import Dict, List

import numpy as np
import torch
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier, export_text

import sys
sys.path.insert(0, str(Path(__file__).parent))
from train_nn_classifiers import (PrimeMLP, FEATURE_GROUPS, D, HIDDEN, SCALES,
                                  SMALL_PRIMES_30, N_BIN_FEATURES)


ARTIFACT_DIR = Path("artifacts")


def feature_names() -> List[str]:
    names: List[str] = []
    for p in SMALL_PRIMES_30:
        names.append(f"res_{p}")
    for i in range(N_BIN_FEATURES):
        names.append(f"bit_{i}")
    names += ["log10_n", "log2_n", "digit_count"]
    names += ["mod6", "mod30", "mod210"]
    names += ["is_6k_pm1", "parity"]
    names += ["digital_root", "digit_sum_norm", "last_digit"]
    assert len(names) == D, f"{len(names)} != {D}"
    return names


def feature_group_of(idx: int) -> str:
    for g, idxs in FEATURE_GROUPS.items():
        if idx in idxs:
            return g
    return "?"


def distil_one_scale(scale: int) -> Dict:
    pt_path = ARTIFACT_DIR / f"model_s{scale}.pt"
    npz_path = ARTIFACT_DIR / f"data_s{scale}.npz"

    state = torch.load(pt_path, weights_only=False)
    model = PrimeMLP(in_dim=state["in_dim"], hidden=tuple(state["hidden"]))
    model.load_state_dict(state["state_dict"])
    model.eval()

    data = np.load(npz_path)
    X_tr, y_tr = data["X_train"], data["y_train"]
    X_te, y_te = data["X_test"],  data["y_test"]

    with torch.no_grad():
        p_tr_nn = torch.sigmoid(model(torch.tensor(X_tr))).numpy()
        p_te_nn = torch.sigmoid(model(torch.tensor(X_te))).numpy()
    yhat_tr_nn = (p_tr_nn > 0.5).astype(int)
    yhat_te_nn = (p_te_nn > 0.5).astype(int)
    nn_test_acc = float((yhat_te_nn == y_te.astype(int)).mean())
    nn_test_auc = float(roc_auc_score(y_te, p_te_nn))

    feats = feature_names()
    results: Dict = {"scale": scale,
                     "nn_test_acc": nn_test_acc,
                     "nn_test_auc": nn_test_auc}

    # ── (a) decision tree ────────────────────────────────────────────────
    tree = DecisionTreeClassifier(max_depth=8, min_samples_leaf=20,
                                   random_state=0)
    tree.fit(X_tr, yhat_tr_nn)
    yhat_te_tree = tree.predict(X_te)
    p_te_tree    = tree.predict_proba(X_te)[:, 1]
    tree_acc_vs_truth = float((yhat_te_tree == y_te.astype(int)).mean())
    tree_acc_vs_nn    = float((yhat_te_tree == yhat_te_nn).mean())
    tree_auc          = float(roc_auc_score(y_te, p_te_tree))

    importances = tree.feature_importances_
    top_idx = np.argsort(importances)[::-1][:15]
    top_features_tree = [
        {"feature": feats[i],
         "group": feature_group_of(int(i)),
         "importance": float(importances[i])}
        for i in top_idx if importances[i] > 0
    ]
    text_rules = export_text(tree, feature_names=feats, max_depth=4)

    pickle.dump(tree, open(ARTIFACT_DIR / f"distilled_tree_s{scale}.pkl", "wb"))

    results["tree"] = {
        "max_depth": int(tree.get_depth()),
        "n_leaves":  int(tree.get_n_leaves()),
        "test_acc_vs_truth": tree_acc_vs_truth,
        "test_acc_vs_nn":    tree_acc_vs_nn,
        "test_auc":          tree_auc,
        "top_features":      top_features_tree,
        "rules_text_top4":   text_rules,
    }

    # ── (b) sparse L1 logistic regression ────────────────────────────────
    scaler = StandardScaler().fit(X_tr)
    Xs_tr = scaler.transform(X_tr)
    Xs_te = scaler.transform(X_te)
    logit = LogisticRegression(penalty="l1", solver="saga",
                                C=0.1, max_iter=2000, random_state=0)
    logit.fit(Xs_tr, yhat_tr_nn)
    yhat_te_logit = logit.predict(Xs_te)
    p_te_logit    = logit.predict_proba(Xs_te)[:, 1]
    logit_acc_vs_truth = float((yhat_te_logit == y_te.astype(int)).mean())
    logit_acc_vs_nn    = float((yhat_te_logit == yhat_te_nn).mean())
    logit_auc          = float(roc_auc_score(y_te, p_te_logit))

    coefs = logit.coef_.ravel()
    nonzero_idx = np.where(np.abs(coefs) > 1e-6)[0]
    sorted_idx = nonzero_idx[np.argsort(-np.abs(coefs[nonzero_idx]))]
    top_features_logit = [
        {"feature": feats[i],
         "group": feature_group_of(int(i)),
         "coefficient": float(coefs[i])}
        for i in sorted_idx[:15]
    ]
    pickle.dump({"model": logit, "scaler": scaler},
                open(ARTIFACT_DIR / f"distilled_logit_s{scale}.pkl", "wb"))

    results["logit"] = {
        "C": 0.1,
        "n_nonzero_coefs": int(len(nonzero_idx)),
        "intercept": float(logit.intercept_[0]),
        "test_acc_vs_truth": logit_acc_vs_truth,
        "test_acc_vs_nn":    logit_acc_vs_nn,
        "test_auc":          logit_auc,
        "top_features":      top_features_logit,
    }

    return results


def render_markdown(per_scale: List[Dict]) -> str:
    lines: List[str] = []
    lines.append("# Knowledge distillation: NN → tree, NN → sparse logistic\n")
    lines.append("For each scale we trained a depth-8 decision tree and an "
                 "L1-regularised logistic regression to mimic the trained MLP, "
                 "using the NN's own predictions as the teacher target. "
                 "Tables below show how faithfully each surrogate reproduces "
                 "the NN, and which input features the surrogate ends up using.\n")

    lines.append("## Fidelity summary\n")
    lines.append("| scale | NN acc | NN AUC | tree → NN | tree AUC | "
                 "tree leaves | logit → NN | logit AUC | logit nz coefs |")
    lines.append("|------:|------:|------:|--------:|--------:|"
                 "------------:|---------:|--------:|--------------:|")
    for r in per_scale:
        lines.append(
            f"| {r['scale']} | {r['nn_test_acc']:.4f} | {r['nn_test_auc']:.4f} | "
            f"{r['tree']['test_acc_vs_nn']:.4f} | {r['tree']['test_auc']:.4f} | "
            f"{r['tree']['n_leaves']} | "
            f"{r['logit']['test_acc_vs_nn']:.4f} | {r['logit']['test_auc']:.4f} | "
            f"{r['logit']['n_nonzero_coefs']} |"
        )
    lines.append("")

    lines.append("## Decision-tree top features by scale\n")
    for r in per_scale:
        lines.append(f"### scale s = {r['scale']}\n")
        lines.append("| feature | group | importance |")
        lines.append("|:--------|:------|----------:|")
        for f in r["tree"]["top_features"][:10]:
            lines.append(f"| `{f['feature']}` | {f['group']} | {f['importance']:.4f} |")
        lines.append("")

    lines.append("## L1-logistic top features by scale\n")
    for r in per_scale:
        lines.append(f"### scale s = {r['scale']}\n")
        lines.append("| feature | group | coefficient |")
        lines.append("|:--------|:------|-----------:|")
        for f in r["logit"]["top_features"][:10]:
            lines.append(f"| `{f['feature']}` | {f['group']} | "
                         f"{f['coefficient']:+.4f} |")
        lines.append("")

    return "\n".join(lines)


if __name__ == "__main__":
    per_scale = []
    for s in SCALES:
        print(f"  distilling scale s={s}...")
        per_scale.append(distil_one_scale(s))

    out_json = ARTIFACT_DIR / "distillation.json"
    json.dump({"per_scale": per_scale, "scales": SCALES},
              open(out_json, "w"), indent=2)
    out_md = Path("reports") / "nn_distillation.md"
    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_md.write_text(render_markdown(per_scale), encoding="utf-8")

    print(f"\nWrote {out_json}")
    print(f"Wrote {out_md}")
    print(f"\nFidelity summary:")
    for r in per_scale:
        print(f"  s={r['scale']}  NN_acc={r['nn_test_acc']:.4f}  "
              f"tree→NN={r['tree']['test_acc_vs_nn']:.4f}  "
              f"logit→NN={r['logit']['test_acc_vs_nn']:.4f}  "
              f"logit_nz={r['logit']['n_nonzero_coefs']}")
