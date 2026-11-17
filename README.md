# Clopos Skill

Clopos POS və arxa paneldə gündəlik əməliyyatlar üçün Azərbaycan dilində Codex skill-i. Qaimə, anbar, resept, maliyyə, hesabat, terminal və modul işlərini mövzuya uyğun istinadlarla dəstəkləyir.

**Müstəqil layihədir. Clopos tərəfindən hazırlanmış və ya təsdiqlənmiş rəsmi inteqrasiya deyil.** Skill Clopos-a giriş vermir; hesabda işləmək üçün ayrıca mövcud sessiya və uyğun alətlər lazımdır.

## Bu buraxılış

`0.1.0` — mənbəli ilkin buraxılış, 17 noyabr 2026.

| Mənbə | Əhatə |
| --- | ---: |
| Göndərilmiş pleylistlər | 13 |
| Pleylistlərdə fərqli videolar | 45 |
| Kanalın Videos + Shorts bölmələri ilə ümumi siyahı | 56 |
| Əldə edilmiş və nəzərdən keçirilmiş transkriptlər | 40 |
| Transkripti əldə edilməyən videolar | 16 |
| Mətni əldə edilmiş rəsmi yardım məqalələri | 114 |
| İş qaydalarında istinad edilən yardım məqalələri | 60 |

Videoların hamısına baxıldığı iddia edilmir. Bir sıra avtomatik subtitrlər ciddi xətalıdır və bəziləri yalnız musiqini göstərir. Cari iş qaydaları aydın transkript hissələri və uyğun rəsmi yazılı təlimatlara söykənir. Canlı Clopos hesabında əməliyyat sınağı aparılmayıb. [Mənbə qaydası](skills/clopos/references/source-guide.md), [video kataloqu](skills/clopos/references/video-catalog.md), [məhdudiyyətlər](skills/clopos/references/known-gaps.md)

## Quraşdırma

Reponu endirib quraşdırın:

```bash
git clone https://github.com/gasimgarayev/clopos-skill.git
cd clopos-skill
python3 scripts/validate.py
python3 scripts/install.py
```

Quraşdırıcı yalnız `skills/clopos` qovluğunu `${CODEX_HOME}/skills/clopos` ünvanına, `CODEX_HOME` yoxdursa `~/.codex/skills/clopos` ünvanına kopyalayır. Mövcud fərqli skillin üzərinə yazmır; yeniləmək üçün əvvəl fərqləri nəzərdən keçirmək lazımdır. Artıq eyni nüsxə varsa dəyişiklik etmir.

Alternativ olaraq `skills/clopos` qovluğunu öz skill qovluğunuza əl ilə köçürə bilərsiniz. Quraşdırmanın uğuru skill fayllarının yerləşdirilməsidir; cari söhbətin onu dərhal yüklədiyi ayrıca yoxlanmalıdır.

## İstifadə

Normal skill seçimi aktivdir. Açıq çağırış nümunələri:

```text
$clopos Bu qaimənin sətirlərini uyğun məhsullarla tutuşdur və qaralama hazırla.
$clopos Bu yarımfabrikatın çıxışını və porsiya mayasını yoxla.
$clopos Seçilmiş dövr üçün şöbə satışlarını ümumi cəmlə uzlaşdır.
$clopos Bu məhsulun QR menyuda niyə görünmədiyini yoxla.
```

Hesab/filial, tarix, vahid və ödəniş məlumatı mövcud kontekstdən götürülür; çatışmayan hissə təxmin edilmir. Sənədin hazırlanması, təsdiqi və ödənişi ayrı nəticələr kimi izlənir. Əvvəl verilmiş icazə təkrar soruşulmur.

## Quruluş

```text
skills/clopos/
  SKILL.md                   # Qısa giriş, marşrutlama və icra qaydaları
  agents/openai.yaml         # Skill siyahısında görünən məlumat
  references/                # 7 iş istiqaməti, mənbələr və məhdudiyyətlər
scripts/
  validate.py                # Paket bütövlüyü və mənbə əhatəsi
  install.py                 # Üzərinə yazmadan yerli quraşdırma
evals/cases.json              # Sintetik davranış yoxlama ssenariləri
.github/workflows/validate.yml
```

## Yoxlama və töhfə

`python3 scripts/validate.py` daxili keçidləri, skill metadatasını, mənbə reyestrinin saylarını və ssenari quruluşunu yoxlayır. Bu yoxlama Clopos-da işin düzgün icra edildiyini sübut etmir. [Davranış ssenariləri](evals/README.md) ayrıca, canlı dəyişiklik etmədən işlədilməlidir.

Məhsul qaydası dəyişəndə rəsmi URL-ni, tarixini və sübut səviyyəsini qeyd edin. Mətnin əldə edilməsini vizual yoxlama kimi işarələməyin. Mənbə tamlığına yeni sübut olmadan iddia əlavə etməyin.

Kod və növbəti təkmilləşdirmələr üçün [GitHub reposundan](https://github.com/gasimgarayev/clopos-skill) istifadə edin. Xam tədqiqat, canlı hesab eksportları, şifrələr və tam transkriptlər bu paketə daxil deyil.

## Lisenziya

Bu layihənin orijinal kodu və təlimatları [MIT](LICENSE) lisenziyasındadır. Clopos adı, videoları, ekran görüntüləri və rəsmi məqalələr aid olduqları hüquq sahiblərində qalır; bu lisenziya həmin materiallara şamil edilmir. [Mənbələr](skills/clopos/references/sources.json)

---

An Azerbaijani-language Codex skill for Clopos POS workflows, with traceable public sources and explicit evidence gaps. No credentials, private restaurant data, or full third-party transcripts are distributed. This is an independent project, not an official Clopos integration.
