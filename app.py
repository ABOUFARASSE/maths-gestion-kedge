"""Application web pédagogique de mathématiques appliquées à la gestion."""

from __future__ import annotations

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from maths import (
    advertising_model,
    budget_parts,
    future_value,
    integrated_product,
    linear_break_even,
    marginal_model,
    optimal_quantity,
    quadratic_analysis,
)


st.set_page_config(
    page_title="Mathématiques appliquées à la gestion — KEDGE",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
<style>
.block-container {max-width: 1180px; padding-top: 1.5rem; padding-bottom: 3rem;}
.hero {border-left: 6px solid #1f4e79; padding: .8rem 1.1rem; background: #f5f7fa; margin-bottom: 1rem;}
.method {border: 1px solid #b8c2cc; border-radius: 8px; padding: .85rem 1rem; background: white;}
.interpret {border-left: 5px solid #2e7d32; background:#f2f8f2; padding:.8rem 1rem; margin:.6rem 0;}
.warning {border-left: 5px solid #9a6700; background:#fff8e6; padding:.8rem 1rem; margin:.6rem 0;}
.small {font-size:.92rem; color:#4b5563;}
div[data-testid="stMetric"] {border:1px solid #d7dce1; padding:10px; border-radius:8px; background:white;}
</style>
""",
    unsafe_allow_html=True,
)


def euro(x: float) -> str:
    return f"{x:,.2f} €".replace(",", " ").replace(".", ",")


def number(x: float, digits: int = 2) -> str:
    return f"{x:,.{digits}f}".replace(",", " ").replace(".", ",")


def hero(title: str, subtitle: str) -> None:
    st.markdown(f'<div class="hero"><h2>{title}</h2><p>{subtitle}</p></div>', unsafe_allow_html=True)


def interpretation(text: str) -> None:
    st.markdown(f'<div class="interpret"><b>Interprétation de gestion.</b> {text}</div>', unsafe_allow_html=True)


def warning(text: str) -> None:
    st.markdown(f'<div class="warning"><b>Point de vigilance.</b> {text}</div>', unsafe_allow_html=True)


def correction(title: str, body: str) -> None:
    with st.expander(f"Afficher le corrigé détaillé — {title}"):
        st.markdown(body)


def home() -> None:
    hero(
        "Mathématiques appliquées à la gestion",
        "Comprendre une situation, effectuer les calculs, expérimenter, visualiser et prendre une décision.",
    )
    st.info("Application facultative de mise à niveau — Première année KEDGE Business School")
    st.markdown(
        """
Cette application ne remplace ni le cours ni le calcul manuel. Elle permet de vérifier un raisonnement,
de modifier les hypothèses d'un problème et d'observer immédiatement les conséquences sur la décision.

### Méthode commune aux cinq séances

1. **Question de gestion** : quelle décision veut-on éclairer ?
2. **Modèle mathématique** : quelles variables et quelles relations utilise-t-on ?
3. **Calcul détaillé** : comment passe-t-on des données au résultat ?
4. **Simulation** : que se passe-t-il lorsque les hypothèses changent ?
5. **Interprétation** : que signifie le résultat pour le décideur ?
"""
    )
    cards = [
        ("Séance 1", "Fractions et proportions", "Répartir un budget et calculer une remise."),
        ("Séance 2", "Puissances et degré 1", "Projeter une croissance et calculer un seuil."),
        ("Séance 3", "Second degré", "Déterminer une zone rentable et un profit maximal."),
        ("Séance 4", "Dérivées", "Comprendre les coûts et recettes marginaux."),
        ("Séance 5", "Étude de fonctions", "Optimiser une décision sous contrainte."),
        ("Cas final", "Lancement d'un produit", "Relier prix, demande, capacité et profit."),
    ]
    cols = st.columns(3)
    for i, (s, t, d) in enumerate(cards):
        with cols[i % 3]:
            st.markdown(f'<div class="method"><b>{s}</b><h4>{t}</h4><p>{d}</p></div>', unsafe_allow_html=True)
    st.markdown("### Comment utiliser l'application ?")
    st.markdown(
        """
- Commencez par lire la situation sans modifier les valeurs.
- Reproduisez le calcul sur papier.
- Utilisez ensuite les curseurs pour tester d'autres hypothèses.
- Avant d'afficher un corrigé, rédigez une phrase d'interprétation.
"""
    )


def session1() -> None:
    hero("Séance 1 — Fractions et proportions", "Cas : répartir un budget marketing et analyser une remise commerciale.")
    st.markdown("### 1. Situation de gestion")
    st.write("Une entreprise détermine la part de son chiffre d'affaires affectée au marketing, puis la part du budget marketing consacrée au digital.")
    c1, c2, c3 = st.columns(3)
    with c1:
        revenue = st.number_input("Chiffre d'affaires (€)", 10_000.0, 5_000_000.0, 250_000.0, 5_000.0)
    with c2:
        marketing_rate = st.slider("Part marketing du CA", 0.0, 0.50, 0.15, 0.01)
    with c3:
        digital_rate = st.slider("Part digitale du marketing", 0.0, 1.0, 0.42, 0.01)
    r = budget_parts(revenue, marketing_rate, digital_rate)
    m1, m2, m3 = st.columns(3)
    m1.metric("Budget marketing", euro(r["communication"]))
    m2.metric("Budget digital", euro(r["digital"]))
    m3.metric("Budget non marketing", euro(r["reste"]))

    st.markdown("### 2. Calcul détaillé")
    st.latex(rf"B_{{marketing}}={number(revenue)}\times {number(marketing_rate,2)}={number(r['communication'])}\ \text{{€}}")
    st.latex(rf"B_{{digital}}={number(r['communication'])}\times {number(digital_rate,2)}={number(r['digital'])}\ \text{{€}}")
    st.latex(rf"B_{{reste}}={number(revenue)}-{number(r['communication'])}={number(r['reste'])}\ \text{{€}}")

    chart_data = pd.DataFrame({"Poste": ["Digital", "Marketing hors digital", "Autres usages"], "Montant": [r["digital"], r["communication_hors_digital"], r["reste"]]})
    st.plotly_chart(px.pie(chart_data, names="Poste", values="Montant", hole=.42, title="Répartition du chiffre d'affaires"), use_container_width=True)
    interpretation(f"Le marketing représente {marketing_rate:.0%} du chiffre d'affaires. Le digital reçoit {digital_rate:.0%} du budget marketing, soit {r['digital']/revenue:.1%} du chiffre d'affaires total.")

    st.markdown("### 3. Remise et TVA")
    a, b, c = st.columns(3)
    with a:
        price = st.number_input("Prix catalogue HT (€)", 1.0, 10_000.0, 120.0, 1.0)
    with b:
        discount = st.slider("Remise", 0.0, .70, .15, .01)
    with c:
        vat = st.selectbox("Taux de TVA", [0.055, 0.10, 0.20], index=2, format_func=lambda x: f"{x:.1%}")
    net = price * (1 - discount)
    total = net * (1 + vat)
    st.latex(rf"P_{{remisé,HT}}={number(price)}\times(1-{number(discount,2)})={number(net)}\ \text{{€}}")
    st.latex(rf"P_{{TTC}}={number(net)}\times(1+{number(vat,3)})={number(total)}\ \text{{€}}")
    warning("Une baisse de 15 % suivie d'une hausse de 15 % ne ramène pas au prix initial : les deux pourcentages ne s'appliquent pas à la même base.")

    st.markdown("### 4. Exercice")
    st.write("Un magasin consacre 3/8 d'un budget de 48 000 € à sa communication. Les réseaux sociaux représentent 2/5 du budget de communication. Calculez les deux montants.")
    correction("budget de communication", r"""
**Étape 1 — communication**

\[
48\,000\times\frac{3}{8}=\frac{48\,000}{8}\times3=6\,000\times3=18\,000\text{ €}.
\]

**Étape 2 — réseaux sociaux**

\[
18\,000\times\frac{2}{5}=\frac{18\,000}{5}\times2=3\,600\times2=7\,200\text{ €}.
\]

Les réseaux sociaux reçoivent donc **7 200 €**, soit \(7\,200/48\,000=15\%\) du budget total.
""")


def session2() -> None:
    hero("Séance 2 — Puissances et équations du premier degré", "Cas : croissance composée et comparaison de deux offres.")
    st.markdown("### 1. Croissance composée")
    c1, c2, c3 = st.columns(3)
    with c1:
        initial = st.number_input("Valeur initiale (€)", 100.0, 1_000_000.0, 10_000.0, 500.0)
    with c2:
        rate = st.slider("Taux annuel", -0.20, 0.30, 0.04, 0.01)
    with c3:
        years = st.slider("Nombre d'années", 1, 30, 8)
    final = future_value(initial, rate, years)
    factor = (1 + rate) ** years
    st.latex(rf"V_n=V_0(1+t)^n={number(initial)}\times(1+{number(rate,2)})^{{{years}}}={number(final)}")
    a, b, c = st.columns(3)
    a.metric("Coefficient global", number(factor, 4))
    b.metric("Valeur finale", euro(final))
    c.metric("Variation cumulée", f"{factor-1:.2%}")
    timeline = pd.DataFrame({"Année": range(years + 1), "Valeur": [future_value(initial, rate, n) for n in range(years + 1)]})
    st.plotly_chart(px.line(timeline, x="Année", y="Valeur", markers=True, title="Évolution composée"), use_container_width=True)
    warning(f"Le taux cumulé n'est pas simplement {years} × {rate:.0%}. Le véritable taux cumulé est {factor-1:.2%}, car chaque période repart de la valeur obtenue précédemment.")

    st.markdown("### 2. Équation du premier degré : comparer deux offres")
    st.write("Offre A : abonnement fixe et coût unitaire faible. Offre B : abonnement plus faible et coût unitaire plus élevé.")
    c1, c2 = st.columns(2)
    with c1:
        fixed_a = st.number_input("Forfait A (€)", 0.0, 5_000.0, 200.0, 10.0)
        unit_a = st.number_input("Coût unitaire A (€)", 0.0, 100.0, 4.0, .5)
    with c2:
        fixed_b = st.number_input("Forfait B (€)", 0.0, 5_000.0, 50.0, 10.0)
        unit_b = st.number_input("Coût unitaire B (€)", 0.0, 100.0, 7.0, .5)
    if abs(unit_a - unit_b) < 1e-12:
        warning("Les coûts unitaires sont identiques : il n'existe pas de seuil unique. L'offre ayant le plus petit forfait est toujours préférable.")
    else:
        q = (fixed_b - fixed_a) / (unit_a - unit_b)
        st.latex(rf"{number(fixed_a)}+{number(unit_a)}q={number(fixed_b)}+{number(unit_b)}q")
        st.latex(rf"({number(unit_a)}-{number(unit_b)})q={number(fixed_b)}-{number(fixed_a)}")
        st.latex(rf"q=\frac{{{number(fixed_b-fixed_a)}}}{{{number(unit_a-unit_b)}}}={number(q)}")
        qmax = max(100.0, max(0, q) * 1.8)
        qs = np.linspace(0, qmax, 150)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=qs, y=fixed_a + unit_a * qs, name="Offre A"))
        fig.add_trace(go.Scatter(x=qs, y=fixed_b + unit_b * qs, name="Offre B"))
        if q >= 0:
            fig.add_vline(x=q, line_dash="dash", annotation_text=f"Seuil = {q:.1f}")
        fig.update_layout(title="Comparaison du coût total", xaxis_title="Nombre d'unités", yaxis_title="Coût (€)")
        st.plotly_chart(fig, use_container_width=True)
        interpretation(f"Les deux offres coûtent le même montant pour {q:.2f} unités. La décision de part et d'autre du seuil dépend de la pente de chaque droite, c'est-à-dire de son coût unitaire.")

    st.markdown("### 3. Exercice")
    st.write("Un chiffre d'affaires de 50 000 € progresse de 5 % par an pendant trois ans. Calculez sa valeur finale.")
    correction("croissance composée", r"""
Le coefficient multiplicateur annuel est \(1+5/100=1,05\).

\[
V_3=50\,000\times1,05^3.
\]

Calcul année par année :

- année 1 : \(50\,000\times1,05=52\,500\) € ;
- année 2 : \(52\,500\times1,05=55\,125\) € ;
- année 3 : \(55\,125\times1,05=57\,881,25\) €.

La valeur finale est donc **57 881,25 €**. La hausse cumulée est de **15,7625 %**, et non exactement 15 %.
""")


def session3() -> None:
    hero("Séance 3 — Second degré et inéquations", "Cas : déterminer les seuils de rentabilité et le profit maximal.")
    st.markdown("### 1. Modèle de profit")
    st.latex(r"P(q)=pq-F-cq-sq^2=-sq^2+(p-c)q-F")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        price = st.number_input("Prix unitaire p (€)", 1.0, 500.0, 80.0, 1.0)
    with c2:
        fixed = st.number_input("Coût fixe F (€)", 0.0, 100_000.0, 500.0, 100.0)
    with c3:
        variable = st.number_input("Coût variable c (€)", 0.0, 400.0, 20.0, 1.0)
    with c4:
        saturation = st.number_input("Saturation s", 0.01, 10.0, 1.0, .1)
    a, b, c = -saturation, price - variable, -fixed
    res = quadratic_analysis(a, b, c)
    m1, m2, m3 = st.columns(3)
    m1.metric("Discriminant Δ", number(res.discriminant))
    m2.metric("Quantité du sommet", number(res.vertex_x))
    m3.metric("Profit maximal théorique", euro(res.vertex_y))
    st.markdown("### 2. Calcul détaillé")
    st.latex(rf"P(q)={number(a)}q^2+{number(b)}q+({number(c)})")
    st.latex(rf"\Delta=b^2-4ac={number(b)}^2-4\times({number(a)})\times({number(c)})={number(res.discriminant)}")
    if res.roots:
        r1, r2 = res.roots
        st.latex(rf"q_1=\frac{{-b-\sqrt{{\Delta}}}}{{2a}}={number(r1)},\qquad q_2=\frac{{-b+\sqrt{{\Delta}}}}{{2a}}={number(r2)}")
        st.latex(rf"q_S=-\frac{{b}}{{2a}}={number(res.vertex_x)},\qquad P(q_S)={number(res.vertex_y)}")
        qmax = max(10.0, r2 * 1.25)
        qs = np.linspace(0, qmax, 300)
        profits = a * qs**2 + b * qs + c
        fig = px.line(x=qs, y=profits, labels={"x": "Quantité q", "y": "Profit (€)"}, title="Profit en fonction de la quantité")
        fig.add_hline(y=0, line_color="black")
        fig.add_vline(x=res.vertex_x, line_dash="dash", annotation_text="Sommet")
        st.plotly_chart(fig, use_container_width=True)
        interpretation(f"Le profit est positif entre les deux racines, soit approximativement entre {r1:.2f} et {r2:.2f} unités. Son maximum théorique, {euro(res.vertex_y)}, est atteint pour {res.vertex_x:.2f} unités.")
    else:
        warning("Le discriminant est négatif : le profit ne coupe pas l'axe horizontal. Avec les paramètres choisis, il n'existe aucun seuil réel.")
    warning("Les racines répondent à « quand le profit est-il nul ? ». Le sommet répond à « quand le profit est-il maximal ? ». Ce ne sont pas les mêmes valeurs.")

    st.markdown("### 3. Exercice")
    st.write(r"On considère le profit \(P(q)=-q^2+10q-16\). Déterminez les seuils de rentabilité et le profit maximal.")
    correction("second degré", r"""
On identifie \(a=-1\), \(b=10\) et \(c=-16\).

\[
\Delta=b^2-4ac=10^2-4\times(-1)\times(-16)=100-64=36.
\]

Comme \(\Delta>0\), il existe deux racines :

\[
q_1=\frac{-10+\sqrt{36}}{-2}=2,\qquad
q_2=\frac{-10-\sqrt{36}}{-2}=8.
\]

Le coefficient \(a\) est négatif : la parabole est tournée vers le bas. Le profit est donc positif entre 2 et 8.

Le sommet a pour abscisse :

\[
q_S=-\frac{b}{2a}=-\frac{10}{-2}=5.
\]

\[
P(5)=-5^2+10\times5-16=-25+50-16=9.
\]

Le profit maximal est **9 unités monétaires**, atteint pour **5 unités produites**.
""")


def session4() -> None:
    hero("Séance 4 — Dérivées et analyse marginale", "Cas : comprendre le coût d'une unité supplémentaire et rechercher l'optimum.")
    st.markdown("### 1. Idée simple")
    st.markdown("La dérivée mesure la vitesse de variation d'une grandeur. En gestion, elle répond notamment à la question : **que se passe-t-il approximativement si l'on produit ou vend une unité de plus ?**")
    st.latex(r"C'(q)\approx C(q+1)-C(q)")
    st.markdown("### 2. Modèle")
    st.latex(r"C(q)=F+aq+bq^2,\qquad R(q)=pq-dq^2,\qquad P(q)=R(q)-C(q)")
    c1, c2, c3 = st.columns(3)
    with c1:
        fixed = st.number_input("Coût fixe F (€)", 0.0, 100_000.0, 500.0, 100.0)
        a = st.number_input("Coefficient a", 0.0, 500.0, 30.0, 1.0)
    with c2:
        b = st.number_input("Coefficient b", 0.01, 20.0, .5, .1)
        price = st.number_input("Prix potentiel p (€)", 1.0, 1_000.0, 100.0, 1.0)
    with c3:
        d = st.number_input("Pente de demande d", 0.01, 20.0, .8, .1)
        q = st.slider("Quantité étudiée q", 0.0, 100.0, 20.0, 1.0)
    vals = marginal_model(fixed, a, b, price, d, q)
    exact_next_cost = marginal_model(fixed, a, b, price, d, q + 1)["cost"] - vals["cost"]
    st.markdown("### 3. Dérivation pas à pas")
    st.latex(rf"C'(q)=0+{number(a)}+2\times {number(b)}q={number(a)}+{number(2*b)}q")
    st.latex(rf"R'(q)={number(price)}-2\times {number(d)}q={number(price)}-{number(2*d)}q")
    st.latex(rf"P'(q)=R'(q)-C'(q)")
    m1, m2, m3 = st.columns(3)
    m1.metric("Coût marginal C′(q)", euro(vals["marginal_cost"]))
    m2.metric("Recette marginale R′(q)", euro(vals["marginal_revenue"]))
    m3.metric("Profit marginal P′(q)", euro(vals["marginal_profit"]))
    st.markdown("### 4. Variation exacte et approximation")
    st.latex(rf"C({number(q+1,0)})-C({number(q,0)})={number(exact_next_cost)}\ \text{{€}}")
    st.latex(rf"C'({number(q,0)})={number(vals['marginal_cost'])}\ \text{{€}}")
    interpretation(f"À {q:.0f} unités, une unité supplémentaire augmente approximativement le coût de {euro(vals['marginal_cost'])}. La variation exacte est {euro(exact_next_cost)}. L'écart provient de la courbure du coût.")
    try:
        qstar = optimal_quantity(a, b, price, d)
        qstar = max(0.0, qstar)
        st.latex(rf"P'(q)=0\Longleftrightarrow {number(price-a)}-2({number(b+d)})q=0\Longleftrightarrow q^*={number(qstar)}")
        qs = np.linspace(0, max(60, qstar * 2), 250)
        mc = a + 2 * b * qs
        mr = price - 2 * d * qs
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=qs, y=mc, name="Coût marginal C′(q)"))
        fig.add_trace(go.Scatter(x=qs, y=mr, name="Recette marginale R′(q)"))
        fig.add_vline(x=qstar, line_dash="dash", annotation_text=f"q*={qstar:.2f}")
        fig.update_layout(title="Condition d'optimum : recette marginale = coût marginal", xaxis_title="Quantité", yaxis_title="Montant marginal (€)")
        st.plotly_chart(fig, use_container_width=True)
        interpretation(f"Avant {qstar:.2f}, la recette marginale dépasse le coût marginal : produire davantage améliore le profit. Après {qstar:.2f}, l'unité supplémentaire coûte davantage qu'elle ne rapporte.")
    except ValueError as exc:
        warning(str(exc))

    st.markdown("### 5. Exercice")
    st.write(r"Une entreprise a pour coût \(C(q)=500+20q+0,5q^2\). Calculez \(C'(q)\), puis \(C'(10)\), et interprétez.")
    correction("coût marginal", r"""
On dérive chaque terme séparément :

- la dérivée de la constante 500 est 0 ;
- la dérivée de \(20q\) est 20 ;
- la dérivée de \(0,5q^2\) est \(2\times0,5q=q\).

Ainsi :

\[
C'(q)=0+20+q=20+q.
\]

Pour \(q=10\) :

\[
C'(10)=20+10=30.
\]

Au voisinage d'une production de 10 unités, produire une unité supplémentaire augmente approximativement le coût total de **30 €**.

Vérification exacte :

\[
C(11)-C(10)=\bigl(500+220+0,5\times121\bigr)-\bigl(500+200+0,5\times100\bigr)
\]

\[
=780,5-750=30,5\text{ €}.
\]

La dérivée donne ici une approximation de 30 €, proche de la variation exacte de 30,50 €.
""")


def session5() -> None:
    hero("Séance 5 — Étude de fonctions", "Cas : optimiser un budget publicitaire avec saturation des ventes.")
    st.markdown("### 1. Question de gestion")
    st.write("Lorsque le budget publicitaire augmente, les ventes progressent, mais de moins en moins rapidement. Quel budget maximise le profit ?")
    st.latex(r"V(x)=V_{max}\frac{x}{x+k},\qquad P(x)=mV(x)-x")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        vmax = st.number_input("Ventes maximales", 10.0, 100_000.0, 1_200.0, 50.0)
    with c2:
        k = st.number_input("Saturation k (€)", 100.0, 1_000_000.0, 20_000.0, 1_000.0)
    with c3:
        margin = st.number_input("Marge par vente (€)", 1.0, 10_000.0, 80.0, 5.0)
    with c4:
        max_budget = st.number_input("Budget maximal (€)", 0.0, 1_000_000.0, 50_000.0, 1_000.0)
    model0 = advertising_model(vmax, k, margin, 0)
    theoretical = model0["theoretical_optimum"]
    recommended = min(max_budget, theoretical)
    at_opt = advertising_model(vmax, k, margin, recommended)
    st.markdown("### 2. Dérivée et point critique")
    st.latex(r"V'(x)=V_{max}\frac{k}{(x+k)^2}")
    st.latex(r"P'(x)=mV_{max}\frac{k}{(x+k)^2}-1")
    st.latex(r"P'(x)=0\Longleftrightarrow (x+k)^2=mV_{max}k\Longleftrightarrow x^*=\sqrt{mV_{max}k}-k")
    m1, m2, m3 = st.columns(3)
    m1.metric("Optimum théorique", euro(theoretical))
    m2.metric("Budget recommandé", euro(recommended))
    m3.metric("Profit associé", euro(at_opt["profit"]))
    xmax = max(1_000.0, max_budget * 1.3, theoretical * 1.3)
    xs = np.linspace(0, xmax, 350)
    profits = [advertising_model(vmax, k, margin, x)["profit"] for x in xs]
    fig = px.line(x=xs, y=profits, labels={"x": "Budget publicitaire (€)", "y": "Profit (€)"}, title="Profit en fonction du budget publicitaire")
    fig.add_vline(x=theoretical, line_dash="dash", annotation_text="Optimum théorique")
    fig.add_vline(x=max_budget, line_dash="dot", line_color="orange", annotation_text="Contrainte")
    st.plotly_chart(fig, use_container_width=True)
    if theoretical <= max_budget:
        interpretation(f"L'optimum théorique de {euro(theoretical)} respecte la contrainte budgétaire. Il peut donc être retenu.")
    else:
        interpretation(f"L'optimum théorique de {euro(theoretical)} dépasse le budget maximal. Sur le domaine réalisable, la meilleure décision est donc la borne {euro(max_budget)}.")
    warning("Une étude de fonction ne s'arrête pas à résoudre P′(x)=0. Il faut étudier le signe de la dérivée, tenir compte du domaine et comparer les points critiques aux bornes.")

    st.markdown("### 3. Exercice")
    st.write(r"Étudiez \(P(q)=-2q^2+80q-600\) sur \([0;30]\) et déterminez son maximum.")
    correction("étude complète", r"""
**1. Dérivée**

\[
P'(q)=-4q+80.
\]

**2. Point critique**

\[
-4q+80=0\Longleftrightarrow -4q=-80\Longleftrightarrow q=20.
\]

**3. Signe**

- si \(q<20\), alors \(-4q+80>0\) : le profit augmente ;
- si \(q=20\), alors \(P'(q)=0\) ;
- si \(q>20\), alors \(-4q+80<0\) : le profit diminue.

**4. Valeurs à comparer**

\[
P(0)=-600,
\]

\[
P(20)=-2\times20^2+80\times20-600=-800+1\,600-600=200,
\]

\[
P(30)=-2\times30^2+80\times30-600=-1\,800+2\,400-600=0.
\]

Le maximum sur \([0;30]\) est donc **200 €**, atteint pour une production de **20 unités**.
""")


def integrated_case() -> None:
    hero("Cas intégrateur — Lancement d'un produit", "Relier demande, prix, capacité, coûts et profit.")
    st.markdown("### Mission")
    st.write("Vous accompagnez une entreprise qui prépare le lancement d'un produit. Vous devez proposer un prix en tenant compte de la demande, de la capacité et des coûts.")
    st.latex(r"q(p)=A-Bp,\qquad C(q)=F+cq,\qquad P(p)=p\,q(p)-C(q(p))")
    c1, c2, c3 = st.columns(3)
    with c1:
        A = st.number_input("Demande potentielle A", 10.0, 100_000.0, 1_000.0, 50.0)
        B = st.number_input("Sensibilité au prix B", .1, 1_000.0, 10.0, .5)
    with c2:
        fixed = st.number_input("Coût fixe (€)", 0.0, 1_000_000.0, 5_000.0, 500.0)
        variable = st.number_input("Coût variable unitaire (€)", 0.0, 10_000.0, 20.0, 1.0)
    with c3:
        capacity = st.number_input("Capacité maximale", 1.0, 100_000.0, 600.0, 25.0)
        tested_price = st.slider("Prix testé (€)", 0.0, max(10.0, A / B), 55.0, 1.0)
    tested = integrated_product(A, B, fixed, variable, tested_price, capacity)
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Demande", number(tested["demand"], 0))
    m2.metric("Ventes réalisables", number(tested["quantity"], 0))
    m3.metric("Chiffre d'affaires", euro(tested["revenue"]))
    m4.metric("Profit", euro(tested["profit"]))

    prices = np.linspace(0, max(10.0, A / B), 500)
    rows = [integrated_product(A, B, fixed, variable, p, capacity) for p in prices]
    profits = np.array([r["profit"] for r in rows])
    i = int(np.argmax(profits))
    best_price, best = prices[i], rows[i]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=prices, y=profits, name="Profit"))
    fig.add_vline(x=best_price, line_dash="dash", annotation_text=f"Prix recommandé ≈ {best_price:.2f} €")
    fig.update_layout(title="Recherche numérique du meilleur prix réalisable", xaxis_title="Prix (€)", yaxis_title="Profit (€)")
    st.plotly_chart(fig, use_container_width=True)
    interpretation(f"Avec les hypothèses retenues, la simulation recommande un prix proche de {euro(best_price)}, pour environ {best['quantity']:.0f} ventes et un profit de {euro(best['profit'])}.")
    warning("Ce résultat dépend entièrement du modèle de demande supposé, des coûts et de la capacité. Une recommandation quantitative doit toujours être accompagnée d'une analyse de sensibilité et d'une discussion des hypothèses.")

    st.markdown("### Défi")
    st.write("Modifiez successivement la capacité, le coût variable et la sensibilité au prix. Pour chaque scénario, expliquez pourquoi le prix recommandé et le profit évoluent.")


PAGES = {
    "Accueil": home,
    "Séance 1 — Fractions et proportions": session1,
    "Séance 2 — Puissances et degré 1": session2,
    "Séance 3 — Second degré et inéquations": session3,
    "Séance 4 — Dérivées": session4,
    "Séance 5 — Étude de fonctions": session5,
    "Cas intégrateur — Lancement d'un produit": integrated_case,
}

with st.sidebar:
    st.title("Maths & Gestion")
    st.caption("Première année — KEDGE")
    selected = st.radio("Navigation", list(PAGES))
    st.divider()
    st.markdown("**Conseil**")
    st.caption("Faites d'abord le calcul sur papier, puis utilisez la simulation pour vérifier et explorer.")
    st.divider()
    st.caption("Application pédagogique facultative. Les résultats dépendent des hypothèses saisies.")

PAGES[selected]()
