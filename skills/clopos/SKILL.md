---
name: clopos
description: Clopos POS və arxa paneldə qaimə/tədarük, anbar, inventarlaşdırma, texniki kart, yarımfabrikat, maliyyə, satış hesabatları, terminal və QR menyu tapşırıqlarını mənbəli qaydalarla icra et. Clopos daxilində iş və ya Clopos haqqında konkret izah tələb olunduqda istifadə et.
---

# Clopos

İstifadəçinin Clopos tapşırığını mövcud alətlərlə yerinə yetir. Yazılı izah istənirsə izah et; canlı əməliyyat istənirsə hesaba çıxışı yoxla və verilmiş səlahiyyət daxilində işi tamamla. İstifadəçinin dilində danış, interfeysdəki sahə adlarını dəqiq saxla.

## Tapşırığı yönəlt

Yalnız iş üçün lazım olan istinadı oxu:

| Tapşırıq | İstinad |
| --- | --- |
| Qaimə, alış, tədarükçü borcu, alışın qaytarılması | [purchases.md](references/purchases.md) |
| Qalıq, sayım, transfer, istehsalat, tullantı | [inventory.md](references/inventory.md) |
| Məhsul, inqrediyent, resept, tex.karta, yarımfabrikat, modifikator | [menu-recipes.md](references/menu-recipes.md) |
| Maliyyə hesabları, kateqoriyalar, əməkhaqqı, ödəniş əlaqələri | [finance.md](references/finance.md) |
| Satış, maya, şöbə, filial, dövr və eksport üzrə hesabat | [reports.md](references/reports.md) |
| Çek, bölünmüş ödəniş, geri qaytarma, müştəri balansı, stop-list | [terminal-sales.md](references/terminal-sales.md) |
| İcazələr, zal/masa, QR menyu, qiymət cədvəli, printer, e-kassa, Waiter | [setup-modules.md](references/setup-modules.md) |
| Video axtarışı, təlimin mənşəyi, mənbə əhatəsi | [source-guide.md](references/source-guide.md) və [video-catalog.md](references/video-catalog.md) |
| Mənbələr ziddiyyətlidir və ya təlim çatışmır | [known-gaps.md](references/known-gaps.md) |

## İcranın əsasları

1. Cari brend/filialı, tarix intervalını və işin aid olduğu anbarı və ya maliyyə hesabını müəyyənləşdir. Açıq sessiya və söhbət bunları artıq dəqiqləşdiribsə yenidən soruşma. Başqa restorandakı qaydanı avtomatik tətbiq etmə.
2. Mövcud Clopos konnektoru işi görürsə ondan istifadə et; əks halda dəstəklənən brauzer/kompüter alətlərini işlət. Çıxış yoxdursa onu açıq bildir və hazırlanmış nəticəni təqdim et. Mövcud olmayan API, giriş, sahə və ya düymə uydurma.
3. Məhsulu yalnız ada görə uyğunlaşdırma: ID, növ, vahid, qablaşdırma və tərkibdəki rolunu tutuşdur. Oxşar adlar fərqli kartlar ola bilər. Miqdarı, qramajı, alış qiymətini və ödənilmə statusunu təxminlə doldurma.
4. Məlumatları hazırlamaq, qaralama saxlamaq, sənədi təsdiqləmək və ödəniş yazmaq ayrı nəticələrdir. İstifadəçinin artıq verdiyi icazəni təkrar istəmə; qalan naməlum məlumat və ya əhatədən kənar nəticə üçün yalnız konkret çatışmazlığı soruş. İcazəsiz maliyyə hərəkətini əlavə etmə.
5. Yazmadan əvvəl mövcud sənədləri və əməliyyatları yoxla. Cavab gecikəndə və ya bağlantı kəsiləndə yenidən yaratmağa keçmə: əvvəl əvvəlki cəhdin nəticəsini ID/tarix/məbləğ/sətirlər üzrə tap. Mövcud qeydi tapmaq mümkün deyilsə təkrar cəhdə qədər qeyri-müəyyənliyi həll et.
6. Dəyişən məlumatı canlı mənbədən yoxla. İstinadlardakı yollar başlanğıc bələdçisidir; cari UI və səlahiyyətlər fərqlənə bilər. Köhnə videodakı qiyməti, portu, IP-ni və nümunə balansını real hesaba köçürmə.
7. Yadda saxladıqdan sonra sənədi yenidən aç və soruşulan nəticəni yoxla: status, sətirlər, cəm, tərkib, qalıq və ya hesab hərəkəti. Sadəcə düyməyə basmağı tamamlanma hesab etmə. Toplu işdə icra olunan, gözləyən və xətalı elementləri ayrıca say.

## Nəticəni təqdim et

Nə edildiyini qısa yaz; uyğun sənəd/məhsul ID-lərini, statusu, say və məbləği göstər. Qalan qeyri-müəyyənliyi və nəyin hələ təsdiqlənmədiyini bildir. Nümunə:

> 4 tədarük yoxlandı: 3-ü təsdiqləndi, 1-i vahidi dəqiqləşənədək qaralamadır. Sənəd ID-ləri: …

Bu skill şəxsi hesab məlumatı saxlamır. İstifadəçi açıq şəkildə istəmədikcə məkan adları, əməkdaşlar, qaimələr, giriş məlumatları və canlı eksportlar paylaşılacaq skill paketinə daxil edilmir.
