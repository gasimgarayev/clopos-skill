# Resept snapshot-ının yerli yoxlanması

`scripts/check_recipes.py` verilmiş kart siyahısında boş tərkibi, sıfır/naməlum miqdarı və çıxışı, sıfır/naməlum bildirilmiş mayanı, təkrarlanan ID və komponentləri, çatışmayan kart əlaqələrini və özünə qayıdan tərkib zəncirlərini axtarır. Hər tapıntının JSON yolu və sabit `code` sahəsi var. Əsas resept qaydaları üçün [menu-recipes.md](menu-recipes.md) oxu.

## Girişin hazırlanması

Bu, Clopos-un yerli eksport formatı deyil. Yalnız istifadəçinin verdiyi məlumatı və ya icazə daxilində oxunmuş kartları aşağıdakı JSON sxeminə köçür. Bir snapshot eyni hesab/filial və tarixə aid olmalıdır; başqa məkanın kartlarını ID-yə görə birləşdirmə. Faylı paylaşılacaq repoya əlavə etmə.

| Sahə | Mənası |
| --- | --- |
| `currency` | Açıq `AZN`; valyuta çevrilməsi aparılmır |
| `cards` | Ən azı bir kart, əlaqələrdə istifadə edilən alt kartlar daxil olmaqla |
| `id` | Mənbədəki kart ID-si, boşluqsuz mətn; ada görə uyğunlaşdırma aparılmır |
| `type` | `GOODS`, `INGREDIENT`, `DISH`, `PREPARATION` |
| `unit` | Kartın vahidi: `kg`, `g`, `l`, `ml`, `pcs` |
| `output_quantity` | DISH/PREPARATION tərkibinin aid olduğu çıxış miqdarı, kartın vahidində; məlum deyilsə `null` |
| `reported_unit_cost` | Kartın bir `unit`-i üçün mənbədə göstərilən maya; məlum deyilsə `null` |
| `contents` | Bu çıxış üçün tərkib sətirləri; GOODS/INGREDIENT üçün `[]`, çıxış isə `null` olmalıdır |
| `component_id` | Tərkib sətrinin aid olduğu alt kart ID-si |
| `gross_quantity` | Həmin çıxışa aid brutto miqdar; məlum deyilsə `null` |
| Sətirdə `unit` | Brutto miqdarın vahidi; alt kartın vahidindən fərqlənə bilər |

Ədədləri onluq mətn kimi yaz: `"0.025"`; JSON ədədi, vergül, eksponent və mənfi dəyər qəbul edilmir. Hər ədəd maksimum 18 tam və 6 kəsr rəqəmi daşıyır. Sxemdəki bütün sahələr tələb olunur; əlavə sahələr və təkrarlanan JSON açarları xəta qaytarır. Brutto yerinə netto və ya faiz yazma. Naməlumu `0` ilə doldurma.

`q`, `qr`, `gr`, `ədəd`, qutu və digər işarələri avtomatik dəyişmə. Mənbədəki mənanı təsdiqlə, sonra uyğun standart vahidi yaz; dəqiqləşməyibsə orijinal etiketi saxla, `unsupported_unit` alınacaq. `pcs` yalnız ədəd deməkdir, qablaşdırmanın çəkisini bildirmir.

## İcra

Repo kökündə sintetik nümunə:

```bash
python3 -B skills/clopos/scripts/check_recipes.py examples/recipes.json
```

Quraşdırılmış skilldə onun `scripts/check_recipes.py` faylını istifadəçinin snapshot faylı ilə çağır. Python standart kitabxanası kifayətdir. Proqram faylı dəyişmir və şəbəkəyə çıxmır.

`normalized_lines` hər sətrin brutto miqdarını komponent kartının vahidində göstərir: 300 g → 0.3 kg, 500 ml → 0.5 l. Hesablama `Decimal` ilədir. Kütlə↔həcm, ədəd↔çəki və qutu↔ədəd çevrilməsi aparılmır. Uyğunsuz və ya qeyri-müəyyən əlaqədə nəticə `null` qalır.

| Çıxış kodu | `status` | Şərhi |
| --- | --- | --- |
| 0 | `no_issues_found` | Yalnız verilmiş snapshot və dəstəklənən yoxlamalarda tapıntı yoxdur |
| 1 | `review_required` | `issues` siyahısını mənbə kartlarla tutuşdur |
| 2 | `invalid_input` | Sxem, ədəd və ya fayl xətasını düzəlt |

## Nəticəni şərh et

- `missing_component` yalnız alt kartın snapshot-da olmadığını bildirir. Onun Clopos-da silindiyini iddia etmə; çatışmayan kartı oxuyub yoxlamanı tamamla.
- `duplicate_card_id` olduqda həmin ID ilə bağlı heç bir kart üstün seçilmir. `duplicate_component` sətirləri birləşdirilmir; bu, mənbədə ayrıca istifadə ola bilər.
- `recipe_cycle` problemin yolunu `card_ids` ilə göstərir, məsələn `A → B → A`. Öz-özünə istinad da tapılır. Qaytarılan yollar bütün mümkün dövrlərin tam siyahısı deyil; göstərilən əlaqələri həll etdikdən sonra yenidən yoxla.
- Sıfır maya araşdırma siqnalıdır. Alış qiyməti, vergi, itki, çıxış və canlı maya üsulu burada hesablanmır; `reported_unit_cost` yalnız mənbədəki dəyərdir. Sintetik nümunədəki mayalar real qiymət və ya tam maya hesabı deyil.
- Reseptin çıxışı brutto miqdarların cəmi ilə müqayisə edilmir: müxtəlif vahidlər, itki və bişirmə təsiri ayrıca məlumat tələb edir. Yarımfabrikat zənciri xammal ehtiyacına qədər açılmır.
- `no_issues_found` canlı reseptin, silinmə rejiminin, faktiki qalığın və ya porsiya mayasının düzgünlüyünü təsdiqləmir. Yoxlayıcının tapıntısı avtomatik kart düzəlişi üçün icazə vermir; dəyişiklik istifadəçinin tapşırığına və mənbə məlumatına əsaslanmalıdır.
