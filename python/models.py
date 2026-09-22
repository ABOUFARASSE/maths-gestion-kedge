import json, math

def _fmt(x, digits=2):
    return round(float(x), digits)

def solve(case_id, p):
    if case_id == "budget":
        total=p["total"]; digital=total*p["digital"]/100; training=total*p["training"]/100; equipment=total*p["equipment"]/100
        remaining=total-digital-training-equipment; minimum=total*p["reserve_min"]/100
        ok=remaining>=minimum
        return {"metrics":[["Budget disponible",_fmt(total),"€"],["Total engagé",_fmt(total-remaining),"€"],["Réserve",_fmt(remaining),"€"],["Marge sur réserve",_fmt(remaining-minimum),"€"]],
                "chart":{"type":"pie","labels":["Communication","Formation","Équipement","Réserve"],"values":[digital,training,equipment,remaining]},
                "decision":("Répartition soutenable" if ok else "Répartition à réviser"),
                "explanation":(f"La réserve atteint {_fmt(remaining/total*100,1)} % du budget, contre un minimum exigé de {p['reserve_min']} %." if total else "Budget nul."),
                "alert":not ok}
    if case_id == "growth":
        years=int(p["years"]); initial=p["initial"]; rates=[p["pessimistic"],p["central"],p["optimistic"]]
        names=["Prudent","Central","Dynamique"]; xs=list(range(years+1)); series=[]
        for name,r in zip(names,rates): series.append({"name":name,"x":xs,"y":[initial*(1+r/100)**t for t in xs]})
        final=series[1]["y"][-1]; gap=final-p["capacity"]
        return {"metrics":[["Valeur initiale",initial,"€"],["Prévision centrale",_fmt(final),"€"],["Croissance cumulée",_fmt((final/initial-1)*100,1),"%"],["Écart à la capacité",_fmt(gap),"€"]],
                "chart":{"type":"lines","series":series},"decision":("Capacité à renforcer" if gap>0 else "Capacité suffisante"),
                "explanation":f"Au scénario central, l'activité atteint {_fmt(final):,.0f} € après {years} ans. La croissance composée représente {_fmt((final/initial-1)*100,1)} % sur la période.","alert":gap>0}
    if case_id == "supplier":
        q=p["quantity"]; ca=p["fixed_a"]+p["unit_a"]*q; cb=p["fixed_b"]+p["unit_b"]*q
        den=p["unit_b"]-p["unit_a"]; threshold=(p["fixed_a"]-p["fixed_b"])/den if den else None
        winner="A" if ca<cb else "B" if cb<ca else "A ou B"
        xmax=max(q*1.6,(threshold or q)*1.35,10); xs=[xmax*i/40 for i in range(41)]
        return {"metrics":[["Coût fournisseur A",_fmt(ca),"€"],["Coût fournisseur B",_fmt(cb),"€"],["Économie",_fmt(abs(ca-cb)),"€"],["Seuil d'indifférence",_fmt(threshold) if threshold is not None else "—","unités"]],
                "chart":{"type":"lines","series":[{"name":"Fournisseur A","x":xs,"y":[p['fixed_a']+p['unit_a']*x for x in xs]},{"name":"Fournisseur B","x":xs,"y":[p['fixed_b']+p['unit_b']*x for x in xs]}],"marker":{"x":q,"y":min(ca,cb)}},
                "decision":f"Choisir le fournisseur {winner}","explanation":f"Pour {q:.0f} unités, l'offre {winner} minimise le coût total. Le choix peut changer lorsque le volume franchit le seuil d'indifférence.","alert":False}
    if case_id == "break_even":
        margin=p["price"]-p["unit_cost"]; threshold=p["fixed"]/margin if margin>0 else math.inf; forecast=p["forecast"]
        profit=margin*forecast-p["fixed"]; safety=forecast-threshold if math.isfinite(threshold) else -math.inf
        xs=[p["capacity"]*i/50 for i in range(51)]
        return {"metrics":[["Marge unitaire",_fmt(margin),"€"],["Seuil de rentabilité",math.ceil(threshold) if math.isfinite(threshold) else "Impossible","unités"],["Bénéfice prévisionnel",_fmt(profit),"€"],["Marge de sécurité",_fmt(safety) if math.isfinite(safety) else "—","unités"]],
                "chart":{"type":"lines","series":[{"name":"Recettes","x":xs,"y":[p['price']*x for x in xs]},{"name":"Coûts","x":xs,"y":[p['fixed']+p['unit_cost']*x for x in xs]}],"marker":{"x":forecast,"y":p['price']*forecast}},
                "decision":("Projet rentable au volume prévu" if profit>0 else "Projet non rentable au volume prévu"),"explanation":f"La prévision de {forecast:.0f} ventes est {'au-dessus' if safety>=0 else 'en dessous'} du point mort de {math.ceil(threshold) if math.isfinite(threshold) else '—'} unités.","alert":profit<=0}
    if case_id == "marginal":
        q=p["quantity"]; exact_c=p["a"]+p["b"]*((q+1)**2-q**2); mc=p["a"]+2*p["b"]*q
        mr=p["price"]-2*p["d"]*q; mp=mr-mc; exact_p=(p["price"]*(q+1)-p["d"]*(q+1)**2-p["fixed"]-p["a"]*(q+1)-p["b"]*(q+1)**2)-(p["price"]*q-p["d"]*q*q-p["fixed"]-p["a"]*q-p["b"]*q*q)
        xs=[max(0,q-60)+i*3 for i in range(41)]
        return {"metrics":[["Coût marginal",_fmt(mc),"€/unité"],["Coût exact de l'unité suivante",_fmt(exact_c),"€"],["Recette marginale",_fmt(mr),"€/unité"],["Profit marginal",_fmt(mp),"€/unité"]],
                "chart":{"type":"lines","series":[{"name":"Recette marginale","x":xs,"y":[p['price']-2*p['d']*x for x in xs]},{"name":"Coût marginal","x":xs,"y":[p['a']+2*p['b']*x for x in xs]}],"marker":{"x":q,"y":mc}},
                "decision":("Augmenter légèrement la production" if mp>0 else "Ne pas augmenter la production"),"explanation":f"Autour de {q:.0f} unités, une unité supplémentaire modifie le profit d'environ {_fmt(mp)} €. La variation exacte est de {_fmt(exact_p)} €.","alert":mp<0}
    if case_id == "optimization":
        raw=p["b"]/(2*p["a"]); q=max(0,min(p["capacity"],raw)); profit=-p["a"]*q*q+p["b"]*q-p["fixed"]
        xs=[p["capacity"]*i/50 for i in range(51)]; ys=[-p["a"]*x*x+p["b"]*x-p["fixed"] for x in xs]
        constrained=raw>p["capacity"]
        return {"metrics":[["Point critique",_fmt(raw),"unités"],["Quantité réalisable",_fmt(q),"unités"],["Profit maximal réalisable",_fmt(profit),"€"],["Capacité",p["capacity"],"unités"]],
                "chart":{"type":"lines","series":[{"name":"Profit","x":xs,"y":ys}],"marker":{"x":q,"y":profit}},"decision":("Produire à la capacité maximale" if constrained else f"Produire environ {q:.0f} unités"),"explanation":("L'optimum théorique dépasse la capacité : la meilleure décision réalisable se situe à la borne." if constrained else "La dérivée passe de positive à négative au point critique : le profit y atteint son maximum."),"alert":profit<0}
    if case_id == "launch":
        budget=p["budget"]; marketing=budget*p["marketing_share"]/100; demand=p["base_demand"]*(1+p["growth"]/100)+p["ad_effect"]*math.sqrt(max(marketing,0)/1000)
        ca=p["fixed_a"]+p["unit_a"]*demand; cb=p["fixed_b"]+p["unit_b"]*demand; supplier="A" if ca<cb else "B"; supply=min(ca,cb)
        unit_supply=(p["unit_a"] if supplier=="A" else p["unit_b"]); launch_fixed=budget-marketing+(p["fixed_a"] if supplier=="A" else p["fixed_b"])
        margin=p["price"]-unit_supply; be=launch_fixed/margin if margin>0 else math.inf; profit=margin*demand-launch_fixed
        scenarios=[-.15,0,.15]; labels=["Prudent","Central","Dynamique"]; values=[margin*demand*(1+s)-launch_fixed for s in scenarios]
        return {"metrics":[["Demande prévue",_fmt(demand),"unités"],["Fournisseur retenu",supplier,""],["Point mort",math.ceil(be) if math.isfinite(be) else "Impossible","unités"],["Profit prévisionnel",_fmt(profit),"€"]],
                "chart":{"type":"bars","labels":labels,"values":values},"decision":("Lancer sous les hypothèses retenues" if profit>0 and demand>=be else "Revoir le projet avant lancement"),"explanation":f"Le scénario central prévoit {demand:.0f} unités pour un point mort de {math.ceil(be) if math.isfinite(be) else '—'}. Le fournisseur {supplier} minimise le coût d'approvisionnement à ce volume.","alert":profit<=0}
    raise ValueError("Cas inconnu")

def solve_json(case_id, params_json):
    return json.dumps(solve(case_id, json.loads(params_json)), ensure_ascii=False)
