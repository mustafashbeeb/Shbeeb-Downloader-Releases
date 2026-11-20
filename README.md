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
