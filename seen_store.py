#daha once bildirilen maillerin id lerini saklar
import json  # ID'leri dosyaya yazıp okumak için
import os    # Dosya var mı diye kontrol etmek için


def load_seen(path="seen_ids.json"):
    # Dosya hiç yoksa (ilk çalıştırma) = boş küme döndür
    if not os.path.exists(path):
        return set()
    # Dosya varsa = içindeki listeyi oku ve kümeye (set) çevir
    with open(path, encoding="utf-8") as file:
        return set(json.load(file))


def save_seen(seen, path="seen_ids.json"):
    # JSON set saklayamaz = sıralı bir listeye çevirip dosyaya yaz
    with open(path, "w", encoding="utf-8") as file:
        json.dump(sorted(seen), file, indent=2)


# Sadece bu dosyayı çalıştırınca: kaydet-oku döngüsünü dene
if __name__ == "__main__":
    seen = load_seen()                       # Var olanları oku (ilk seferde boş)
    print("Before:", seen)
    seen.add("test-id-123")                  # Yeni bir ID ekle
    seen.add("test-id-123")                  # Aynısını tekrar ekle = set olduğu için iki kez eklenmez
    save_seen(seen)                          # Dosyaya kaydet
    print("After:", load_seen())             # Dosyadan tekrar oku
    print("Already seen?", "test-id-123" in load_seen())  #  True