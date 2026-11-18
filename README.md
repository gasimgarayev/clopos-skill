# Clopos Skill

Clopos POS və arxa paneldə gündəlik əməliyyatlar üçün Azərbaycan dilində SI skill-i. Qaimə, anbar, resept, maliyyə, hesabat, terminal və modul işlərini mövzuya uyğun istinadlarla dəstəkləyir.

## Quraşdırma

Reponu endirib quraşdırın:

```bash
git clone https://github.com/gasimgarayev/clopos-skill.git
cd clopos-skill
python3 scripts/validate.py
python3 scripts/install.py
```

Quraşdırıcı yalnız `skills/clopos` qovluğunu `${CODEX_HOME}/skills/clopos` ünvanına, `CODEX_HOME` yoxdursa `~/.codex/skills/clopos` ünvanına kopyalayır. Standart rejimdə mövcud fərqli skillin üzərinə yazmır. Artıq eyni nüsxə varsa dəyişiklik etmir.

Alternativ olaraq `skills/clopos` qovluğunu öz skill qovluğunuza əl ilə köçürə bilərsiniz. Quraşdırmanın uğuru skill fayllarının yerləşdirilməsidir; cari söhbətin onu dərhal yüklədiyi ayrıca yoxlanmalıdır.

### Mövcud versiyanı yeniləmək

Repo təmiz vəziyyətdədirsə son dəyişiklikləri götürüb əvvəl baxış keçirin:

```bash
git pull --ff-only
python3 -B scripts/install.py --update --dry-run
python3 -B scripts/install.py --update
```

`--update` açıq şəkildə yeni nüsxəyə keçidi seçir. Quraşdırıcı əvvəl yeni faylları ayrıca yoxlayır, köhnə skillin bütün fayllarını və yerli redaktələrini gizli ehtiyat qovluğunda saxlayır, sonra yeni nüsxəyə keçir. Ehtiyat yolu nəticədə göstərilir. Yeni nüsxəni yerinə köçürmək alınmasa əvvəlki qovluq bərpa edilir. Yerli redaktələr avtomatik birləşdirilmir; ehtiyat nüsxədə qalır.

## İstifadə

Normal skill seçimi aktivdir. Açıq çağırış nümunələri:

```text
$clopos Bu qaimənin sətirlərini uyğun məhsullarla tutuşdur və qaralama hazırla.
$clopos Bu yarımfabrikatın çıxışını və porsiya mayasını yoxla.
$clopos Seçilmiş dövr üçün şöbə satışlarını ümumi cəmlə uzlaşdır.
$clopos Bu məhsulun QR menyuda niyə görünmədiyini yoxla.
$clopos Bu qiymət cədvəli importunu ID-lər və sütunlar üzrə yoxla.
```

Hesab/filial, tarix, vahid və ödəniş məlumatı mövcud kontekstdən götürülür; çatışmayan hissə təxmin edilmir. Sənədin hazırlanması, təsdiqi və ödənişi ayrı nəticələr kimi izlənir. Əvvəl verilmiş icazə təkrar soruşulmur.

## Quruluş

```text
skills/clopos/
  SKILL.md                   # Qısa giriş, marşrutlama və icra qaydaları
  agents/openai.yaml         # Skill siyahısında görünən məlumat
  scripts/check_purchase.py  # Qaimə hesabının yerli yoxlanması
  references/                # İş istiqamətləri, Excel importu və mənbələr
scripts/
  validate.py                # Paket bütövlüyü və mənbə əhatəsi
  install.py                 # Quraşdırma və ehtiyat nüsxəli yeniləmə
evals/cases.json              # Sintetik davranış yoxlama ssenariləri
.github/workflows/validate.yml
```

## Yoxlama və töhfə

Uydurma qaimə üzərində hesab yoxlamasını sınamaq üçün:

```bash
python3 -B skills/clopos/scripts/check_purchase.py examples/purchase.json
```

Köməkçi rəqəmləri `Decimal` ilə hesablayır, naməlum sahəni və vahid fərqini bildirir. Mənbə faylı dəyişmir, Clopos-a qoşulmur, məhsul və ödəniş statusunu yoxlamır. [Giriş sxemi və çıxış kodları](skills/clopos/references/purchase-checker.md)

`python3 scripts/validate.py` daxili keçidləri, skill metadatasını, mənbə reyestrinin saylarını və ssenari quruluşunu yoxlayır. Bu yoxlama Clopos-da işin düzgün icra edildiyini sübut etmir. [Davranış ssenariləri](evals/README.md) ayrıca, canlı dəyişiklik etmədən işlədilməlidir.

Yoxlayıcıların və quraşdırıcının avtomatik sınaqları: `python3 -B -m unittest discover -s tests -v`.

Məhsul qaydası dəyişəndə rəsmi URL-ni, tarixini və sübut səviyyəsini qeyd edin. Mətnin əldə edilməsini vizual yoxlama kimi işarələməyin. Mənbə tamlığına yeni sübut olmadan iddia əlavə etməyin.

Kod və növbəti təkmilləşdirmələr üçün [GitHub reposundan](https://github.com/gasimgarayev/clopos-skill) istifadə edin. Xam tədqiqat, canlı hesab eksportları, şifrələr və tam transkriptlər bu paketə daxil deyil.

## Lisenziya

Bu layihənin orijinal kodu və təlimatları [MIT](LICENSE) lisenziyasındadır. Clopos adı, videoları, ekran görüntüləri və rəsmi məqalələr aid olduqları hüquq sahiblərində qalır; bu lisenziya həmin materiallara şamil edilmir. [Mənbələr](skills/clopos/references/sources.json)

---

An Azerbaijani-language AI skill for Clopos POS workflows, with traceable public sources and explicit evidence gaps. No credentials, private restaurant data, or full third-party transcripts are distributed. This is an independent project, not an official Clopos integration.
