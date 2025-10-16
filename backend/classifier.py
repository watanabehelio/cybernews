# backend/classifier.py
import re

CATEGORIES = [
    "LGPD/Privacidade",
    "Vazamento de Dados",
    "Ataques Cibernéticos",
    "Ransomware",
    "Phishing",
    "Vulnerabilidades (CVE)",
    "IA/IA Generativa",
    "Compliance/Regulação",
    "Cibersegurança (Geral)"
]

KEYWORDS = {
    "LGPD/Privacidade": [
        r"\bLGPD\b", r"\bANPD\b", r"prote(c|ç)[aã]o de dados", r"privacidade",
        r"DPO", r"encarregado", r"base legal", r"relat[óo]rio de impacto|DPIA",
        r"consentimento", r"titular(es)? de dados", r"direito(s)? do titular"
    ],
    "Vazamento de Dados": [
        r"vazamento", r"exposi[cç][aã]o de dados", r"data leak", r"data breach",
        r"dump", r"leak(ed)?", r"pastebin", r"credenciais vazadas"
    ],
    "Ataques Cibernéticos": [
        r"ataque(s)? cibern[eé]tico(s)?", r"intrus(ão|ao)", r"exploit", r"comprometimento",
        r"DDoS", r"defacement", r"backdoor", r"web shell", r"lateral movement"
    ],
    "Ransomware": [
        r"ransomware", r"cripto(malware)?", r"double extortion", r"lockbit|blackcat|cl0p|play|royal"
    ],
    "Phishing": [
        r"phishing", r"spear[- ]?phishing", r"smishing", r"vishing", r"fraude por e-mail",
        r"golpe(s)?", r"spoofing", r"credenciais"
    ],
    "Vulnerabilidades (CVE)": [
        r"\bCVE-\d{4}-\d{4,7}\b", r"zero[- ]day", r"vulnerabilidade(s)?", r"patch|corre[cç][aã]o",
        r"eleva[cç][aã]o de privil[eé]gio"
    ],
    "IA/IA Generativa": [
        r"\bIA\b|\bI\.A\.\b|\bintelig[eê]ncia artificial\b", r"IA generativa|GenAI",
        r"modelos (fundacionais|fundacionais)|LLM|GPT|transformer", r"alucina[cç][oõ]es"
    ],
    "Compliance/Regulação": [
        r"compliance", r"conformidade", r"regula[cç][aã]o", r"cvm|bacen|anbima|susep|anatel|anvisa",
        r"pol[ií]tica(s)?", r"controles internos", r"auditoria"
    ],
    "Cibersegurança (Geral)": [
        r"seguran[çc]a da informa[cç][aã]o", r"ciberseguran[çc]a", r"gest[aã]o de riscos",
        r"iso\s*2700\d", r"NIST", r"conting[eê]ncia", r"resposta a incidentes|CSIRT|CERT"
    ],
}

def _norm(s: str) -> str:
    return (s or "").lower()

def classify_category(title: str, summary: str) -> str:
    text = _norm(f"{title} {summary}")
    for cat, patterns in KEYWORDS.items():
        for pat in patterns:
            if re.search(pat, text, flags=re.IGNORECASE):
                return cat
    # fallback
    return "Cibersegurança (Geral)"
