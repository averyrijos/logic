"""
Applied TIL (Transcendental Induction Logic) — Minimal Working Simulation
-----------------------------------------------------------------------
This script simulates an evolving logic L under conditions C using the
TIL loop:
  - Detect anomalies (Scar-Induction 𝓘_S)
  - Detect stabilizing patterns (Bloom-Induction 𝓘_B)
  - Update logic via a policy Upd_Π
  - Enforce adoption gates: COH, ADEQ, SAFE, GEN
It prints a step-by-step trace and plots the Ontopolitical Generativity
Index (OGI) over time, annotating Scar/Bloom events.

Run:
  python til_sim.py

Dependencies:
  - matplotlib (for the OGI chart)

Feel free to extend the placeholders with your domain semantics.
"""
from __future__ import annotations

import math
import random
from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional

# ------------------------------
# Configuration / Random seed
# ------------------------------
SEED = 42
random.seed(SEED)

# ------------------------------
# Data structures
# ------------------------------
@dataclass
class Rule:
    name: str
    weight: float = 1.0  # influence in OGI computations
    risk: float = 0.0    # safety risk contribution

@dataclass
class LogicState:
    version: int
    rules: Dict[str, Rule] = field(default_factory=dict)
    coverage: float = 0.20  # how much of the target phenomenon L can capture [0,1]
    stability: float = 0.60 # internal stability [0,1]; affected by rule churn
    novelty: float = 0.10   # exploratory capacity [0,1]

    def clone(self) -> 'LogicState':
        return LogicState(
            version=self.version,
            rules={k: Rule(r.name, r.weight, r.risk) for k, r in self.rules.items()},
            coverage=self.coverage,
            stability=self.stability,
            novelty=self.novelty,
        )

@dataclass
class Conditions:
    # Conditions-of-possibility C (constraints/KPIs)
    min_coverage: float = 0.30
    max_risk: float = 0.35
    min_stability: float = 0.40

@dataclass
class SAT:  # Structured Anomaly Token
    kind: str     # e.g., 'undercapture', 'contradiction', 'fragility'
    severity: float  # [0,1]

@dataclass
class Bloom:
    pattern: str
    strength: float  # [0,1]

@dataclass
class StepLog:
    step: int
    event: str  # 'scar' or 'bloom' or 'none'
    sat: Optional[SAT]
    bloom: Optional[Bloom]
    ogi: float
    gates_passed: Tuple[bool, bool, bool, bool]  # (COH, ADEQ, SAFE, GEN)
    comment: str = ""

# ------------------------------
# OGI (Ontopolitical Generativity Index)
# ------------------------------

def compute_ogi(L: LogicState) -> float:
    """Simple composite metric in [0,1] (clipped).
    Increase with coverage & novelty; decrease with excess risk; reward stability.
    Risk is summed from rules.
    """
    risk = sum(r.risk for r in L.rules.values())
    raw = 0.45 * L.coverage + 0.25 * L.stability + 0.25 * L.novelty - 0.30 * risk
    return max(0.0, min(1.0, raw))

# ------------------------------
# Event generators (Scar / Bloom)
# ------------------------------

def detect_sat(L: LogicState, C: Conditions) -> Optional[SAT]:
    risk = sum(r.risk for r in L.rules.values())
    # Trigger probabilities based on state; you can replace with domain checks
    p_under = max(0.0, (C.min_coverage - L.coverage))
    p_frag  = max(0.0, (C.min_stability - L.stability)) * 0.8
    p_risk  = max(0.0, (risk - C.max_risk)) * 0.9
    # Mild background chance of contradiction if many rules
    p_contra = max(0.0, (len(L.rules) - 6) * 0.03)

    # Normalize rough probabilities
    probs = [p_under, p_frag, p_risk, p_contra]
    labels = ['undercapture', 'fragility', 'risk_over', 'contradiction']
    total = sum(probs)
    if total <= 0 and random.random() > 0.1:
        return None
    # Weighted pick
    if total <= 0:
        kind = 'undercapture'
    else:
        r = random.random() * total
        acc = 0.0
        kind = labels[-1]
        for p, lab in zip(probs, labels):
            acc += p
            if r <= acc:
                kind = lab
                break
    severity = min(1.0, 0.3 + random.random() * 0.7)
    return SAT(kind=kind, severity=severity)

def detect_bloom(L: LogicState) -> Optional[Bloom]:
    # Bloom more likely when novelty is moderate and stability reasonable
    p_bloom = max(0.0, (0.5 - abs(L.novelty - 0.5))) * (0.4 + 0.6 * L.stability)
    if random.random() < p_bloom:
        return Bloom(pattern=f"pattern_{random.randint(1,999)}", strength=0.3 + 0.7 * random.random())
    return None

# ------------------------------
# Update Policy (Upd_Π)
# ------------------------------

def update_logic(L: LogicState, sat: Optional[SAT], bloom: Optional[Bloom]) -> LogicState:
    Lp = L.clone()
    Lp.version += 1

    if sat:
        # Scar-Induction — repair moves depend on SAT kind
        if sat.kind == 'undercapture':
            # Add a new explanatory rule; increases coverage & risk slightly, reduces stability
            rname = f"rule_cov_{Lp.version}"
            Lp.rules[rname] = Rule(rname, weight=1.0, risk=0.05 + 0.10 * sat.severity)
            Lp.coverage += 0.10 + 0.20 * sat.severity
            Lp.stability -= 0.05 + 0.10 * sat.severity
            Lp.novelty += 0.05
        elif sat.kind == 'fragility':
            # Consolidate rules; reduce risk and increase stability, slight coverage loss
            if Lp.rules:
                # Remove weakest rule by weight/risk ratio
                weakest = sorted(Lp.rules.values(), key=lambda r: (r.weight - r.risk))[:1]
                for w in weakest:
                    Lp.rules.pop(w.name, None)
            Lp.stability += 0.10 + 0.20 * sat.severity
            Lp.coverage -= 0.05
            Lp.novelty -= 0.05
        elif sat.kind == 'risk_over':
            # Harden safety; reduce risks on all rules, reduce novelty
            for rr in Lp.rules.values():
                rr.risk = max(0.0, rr.risk - (0.05 + 0.10 * sat.severity))
            Lp.stability += 0.05
            Lp.novelty -= 0.10
        elif sat.kind == 'contradiction':
            # Add reflection rule; improves stability but adds small risk
            rname = f"rule_reflect_{Lp.version}"
            Lp.rules[rname] = Rule(rname, weight=0.8, risk=0.06)
            Lp.stability += 0.15
            Lp.novelty += 0.02
        # Clamp
        Lp.coverage = max(0.0, min(1.0, Lp.coverage))
        Lp.stability = max(0.0, min(1.0, Lp.stability))
        Lp.novelty = max(0.0, min(1.0, Lp.novelty))

    if bloom:
        # Bloom-Induction — formalize stable pattern as low-risk rule
        rname = f"rule_bloom_{Lp.version}"
        added_risk = 0.02 + 0.05 * (1.0 - bloom.strength)
        Lp.rules[rname] = Rule(rname, weight=0.6 + 0.4 * bloom.strength, risk=added_risk)
        Lp.stability += 0.05 + 0.10 * bloom.strength
        Lp.coverage += 0.05 * bloom.strength
        Lp.novelty = max(0.0, Lp.novelty - 0.05)
        Lp.coverage = min(1.0, Lp.coverage)
        Lp.stability = min(1.0, Lp.stability)

    # Gentle drift to avoid stagnation
    Lp.novelty = max(0.0, min(1.0, Lp.novelty + random.uniform(-0.02, 0.02)))
    return Lp

# ------------------------------
# Adoption gates: COH, ADEQ, SAFE, GEN
# ------------------------------

def gate_coh(L: LogicState) -> bool:
    # Coherence gate: penalize excessive churn and contradictory mass (proxy by rule count vs stability)
    return L.stability >= 0.35 and len(L.rules) <= 18

def gate_adeq(L: LogicState, C: Conditions) -> bool:
    return L.coverage >= C.min_coverage and L.stability >= C.min_stability

def gate_safe(L: LogicState, C: Conditions) -> bool:
    risk = sum(r.risk for r in L.rules.values())
    return risk <= C.max_risk

def gate_gen(prev_ogi: float, new_ogi: float) -> bool:
    return new_ogi >= prev_ogi - 1e-9  # allow equality

# ------------------------------
# Simulation
# ------------------------------

def simulate(steps: int = 50, verbose: bool = True) -> Tuple[List[LogicState], List[StepLog]]:
    # Initial state
    L = LogicState(version=0,
                   rules={f"base_{i}": Rule(f"base_{i}", weight=1.0, risk=0.03) for i in range(3)},
                   coverage=0.25,
                   stability=0.65,
                   novelty=0.15)
    C = Conditions()

    history: List[LogicState] = [L.clone()]
    logs: List[StepLog] = []

    prev_ogi = compute_ogi(L)

    for t in range(1, steps + 1):
        sat = detect_sat(L, C)
        bloom = None if sat else detect_bloom(L)  # prefer SAT when both possible

        Lp = update_logic(L, sat, bloom)
        new_ogi = compute_ogi(Lp)

        coh = gate_coh(Lp)
        adeq = gate_adeq(Lp, C)
        safe = gate_safe(Lp, C)
        gen = gate_gen(prev_ogi, new_ogi)

        if not (coh and adeq and safe and gen):
            # If any gate fails, attempt a soft repair: roll back the highest-risk rule
            # and re-evaluate once.
            highest = None
            if Lp.rules:
                highest = max(Lp.rules.values(), key=lambda r: r.risk)
                Lp.rules.pop(highest.name, None)
                # Improve stability slightly after rollback
                Lp.stability = min(1.0, Lp.stability + 0.05)
                new_ogi = compute_ogi(Lp)
                coh = gate_coh(Lp)
                adeq = gate_adeq(Lp, C)
                safe = gate_safe(Lp, C)
                gen = gate_gen(prev_ogi, new_ogi)

        gates = (coh, adeq, safe, gen)
        accepted = all(gates)

        event = 'none'
        comment = ''
        if sat and accepted:
            event = 'scar'
            comment = f"Applied repair for {sat.kind} (sev={sat.severity:.2f})."
        elif bloom and accepted:
            event = 'bloom'
            comment = f"Integrated {bloom.pattern} (str={bloom.strength:.2f})."
        elif not accepted:
            event = 'none'
            comment = 'Update rejected by gates; soft rollback applied.'

        if accepted:
            L = Lp
            prev_ogi = new_ogi
        # else keep previous L

        history.append(L.clone())
        logs.append(StepLog(step=t, event=event, sat=sat, bloom=bloom, ogi=prev_ogi, gates_passed=gates, comment=comment))

        if verbose:
            sat_msg = f"SAT={sat.kind}(sev={sat.severity:.2f})" if sat else "SAT=None"
            blo_msg = f"Bloom={bloom.pattern}(str={bloom.strength:.2f})" if bloom else "Bloom=None"
            print(f"t={t:02d} v={L.version:02d} | {sat_msg} | {blo_msg} | OGI={prev_ogi:.3f} | Gates={gates} | {comment}")

    return history, logs

# ------------------------------
# Visualization
# ------------------------------

def plot_ogi(history: List[LogicState], logs: List[StepLog]) -> None:
    import matplotlib.pyplot as plt

    xs = list(range(len(history)))
    ys = [compute_ogi(L) for L in history]

    plt.figure()
    plt.plot(xs, ys, marker='o')
    plt.xlabel('Step')
    plt.ylabel('OGI')
    plt.title('Ontopolitical Generativity Index over time')

    # Annotate Scar/Bloom points
    for lg in logs:
        if lg.event in ('scar', 'bloom'):
            x = lg.step
            y = ys[x]
            txt = 'S' if lg.event == 'scar' else 'B'
            plt.annotate(txt, (x, y), textcoords="offset points", xytext=(0,8))

    plt.tight_layout()
    plt.show()

# ------------------------------
# Entrypoint
# ------------------------------
if __name__ == "__main__":
    hist, logs = simulate(steps=50, verbose=True)
    try:
        plot_ogi(hist, logs)
    except Exception as e:
        print("(Plotting skipped)", e)
    print("Simulation complete. Check the console for step logs.")  