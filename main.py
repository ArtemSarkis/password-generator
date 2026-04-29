import random
import string
import json
import os

HISTORY_FILE = "history.json"

def load_history():
    if not os.path.exists(HISTORY_FILE):
        return []
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_history(entry):
    history = load_history()
    history.append(entry)
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

def generate_password():
    print("\n=== ГЕНЕРАЦИЯ ПАРОЛЯ ===")
    length = input("Введите длину пароля (например: 12): ").strip()
    if not length.isdigit() or int(length) < 4:
        print("❌ Длина должна быть числом >= 4!")
        return
    length = int(length)
    use_special = input("Использовать спецсимволы? (да/нет): ").strip().lower()
    chars = string.ascii_letters + string.digits
    if use_special == "да":
        chars += string.punctuation
    password = ''.join(random.choice(chars) for _ in range(length))
    print(f"✅ Пароль успешно сгенерирован: {password}")
    print(f"   Длина: {length} | Спецсимволы: {'да' if use_special == 'да' else 'нет'}")
    save_history({"type": "password", "value": password, "length": length})

def generate_key():
    print("\n=== ГЕНЕРАЦИЯ КЛЮЧА ===")
    bits = input("Введите длину ключа в битах (128 / 256): ").strip()
    if bits not in ("128", "256"):
        print("❌ Допустимые значения: 128 или 256!")
        return
    key = ''.join(random.choice('0123456789abcdef') for _ in range(int(bits) // 4))
    print(f"✅ Ключ сгенерирован: {key}")
    save_history({"type": "key", "value": key, "bits": int(bits)})

def check_strength():
    print("\n=== ПРОВЕРКА НАДЁЖНОСТИ ===")
    password = input("Введите пароль для проверки: ").strip()
    if not password:
        print("❌ Пароль не может быть пустым!")
        return
    score = 0
    if len(password) >= 8: score += 1
    if len(password) >= 12: score += 1
    if any(c.isupper() for c in password): score += 1
    if any(c.islower() for c in password): score += 1
    if any(c.isdigit() for c in password): score += 1
    if any(c in string.punctuation for c in password): score += 1
    levels = {6: "🟢 Очень надёжный", 5: "🟡 Надёжный", 4: "🟠 Средний", 3: "🔴 Слабый"}
    level = levels.get(score, "🔴 Очень слабый")
    print(f"Результат: {level} (счёт: {score}/6)")

def view_history():
    print("\n=== ИСТОРИЯ ГЕНЕРАЦИЙ ===")
    history = load_history()
    if not history:
        print("История пуста.")
        return
    print(f"Всего записей: {len(history)}")
    print("-" * 30)
    for i, entry in enumerate(history, 1):
        if entry["type"] == "password":
            print(f"  {i}. Пароль | Длина: {entry['length']} | {entry['value']}")
        elif entry["type"] == "key":
            print(f"  {i}. Ключ    | Бит: {entry['bits']} | {entry['value']}")
    print("-" * 30)

def main():
    print("\n╔══════════════════════════════╗")
    print("║   ГЕНЕРАТОР ПАРОЛЕЙ И КЛЮЧЕЙ  ║")
    print("╚══════════════════════════════╝")
    while True:
        print("\nГлавное меню:")
        print("  1 — Сгенерировать пароль")
        print("  2 — Сгенерировать ключ")
        print("  3 — Проверить надёжность пароля")
        print("  4 — Просмотреть историю")
        print("  0 — Выход")
        choice = input("\nВаш выбор: ").strip()
        if choice == "1": generate_password()
        elif choice == "2": generate_key()
        elif choice == "3": check_strength()
        elif choice == "4": view_history()
        elif choice == "0":
            print("До свидания!")
            break
        else:
            print("❌ Неверный выбор!")

if __name__ == "__main__":
    main()
