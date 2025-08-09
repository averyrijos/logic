# Proving the Hard Problem of Consciousness (clean, self-contained markdown)

> **Claim (Hard Problem, formal):**
> Let **T\_str** be any complete, purely structural–functional theory of a physical/cognitive system (causal topology, computational organization, dynamics) formulated in a first-order language **L\_str** whose predicates are **structural** (invariant under structure-preserving isomorphisms).
> Let **Φ** be a phenomenal predicate (“there is something it is like”) in a disjoint language **L\_phen**.
> Then there exist two **T\_str**-models **M₀, M₁** that are **elementarily equivalent in L\_str** but disagree on **Φ** in their **L\_str ∪ L\_phen**-expansions.
> Hence **T\_str ⊬ Φ** and **T\_str ⊬ ¬Φ**.
> Therefore phenomenal facts are **not entailed a priori** by structural–functional facts: the Hard Problem.

---

## 1) Setup

**1.1 Languages.**

* **L\_str**: symbols for states, causal/functional relations, transition rules; no phenomenal terms.
* **L\_phen**: a unary predicate **Qual(x)** or, more generally, a map **q: States → Q** (qualia types).
* **L\_tot := L\_str ∪ L\_phen**.

**1.2 Structural theories.**

* **T\_str** is a consistent, recursively axiomatized theory whose intended models capture *all* physical/functional organization of the target system.
* **Isomorphism invariance:** If **h: M → N** is an **L\_str**-isomorphism then any **L\_str**-sentence has the same truth in **M** and **N**. (By definition of “purely structural”.)

**1.3 Phenomenal assignment.**

* An **expansion** of an **L\_str**-model **M** is an **L\_tot**-model **(M, q)** obtained by adding an interpretation of **L\_phen** (e.g., a predicate **Qual** or map **q**).
* Intuitively, **q** picks out “what it’s like” at each physical/functional state.

---

## 2) Core Lemma (Beth-style Non-Definability Test)

> **Lemma (Beth).** If a predicate **P** on models of **T\_str** is **implicitly definable** in **L\_str** (i.e., any two **L\_tot**-expansions of an **L\_str**-model that satisfy the same **L\_str** theorems agree on **P**), then **P** is **explicitly definable** in **L\_str**.
> Contraposition: if there exist two **L\_tot**-expansions of some **L\_str**-model that are **elementarily equivalent in L\_str** but assign **different extensions** to **P**, then **P** is **not** definable in **L\_str** and is **not** entailed by **T\_str**.

We’ll apply this with **P ≡ Qual** (or **q**).

---

## 3) Two separating expansions exist

Let **M** be any model of **T\_str** (a fully specified structural/functional system).

**Construction A (Zombie expansion).**
Define **(M, q₀)** by assigning **q₀(x) = 0** (no qualia) for all relevant states **x**. This imposes **no** change to **L\_str**; thus **(M, q₀)** is an **L\_tot**-expansion whose **L\_str**-reduct is still **M**.

**Construction B (Phenomenal expansion).**
Define **(M, q₁)** by assigning a **nontrivial** qualia map **q₁(x) ≠ 0** for some states (or a rich range of values in **Q**), chosen arbitrarily **subject only to constraints expressible in L\_str** (there are none by assumption, because **T\_str** has no phenomenal vocabulary).

**Observation.**

* The **L\_str**-reducts of **(M, q₀)** and **(M, q₁)** are the **same model M**.
* Therefore **(M, q₀)** and **(M, q₁)** satisfy **exactly the same L\_str sentences** (they are elementarily equivalent in **L\_str**).
* Yet **Qual** (or **q**) differs between the two expansions.

By the Beth Lemma contraposition, **Qual** is **not L\_str-definable** and thus **not entailed** (nor refutable) by **T\_str**.

*Variants.*

* **Inverted qualia:** choose a permutation **π: Q → Q** and let **q₂ := π ∘ q₁**; then **(M, q₁)** and **(M, q₂)** agree on **L\_str** but differ phenomenally.
* **Isomorphic duplicates:** any **L\_str**-isomorphism **h: M → N** lifts to **(N, q₁ ∘ h⁻¹)**, preserving structure while allowing independent phenomenal relabeling.

---

## 4) The Theorem

> **Theorem (Hard Problem Non-Derivability).**
> For purely structural **T\_str** and phenomenal predicate **Φ** as above, there exist **L\_tot**-expansions that agree on all **L\_str** truths but disagree on **Φ**. Hence **T\_str ⊬ Φ** and **T\_str ⊬ ¬Φ**. Phenomenal facts are not a priori consequences of structural–functional facts.

**Proof.** By Constructions A/B and the Beth non-definability lemma. ∎

---

## 5) Corollaries (connecting classic arguments)

* **Zombie Conceivability (model-theoretic form).** The “zombie” case is just **(M, q₀)**. Since it preserves all **L\_str** truths, zombies are **formally consistent** with **T\_str**; thus **Φ** is not entailed by structure.
* **Mary/Knowledge Argument (epistemic sharpening).** If **Φ** were **L\_str**-definable, complete **L\_str** knowledge would fix phenomenal facts; but by the theorem, **L\_str** leaves them underdetermined. So new knowledge upon seeing red is expected.

---

## 6) What would collapse the Hard Problem?

Only by **adding non-structural bridge principles** to **T\_str**:

* **Psychophysical axioms:** e.g., laws **B:** “for any state meeting structural predicate **S(x)**, **Qual(x) = q\***.”
* **Identity postulates:** add **Qual(x)** to **L\_str** as a primitive with axioms linking it to structure.

But then the resulting theory is **not purely structural**; it **extends the base vocabulary/axioms** precisely in the phenomenal direction. That move **addresses** the Hard Problem by **changing the theory**, not by deriving **Φ** from structure.

---

## 7) Metaformal Logic (Logiforma) reading

* **SAT detection:** “Phenomenal underdetermination” is a **Structured Anomaly Token** for a purely structural base.
* **Lawful upgrade:** add auditable **bridge axioms** (new predicates/rules) as an **Upd** step.
* **Consequence:** You don’t *deduce* **Φ** from **T\_str**; you **govern** a principled extension where **Φ** becomes decidable. This **respects** the theorem (non-derivability) while **solving** the engineering problem (predictive/empirical grip on phenomenality).

---

## 8) Summary in one line

Because phenomenal predicates are **not explicitly (nor implicitly) definable** in a purely structural language, there are always **structurally indistinguishable** models that differ phenomenally; therefore **structure alone cannot entail consciousness**—which is exactly the **Hard Problem**.
