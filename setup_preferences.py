#kullaniciya soru sorup cevaplardan preference.json olusturur
import json  


def ask_words(question):
    # Kullanıcıya soruyu sor, cevabını al
    answer = input(question + " (separate with commas): ")
    # Cevabı virgüllerden böl, boşlukları temizle, küçük harfe çevir, boşları at
    words = [w.strip().lower() for w in answer.split(",") if w.strip()]
    return words


def main():
    print("Let's set up your email filter.\n")  # \n -> bir satır boşluk bırakır

    # 3 soruyu sor ve cevapları filters.py'nin beklediği isimlerle sözlüğe koy
    prefs = {
        "topic_words": ask_words("Which topics do you want to follow?"),
        "wanted_words": ask_words("Which words should trigger a notification?"),
        "blocked_words": ask_words("Which words should NEVER trigger a notification?"),
    }

    # Sözlüğü preferences.json dosyasına yaz
    # indent=2 -> dosya okunaklı olsun diye girintili yazar
    # ensure_ascii=False -> Türkçe karakterleri (ş, ı) bozmadan yazar
    with open("preferences.json", "w", encoding="utf-8") as file:
        json.dump(prefs, file, indent=2, ensure_ascii=False)

    print("\nSaved your preferences to preferences.json")


# Sadece bu dosyayı doğrudan çalıştırınca main() çalışsın
if __name__ == "__main__":
    main()