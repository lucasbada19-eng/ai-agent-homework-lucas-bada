# Domácí úkol — AI Agenti (Lekce 1)

Tento projekt ukazuje základní AI agenta:
1. uživatel zadá dotaz (např. matematický výraz),
2. LLM (GPT) analyzuje dotaz,
3. pokud potřebuje výpočet, zavolá funkci (tool),
4. Python funkce výraz spočítá,
5. LLM vrátí finální odpověď.

---

## Jak projekt spustit (macOS / Linux)

### 1) Aktivovat prostředí
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export OPENAI_API_KEY="tvuj_klic"
python main.py
