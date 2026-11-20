"use strict";
// Strictly local preview: no fetch, tracking, cookies, credentials, GitHub tokens or publishing.
const fields = ["title", "body", "audience", "category", "days"];
const ui = Object.fromEntries(fields.map(id => [id, document.getElementById(id)]));
const previewTitle = document.getElementById("previewTitle");
const previewBody = document.getElementById("previewBody");
const status = document.getElementById("copyStatus");

function render() {
  previewTitle.textContent = ui.title.value.trim() || "عنوان الرسالة";
  previewBody.textContent = ui.body.value.trim() || "اكتب رسالة لتظهر المعاينة.";
  status.textContent = "";
}
for (const id of fields) ui[id].addEventListener("input", render);
render();

document.getElementById("copy").addEventListener("click", async () => {
  const title = ui.title.value.trim();
  const body = ui.body.value.trim();
  const duration = Number(ui.days.value);
  if (!title || !body || title.length > 80 || body.length > 500 ||
      !Number.isInteger(duration) || duration < 1 || duration > 90 ||
      /[\u0000-\u0009\u000b-\u001f\u007f]/.test(body) ||
      /[\u0000-\u001f\u007f]/.test(title)) {
    status.textContent = "تحقق من العنوان والنص والمدة قبل النسخ.";
    return;
  }
  const payload = [
    "Title: " + title, "Body: " + body,
    "Audience: " + ui.audience.value, "Category: " + ui.category.value,
    "Duration days: " + duration
  ].join("\n");
  try {
    await navigator.clipboard.writeText(payload);
    status.textContent = "تم النسخ. راجع البيانات ثم انشرها من حساب GitHub الخاص بك.";
  } catch (err) {
    status.textContent = "تعذر النسخ التلقائي؛ انسخ البيانات يدوياً ثم انتقل إلى GitHub.";
  }
});
