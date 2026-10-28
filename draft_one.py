import asyncio
import httpx

OLLAMA_URL = 'http://localhost:11434/api/generate'
MODEL = 'DeepSeek-Coder-V2:latest'

# 10 сек на подключение, 300 сек на ожидание ответа
TIMEOUT = httpx.Timeout(connect=10.0, read=300.0, write=30.0, pool=10.0)

async def call_ollama(client: httpx.AsyncClient, prompt: str) -> str:
    """Универсальная функция для запроса к Ollama."""
    response = await client.post(
        OLLAMA_URL,
        json={
            'model': MODEL,
            'prompt': prompt,
            'stream': False,
        },
        timeout=TIMEOUT
    )
    response.raise_for_status()
    data = response.json()
    return data['response']  # полный текст, включая рассуждения

async def main(question: str):
    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        # Шаг 0: генерируем ответ
        print("=== Генерация ответа ===")
        current = await call_ollama(client, question)
        print(f"Ответ: {current}\n")

        # 10 проверок цепочкой
        for i in range(1, 11):
            print(f"=== Проверка {i} ===")
            prompt = f"Твоя задача спорить со мной: {current}"
            # prompt = f"{current}"
            current = await call_ollama(client, prompt)
            print(f"Результат проверки {i}: {current}\n")

        print("Цепочка из 10 проверок завершена.")
        print(f"Финальный результат: {current}")

if __name__ == "__main__":
    asyncio.run(main('Се се'))
