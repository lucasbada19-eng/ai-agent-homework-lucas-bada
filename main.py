"""
AI Agents - Praktické cvičení (Lekce 1)

Tento skript:
1) zavolá LLM (OpenAI),
2) LLM navrhne použití nástroje (funkce compute),
3) skript funkci provede a výsledek vrátí do LLM.
"""

import os
import json
import ast
import operator as op
from openai import OpenAI

# -----------------------------------
# Bezpečný kalkulátor (safe eval)
# -----------------------------------

ALLOWED_OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
}

def safe_eval(expr: str):
    """Bezpečně vyhodnotí matematický výraz."""
    node = ast.parse(expr, mode='eval')

    def _eval(n):
        if isinstance(n, ast.Expression):
            return _eval(n.body)
        if isinstance(n, ast.BinOp):
            return ALLOWED_OPERATORS[type(n.op)](_eval(n.left), _eval(n.right))
        if isinstance(n, ast.Constant):
            return n.value
        raise ValueError("Nepovolený výraz")

    return _eval(node)

# -----------------------------------
# Náš nástroj (funkce pro LLM)
# -----------------------------------

def compute_tool(expression: str):
    try:
        result = safe_eval(expression)
        return str(result)
    except Exception as e:
        return f"ERROR: {e}"

# -----------------------------------
# LLM LOGIKA
# -----------------------------------

def run():
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    user_question = input("Zadej otázku: ")

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Když je třeba něco spočítat, použij funkci compute."},
            {"role": "user", "content": user_question}
        ],
        functions=[
            {
                "name": "compute",
                "description": "Bezpečný aritmetický kalkulátor",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "expression": {"type": "string"}
                    },
                    "required": ["expression"]
                }
            }
        ],
        function_call="auto"
    )

    msg = response.choices[0].message

    # LLM požádal o použití funkce?
    if msg.function_call:
        args = json.loads(msg.function_call.arguments)
        result = compute_tool(args["expression"])

        followup = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Asistent využívá funkci compute."},
                {"role": "user", "content": user_question},
                msg,
                {"role": "function", "name": "compute", "content": result}
            ]
        )
        print("Finální odpověď LLM:")
        print(followup.choices[0].message.content)
    else:
        print("LLM odpověděl bez funkce:")
        print(msg.content)

if __name__ ==
