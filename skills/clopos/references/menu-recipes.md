# Menyu, tərkib və maya

## Kart növləri

| Növ | Fərqləndirilən əsas |
| --- | --- |
| Hazır məhsul | Alındığı formada satış; variant/vahid və alış qiyməti |
| İnqrediyent | Xammal; əsas vahid və qablaşdırma |
| Yarımfabrikat | Tərkib, partiya çıxışı, vahid və istehsalat |
| Tex.karta | Yemək/set; porsiya, tərkib, modifikator və şöbə |

[Növlərin fərqi](https://az.help.clopos.com/az/article/texkarta-ve-hazir-mehsul-ferqi-brgwk6/), [inqrediyent](https://az.help.clopos.com/az/article/inqrediyent-fztr1c/), [yarımfabrikat](https://az.help.clopos.com/az/article/yarimfabrikat-14szyjt/), [tex.karta](https://az.help.clopos.com/az/article/texkarta-elave-etmek-hqkcs0/)

## Qramaj və çıxış

Kartın hansı çıxışa görə yazıldığını müəyyənləşdir. Partiyanın tərkibini bir vahid üçün normallaşdırılmış tərkiblə qarışdırma. Nümunə: 2 kq çıxışa 0.6 kq xammal gedirsə, 1 kq çıxışa 0.3 kq düşür. 25 q = 0.025 kq, 80 ml = 0.080 l; ədəd↔kq üçün real çəki və ya təsdiqli qablaşdırma lazımdır. Qramajı “məntiqli görünsün” deyə dəyişmə.

## İnqrediyent əvəzlənməsi

Köhnə/yeni ID, vahid və növü yoxla. İstifadə yerlərini aç: tex.karta, yarımfabrikat və modifikatorlar ayrıca əhatə oluna bilər. Hər istifadədə ilkin brutto, vahid, itki/netto və çıxış əsasını qeyd et. Miqdar qorunmalıdırsa eyni vahiddə eyni rəqəmi, fərqli vahiddə yalnız sübutlu çevrilməni tətbiq et. Uyğunsuz vahidi dəqiqləşdirmədən davam etmə.

Yekunda ID siyahısını və qalan istifadə sayını yoxla. Köhnə kartın istifadəsi sıfır olsa belə silinməsi ayrıca tapşırıqdır. Tarixçə/qalıq/açıq çek asılılıqlarını dəyişmədən keçmə. [İstifadə yerləri](https://az.help.clopos.com/az/article/inqrediyent-fztr1c/), [silməyə maneələr](https://az.help.clopos.com/az/article/mehsulun-silinmemesinin-4-sebebi-z2n9t5/)

## Silinmə üsulu

Brutto anbardan çıxacaq miqdardır. Məhsulun öz ehtiyatı mövcuddursa əvvəl həmin ehtiyat azala bilər. Ehtiyat bitəndə **Tərkibdən sil** alt tərkibə keçir; **Hazır məhsuldan sil** isə məhsulun öz qalığını mənfiyə apara bilər. İç-içə kartlarda hər səviyyəni yoxla. [Tərkib və silinmə](https://az.help.clopos.com/az/article/terkiblerin-elave-edilmesi-7aiqd4/)

İnqrediyent/hazır məhsul məqalələri anbar hesablamasını dayandıran seçimin sonradan geri çevrilmədiyini və qalığı sıfırladığını bildirir; başqa məqalədə zidd ifadə var. Bu seçimi qalıq xətasını “düzəltmək” üçün istifadə etmə. Təsiri cari UI və dəstəklə yoxlanmadan dəyişmə. [Hazır məhsul](https://az.help.clopos.com/az/article/hazir-mehsul-elave-etmek-puae45/), [məhdudiyyət](known-gaps.md)

## Modifikator və set

Sabit tərkibi müştərinin seçdiyi variantdan ayır. Qrupun tək/çox seçim rejimi, qrup hədləri, variant hədləri, ilkin seçim, brutto və əlavə qiymət ayrı parametrlərdir. Ortaq qrupa düzəliş başqa məhsullara yayıla bilər; yalnız bir məhsula fərqli qrup lazımdırsa klon variantını qiymətləndir. Porsiyaya uyğunlaşma həm valideyn, həm seçilən məhsuldan asılıdır. Qrupun adını dəyişməyin yeni müstəqil qrup yaratdığını fərz etmə. [Modifikatorlar](https://az.help.clopos.com/az/article/modifikator-elave-edilmesi-15cdh3h/)

## Maya və import

Sıfır mayada növ, faktiki alış qiyməti, vahid, çıxış, tərkib zənciri və silinməni araşdır. Porsiya mayası üçün eyni əsasda miqdar × vahid maya hesabını tutuşdur. Mayanı düzəltmək adı ilə satış qiyməti və alış tarixçəsini dəyişmə.

Toplu importda cari bölmənin şablonunu əldə et. Ad/vahid yazılışı dublikat yarada bilər; ID dəstəklənirsə istifadə et. Başqa import növünün sütunlarını köçürmə. Rəsmi nümunələrdə vahid kodları da fərqlənir; canlı şablonu əsas götür. Faylı hazırlamaq importu icra etməkdən ayrıdır. [Import nümunələri](https://az.help.clopos.com/az/article/menyu-excel-import-numuneleri-191rvtu/)
