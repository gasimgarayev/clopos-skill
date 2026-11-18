# Excel importu

## Əvvəl import növünü seç

| İş | Mənbə və fərq |
| --- | --- |
| İnqrediyent yaratmaq | `Name`, `Type=INGREDIENT`, `Category`, `Unit`; barkod varsa `Barcode` |
| Hazır məhsul/tex.karta yaratmaq | `Name`, `Price`, `Category`, `Station`, `Type=GOODS` və ya `DISH` |
| Tərkibli tex.karta/yarımfabrikat | Valideyn sətirindən sonra tərkib sətirləri; aşağıdakı qaydanı oxu |
| İnventar sayımına faktiki qalıq | Cari sayımın eksportunu götür; məhsul ID-si, adı və `Quantity` |
| Seçilmiş qiymət cədvəlini yeniləmək | Yalnız `product_id`, `price`; əsas məhsul importu deyil |

[Menyu sxemləri](https://az.help.clopos.com/az/article/menyu-excel-import-numuneleri-191rvtu/), [sayım sxemi](https://az.help.clopos.com/az/article/inventarlasdirmanin-import-edilmesi-tqw8sv/), [qiymət cədvəli sxemi](https://az.help.clopos.com/az/article/qiymet-cedvellerinin-excel-ile-import-edilmesi-1tlzp25/). Bu üç yazılı mənbə 2026-11-19 tarixində təkrar yoxlanıb. Başlıq və vahid kodları üçün cari UI-dən götürülmüş şablon üstün tutulur.

## Tərkibi pozmadan hazırlamaq

Əvvəl tex.karta üçün `DISH`, yarımfabrikat üçün `PREPARATION` valideynini, sonra əlaqəli tərkib sətirlərini yaz. Tərkib sətirlərini valideyndən ayıran ümumi əlifba sıralaması etmə. `GROSS` tərkib miqdarıdır; valideyn sətrində boş qalır. `Net Output` yarımfabrikatın partiya çıxışıdır. `Price` satış, `Cost Price` isə vahid maya dəyəridir. İnqrediyentə satış şöbəsi yazma. Mövcud kartın adını olduğu kimi saxla; adın fərqli yazılışı yeni kart yarada bilər. Məqalədə `g`/`gr` fərqi var; qram kodunu şablondan yoxla. [Tərkibli import](https://az.help.clopos.com/az/article/menyu-excel-import-numuneleri-191rvtu/)

## Fayl üzrə yoxlama

İmportdan əvvəl mənbə faylı saxla və yalnız tələb olunan sətirlərlə ayrıca import faylı hazırla. Barkod, SKU və identifikatorların başındakı sıfırları itirmə. Şablondakı rəqəm formatını yoxla; `1,250` kimi qeyri-müəyyən yazılışı təxminlə çevirmə. Faylın hazırlanması onun sistemə yüklənməsi demək deyil.

Qiymət cədvəlində ID-ləri cari məhsul eksportu ilə tutuşdur, dəyişməyəcək məhsulları importdan çıxar. Eyni ID iki dəfə görünürsə əvvəl ziddiyyəti həll et. Adı `product_id` yerinə yazma; bir cədvəlin qiymətlərini başqa filial/cədvələ tətbiq etmə. [Qiymət importu](https://az.help.clopos.com/az/article/qiymet-cedvellerinin-excel-ile-import-edilmesi-1tlzp25/)

Sayımda Addım 1 və Addım 2 fayllarını ayrı saxla; hər import bir vərəqdən ibarət olmalıdır. Məhsul ID-lərini qoruyub faktiki sayımı `Quantity` sahəsinə yaz. Boş qalıq naməlumdur, sıfır isə real sayım nəticəsi olmalıdır. Importdan sonra sayım hələ qaralamadırsa nəticənin ehtiyata tətbiq edildiyini demə. [Sayım importu](https://az.help.clopos.com/az/article/inventarlasdirmanin-import-edilmesi-tqw8sv/)

## Yüklədikdən sonra

Import pəncərəsinin xəta və qəbul sayını qeyd et, sətir sayı və dəyişmiş ID-ləri yenidən açıb tutuşdur. Qismən qəbul və ya bağlantı xətasında faylı bütöv yenidən göndərmə: hansı sətirlərin yarandığını əvvəl yoxla. Nəticəni “hazırlanıb”, “yüklənib” və “tətbiq edilib” statuslarından uyğun olanı ilə təqdim et. Canlı yoxlama mümkün olmayıbsa bunu bildir.
