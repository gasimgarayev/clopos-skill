# Qaimənin hesabını yerli yoxlamaq

Çoxsətirli qaimənin hesabını tutuşdurmaq üçün Python 3 ilə [check_purchase.py](../scripts/check_purchase.py) işlət. Bu, Clopos qaydalarını tətbiq edən inteqrasiya deyil; mənbədən çıxarılan rəqəmlərin ayrıca hesab yoxlamasıdır. Faylı oxuyur, JSON nəticəsini çıxarır; Clopos-a qoşulmur və mənbə faylı dəyişmir.

## Giriş

Məbləğ və miqdarları nöqtə ilə yazılmış mətn kimi ver (`"0.30"`). Naməlum rəqəm sahəsinə `null` yaz; özündən sıfır əlavə etmə. Valideyn obyektin bütün sahələri və sətirdə göstərilən sahələr məcburidir. Sətir ID-si və vahid adları boş olmayan mətn olmalıdır. Azərbaycan qəpiyi üçün sətir üzrə iki onluğa yarıyuxarı yuvarlaqlaşdırma yalnız açıq `rounding=half_up_2dp` seçimi ilə işləyir. Sənədin başqa yuvarlaqlaşdırma qaydası varsa bu köməkçini həmin qaydanın sübutu kimi istifadə etmə.

```json
{
  "currency": "AZN",
  "rounding": "half_up_2dp",
  "invoice_total": "54.00",
  "lines": [
    {
      "id": "1",
      "quantity": "3",
      "unit": "qutu",
      "unit_price": "18.00",
      "price_unit": "qutu",
      "discount_amount": "0.00",
      "tax_amount": "0.00",
      "line_total": "54.00"
    }
  ],
  "adjustments": []
}
```

Bu nümunə uydurmadır. Miqdar və qiymətin vahidi eyni olmalıdır; çevrilmə avtomatik aparılmır. `discount_amount` və `tax_amount` faiz deyil, mənbədəki sətir üzrə yekun məbləğlərdir. Qaimə üzrə ayrıca əlavə/endirim varsa `adjustments` siyahısına `{"label": "Qaimə endirimi", "amount": "-1.00"}` kimi daxil et. Sətirdə artıq nəzərə alınmış məbləği ikinci dəfə əlavə etmə. Yoxdursa boş siyahı saxla.

## İcra və nəticə

```bash
python3 -B /path/to/clopos/scripts/check_purchase.py /path/to/qaimə.json
```

Yolu quraşdırılmış skillin yerinə uyğunlaşdır. Aralıq JSON-u istifadəçi iş qovluğunda saxla, açıq repoya əlavə etmə.

- `arithmetic_match` / çıxış kodu `0`: verilmiş rəqəmlər seçilmiş hesab qaydasında uyğun gəlir.
- `review_required` / `1`: natamam məlumat, vahid fərqi, təkrarlanan sətir ID-si və ya cəm fərqi var; `issues` səbəbi göstərir.
- `invalid_input` / `2`: sxem/rəqəm formatı uyğun deyil. Vergüllü rəqəm, faiz, mənfi alış və qəpikdən kiçik yekun məbləğ avtomatik düzəldilmir.

Sətir hesabı: `quantity × unit_price − discount_amount + tax_amount`. Qaimə cəmi yoxlaması mənbədə yazılmış sətir cəmləri və ayrıca əlavələr əsasında aparılır; səhv sətir yekununun düzgün ümumi cəmin arxasında gizlənməməsi üçün hər iki nəticəni oxu. `arithmetic_match` məhsul ID/vahid uyğunluğunun tam yoxlanması, ödənişin təsdiqi və ya sənədi canlı tətbiq etmək icazəsi deyil.
