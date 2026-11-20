# Shbeeb Downloader — Public update notices (no APK distribution)

This **public** repository is reserved for the owner-approved read-only announcement/update pages of Shbeeb Downloader.

## Current status: signed private BETA 32, metadata public

- The repository is **public metadata-only**; GitHub Pages/HTTPS were previously verified by the owner on the phone for the Beta31 notification.
- `beta/android.json` now advertises the **verified signed Beta32** (`0.3.11-beta`, code 32), whose private GitHub Release Draft includes `Shbeeb-BETA-v32.apk`. The owner-only Release page is linked from `beta/index.html`; GitHub requires a permitted signed-in account to view its assets.
- No APK, signing key, secret, token or private GitHub Actions artifact is stored in this public repository.
- The public site must never link directly to a distributable public APK while licensing issue #64 remains unresolved.
- No Android OS Push service is claimed or provided.

## Live URLs (GitHub Pages)

- Overview: `https://mustafashbeeb.github.io/Shbeeb-Downloader-Releases/`
- Beta 32 information and owner-only link: `https://mustafashbeeb.github.io/Shbeeb-Downloader-Releases/beta/`
- In-app version feed: `https://mustafashbeeb.github.io/Shbeeb-Downloader-Releases/beta/android.json`

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
