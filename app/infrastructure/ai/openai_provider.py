from openai import OpenAI
from app.domain.ports.ai_provider import AIProvider
from app.config.settings import settings

def _build_prompt(tide_type: str, level: float, time: str) -> str:
    return (
        "Gere UMA única frase curta em português brasileiro.\n"
        "A frase deve ter no máximo 15 palavras.\n"
        "A frase DEVE seguir EXATAMENTE este formato:\n\n"
        "Maré alta: <nível> metros às <horário>, <frase curta>.\n"
        "ou\n"
        "Maré baixa: <nível> metros às <horário>, <frase curta>.\n\n"
        "Não use emojis.\n"
        "Não use exclamações.\n"
        "Tom informal e levemente brincalhão.\n\n"
        "Informações obrigatórias:\n"
        f"- Tipo da maré: {tide_type}\n"
        f"- Nível da maré: {level} metros\n"
        f"- Horário: {time}\n\n"
        "Exemplos de tamanho e estilo:\n"
        "Maré alta: 3 metros às 14:00, melhor evitar o banho.\n"
        "Maré baixa: 0.2 metros às 18:00, mar calmo, dá pra relaxar.\n"
    )


class OpenAIProvider(AIProvider):

    def __init__(self, model: str = "gpt-4o-mini"):
        self.client = OpenAI(api_key=settings.openai_api_key)
        self.model = model

    def generate_tide_message(
        self,
        tide_type: str,
        level: float,
        time: str
    ) -> str:
        prompt = _build_prompt(tide_type, level, time)

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "Você é um assistente criativo e bem-humorado."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.9,
            max_tokens=60
        )

        return response.choices[0].message.content.strip()

