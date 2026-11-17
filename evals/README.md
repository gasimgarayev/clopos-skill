# Davranış yoxlaması

[cases.json](cases.json) sintetik məlumatlarla real qərar nöqtələrini yoxlayır. Bunlar canlı Clopos hesabından alınmayıb.

Hər ssenaridə skillin girişini və yalnız lazım olan istinadını oxuyun. `request` və `state` əsasında cavab və ya icra planı hazırlayın; sonra `pass_criteria` ilə qiymətləndirin. Canlı hesaba giriş, sənəd yaratmaq, pul hərəkəti və cihaz dəyişikliyi etməyin. Alət tələb olunan yerdə hansı oxunuşun və hansı yoxlamanın lazım olduğunu göstərin.

Nəticəni ssenari üzrə keçdi/qaldı və qısa sübutla qeyd edin. Gözlənilən nəticələrə sözbəsöz uyğunluq tələb olunmur; qərarın mənası və say hesabı əsasdır. `scripts/validate.py` yalnız ssenarilərin quruluşunu yoxlayır, onları agentlə icra etmir. Bu buraxılışda ayrıca müstəqil agent davranış qiymətləndirməsi aparılmayıb.
