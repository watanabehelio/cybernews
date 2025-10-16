KEYWORDS_IMPACT = {
    "ransomware": 9,
    "0-day": 9,
    "zero-day": 9,
    "exploit": 8,
    "breach": 8,
    "vazamento": 8,
    "dados sensíveis": 8,
    "sanção": 7,
    "multa": 7,
    "cve": 7,
    "cvss 9": 10,
    "cvss 10": 10,
}

KEYWORDS_PROB = {
    "exploit ativo": 9,
    "poc": 7,
    "proof of concept": 7,
    "em exploração": 8,
}

def score_and_severity(title: str, summary: str):
    txt = f"{title} {summary}".lower()
    imp = 3
    prob = 3
    for k, v in KEYWORDS_IMPACT.items():
        if k in txt:
            imp = max(imp, v)
    for k, v in KEYWORDS_PROB.items():
        if k in txt:
            prob = max(prob, v)
    score = round(imp * 0.6 + prob * 0.4, 1) * 10 / 10
    if score >= 7.5:
        sev = "Crítica"
    elif score >= 5.0:
        sev = "Alta"
    elif score >= 2.5:
        sev = "Média"
    else:
        sev = "Baixa"
    return float(score * 10), sev
