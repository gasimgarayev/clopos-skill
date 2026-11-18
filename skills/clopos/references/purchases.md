# Tədarük, qaimə və tədarükçü

## Qaiməni hazırlamaq

Mənbə sənədin tarixini, nömrəsini, tədarükçüsünü, anbarını və cəmini çıxar. Hər sətir üçün orijinal adı, Clopos ID-sini, miqdar/vahidi, vahid qiymətini, endirim/vergi məlumatını və sətir cəmini tutuşdur. Sətir cəmini vahid qiyməti yerinə yazma. Məbləğləri qəpik dəqiqliyində yoxla; uyğunsuzluğu qiymət dəyişərək gizlətmə.

Çoxsətirli hesab yoxlaması üçün [yerli qaimə yoxlayıcısını](purchase-checker.md) istifadə edə bilərsən. Yalnız mənbədən təsdiqlənmiş rəqəmləri daxil et; bu köməkçinin uğurlu nəticəsi ödəniş və ya məhsul uyğunluğunu təsdiqləmir.

Qablaşdırmanın əsas vahidə çevrilməsini əvvəl yoxla. Sintetik nümunə: 3 qutu × 12 ədəd = 36 ədəd; qutu qiyməti 18 ₼ olduqda cəm 54 ₼, əsas vahid qiyməti 1.50 ₼ olar. UI-də qablaşdırma seçilibsə çevrilməni ikinci dəfə tətbiq etmə. Qutu tərkibi və ya ədəd çəkisi məlum deyilsə fərz etmə. [Qablaşdırma](https://az.help.clopos.com/az/article/qablasdirma-14juc4a/)

Eyni qaiməni tədarükçü, sənəd nömrəsi, əməliyyat tarixi, cəm və məhsullar üzrə mövcud qeydlərlə müqayisə et. Təkcə eyni məbləğ dublikatın sübutu deyil. Mövcud qaralamanı tapdıqda onu davam etdirmək ilə yenisini yaratmaq arasındakı fərqi nəzərə al.

## Tədarükü daxil etmək

**İnventar → Tədarüklər** bölməsindən başla. Forma tədarükçü, status, anbar, əməliyyat vaxtı, balans və qaimə identifikatorunu əhatə edir. Kreditlə alınmış, ödənməmiş alışda uyğun ödənilməmə seçimini saxla. Sətirlər və endirim/vergi dərəcələri sənədə əsaslanmalıdır. Ümumi faiz bütün sətirlərə yayıla bilər; istisna sətirlərin yekunlarını yenidən yoxla. Yadda saxlamanın təsirini seçilmiş statusla birlikdə qiymətləndir. Məqalə inventarlaşdırma tarixindən əvvələ tədarük məhdudiyyəti bildirir; blok yaranarsa faktiki tarixi saxtalaşdırma. [Yeni tədarük](https://az.help.clopos.com/az/article/yeni-tedaruk-yaratmaq-1tck5g1/), [ümumi endirim/vergi](https://az.help.clopos.com/az/article/yenilik-tedarukde-umumi-endirim-ve-vergi-1uqz4ru/)

Oxunmayan sətirlər üçün sual hazırla. Müstəqil, tam aydın sənədlərin icrasını başqa sənəddəki sual saxlamamalıdır. Bir qaiməni qismən təsdiqləmək tələb olunursa, tam sənədlə sonradan dublikat yaranmayacağı bölünmə və uzlaşdırma qaydasını əvvəl dəqiqləşdir. Qaralama qalığını aydın qeyd et.

## Ödənişi ayrıca yoxlamaq

Alışın təsdiqi onun pulunun ödənməsi demək deyil. Ödəniş də tapşırılıbsa verilən icazənin məbləğini, hesabını və tarixini mövcud ödəniş tarixçəsi ilə tutuşdur. Ümumi tədarükçü hesabına ödənişin konkret qaiməyə bağlandığını fərz etmə.

Rəsmi təlimatda tədarükçü bölməsindən qismən ödəniş, konkret tədarükün menyusundan isə qaiməni tam bağlayan ödəniş göstərilir. Formanı canlı yoxla, borc qalığından artıq məbləğ daxil etmə və sonra həm hesab hərəkətini, həm borcu tutuşdur. İki eyni ödəniş görünürsə mənbə sübutu və verilmiş düzəliş icazəsi olmadan birini silmə. [Tədarükçü borcu](https://az.help.clopos.com/az/article/tedarukcuye-borc-odemek-1sjnua0/)

## Alışın qaytarılması

İlkin tədarükün ID-sini tap. Qaytarılan məhsul, miqdar, anbar, qiymət və pulun qayıdacağı hesabı və ya borc düzəlişini ayır. Avtomatik son qiyməti razılaşdırılmış qaytarma qiyməti ilə yoxla. Qaytarma ID-sini ilkin tədarükün ID-si ilə birlikdə saxla. [Tədarükün qaytarılması](https://az.help.clopos.com/az/article/tedarukun-geri-qaytarilmasi-1mourri/)

Videolar: [tədarük](https://www.youtube.com/watch?v=qSJwV75v3u4), [qaytarma](https://www.youtube.com/watch?v=Lp3jgPC1L9Q). Avtomatik türk transkriptləri xətalıdır; dəqiq sahələr üçün yazılı mənbə və cari formanı əsas götür.

## Tamamlanmanı sübut etmək

| İstənilən nəticə | Nəyi yenidən yoxlamalısan |
| --- | --- |
| Qaralama hazırlanıb | Sənəd ID-si, qaralama statusu, sətirlər və yekun məbləğ |
| Tədarük tətbiq edilib | Təsdiq statusu və həmin sənədə aid məhsul hərəkəti |
| Ödəniş qeydə alınıb | Ödəniş ID-si, hesab, tarix, məbləğ və qalan borc |
| Qaytarma edilib | İlkin sənəd, qaytarma ID-si, miqdar və hesab/borc təsiri |

Bu cədvəl skillin icra yoxlamasıdır, Clopos-da yeni status adları yaratmır. Müstəqil tədarükçü balansı ilə konkret qaimənin bağlanmasını eyniləşdirmə. İcra nəticəsi hələ emaldadırsa “tamamlandı” yazma. Yekun hesabın uyğunluğu sətirlərin düzgün məhsula bağlandığını sübut etmir.
