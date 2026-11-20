# Shbeeb Downloader — Public update notices (no APK distribution)

This **public** repository is reserved for the owner-approved read-only announcement/update pages of Shbeeb Downloader.

## Current status: preparation only

- The repository exists and is public.
- GitHub Pages must be configured and HTTPS verified separately.
- **No `beta/android.json` release feed is published yet.** It must be generated only from a real signed Beta 31+ APK that passes the private verification workflow.
- **No APK, signing key, secrets, tokens or private GitHub Actions artifacts** may be committed here.
- There is no live Android Push service.

## Intended URLs (after Pages activation)

- Overview: `https://mustafashbeeb.github.io/Shbeeb-Downloader-Releases/`
- Beta information: `https://mustafashbeeb.github.io/Shbeeb-Downloader-Releases/beta/`
- **Future**, only after signed Beta 31 review: `https://mustafashbeeb.github.io/Shbeeb-Downloader-Releases/beta/android.json`

## Safe publishing checklist

1. Review the signed, privately stored Beta 31 build and its signing certificate against Beta 30.
2. Generate `beta/android.json` with the verified private BETA workflow in **notification-only mode**.
3. Confirm the JSON names the correct Beta package and higher version, and neither JSON nor HTML exposes an APK URL.
4. Publish reviewed *metadata only* after an explicit approval; verify HTTPS, content-type and phone behavior.
5. Do not distribute the APK publicly or to third parties until the GPLv3/third-party licensing gate is resolved.

The future owner's general messages must use a **separate** verified file/schema (e.g. `announcements.json`), with a protected publishing process, no browser-side GitHub token, and no dependency on the APK update feed. Push notifications are deferred to later versions.


## Owner-authored in-app messages — preview and controlled publication

- [معاينة الرسالة العربية](admin/preview.html): محرر محلي للعنوان والنص والجمهور والمدة؛ **صفحة عامة للمعاينة فقط، لا تقوم بالنشر ولا تحفظ أسراراً**. تتطلب عرضها من موقع Pages المنشور بعد تفعيله.
- [نشر الرسالة أو إيقافها بحساب المالك فقط](.github/workflows/owner-announcements.yml): workflow يدوي مع اختيارات `preview` / `publish` / `disable` وكلمة تأكيد صريحة `PUBLISH` أو `DISABLE`؛ يكتب `announcements.json` فقط، ولا يلمس ملفات تحديث APK.
- [اختبارات أمان النشر](tests/test_owner_announcements.py) و[فحص CI](.github/workflows/validate-owner-announcements.yml). لم يتم إثبات اختبار الهاتف، ولم يتم تشغيل Push. يجب مراجعة حالة اختبارات CI الحية قبل النشر.
- `announcements.json` **غير منشور حالياً**؛ لا يُنشأ قبل تحديد المالك نص الرسالة وإجازة نشرها. المستخدِمون الحاليون على Beta 30 لا يستقبلون رسائل الإدارة قبل تثبيت إصدار جديد يحوي المستقبِل.
- يجب تفعيل GitHub Pages عبر `Settings → Pages → Build and deployment → Deploy from a branch → main → / (root)`، ثم تأكيد HTTPS والصفحة الفعلية. لا تدخل مفاتيح GitHub أو كلمات مرور داخل المعاينة.

- [دليل تفعيل Pages وكتابة ومعاينة ونشر/إيقاف الرسائل خطوة بخطوة](docs/OWNER_NOTICES_AR.md) — النشر محمي بحساب المالك فقط.
