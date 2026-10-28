import asyncio
import time


def fib(n: int) -> int:
    """Итеративное вычисление числа Фибоначчи."""
    if n < 0:
        raise ValueError("n должно быть неотрицательным")
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


async def compute_fib(n: int) -> tuple[int, int, float]:
    """Возвращает (индекс, число, время вычисления в секундах)."""
    start = time.perf_counter()
    result = fib(n)
    elapsed = time.perf_counter() - start
    return n, result, elapsed


async def main(start: int, count: int = 100) -> None:
    # Замеряем общее время всего процесса
    total_start = time.perf_counter()

    tasks = []
    for i in range(count):
        # Каждое вычисление в своей задаче, все запускаются «параллельно»
        tasks.append(asyncio.create_task(compute_fib(start + i)))

    # Ждём завершения всех задач и собираем результаты
    results = await asyncio.gather(*tasks)

    # Печатаем каждый результат со временем выполнения задачи
    for index, value, elapsed in results:
        print(f"fib({index}) = {value}  (время: {elapsed:.6f} с)")

    total_elapsed = time.perf_counter() - total_start
    print(f"\nОбщее время всего процесса: {total_elapsed:.6f} с")


if __name__ == "__main__":
    asyncio.run(main(start=0, count=10000))
