import re

CATS = {
    "Ameaças & Campanhas": [r"phishing|botnet|ttp|campaign|campanha"],
    "Vulnerabilidades & Patches": [r"cve|cvss|vulnerab|patch|atualiza"],
    "Incidentes & Vazamentos": [r"vazamento|breach|incidente|ransomware|sequestro"],
    "Governança & Compliance": [r"lgpd|anpd|bacen|cvm|anbima|susep|anatel|anvisa|conformidade|compliance|regulat"],
    "IA & Segurança/Ética": [r"inteligência artificial|ia |\bai\b|generativa|ética|governança de ia"],
    "Privacidade & Proteção de Dados": [r"privacidade|proteção de dados|dados pessoais|dpo"],
    "Mercado & Carreira": [r"mercado|contrata|carreira|vaga|investimento|captação"],
    "Pesquisa & Boas Práticas": [r"pesquisa|paper|estudo|guia|boas práticas|best practice"],
}

order = list(CATS.keys())

def classify_category(title: str, summary: str) -> str:
    text = f"{title} {summary}".lower()
    for cat in order:
        for pat in CATS[cat]:
            if re.search(pat, text):
                return cat
    return "Pesquisa & Boas Práticas"
