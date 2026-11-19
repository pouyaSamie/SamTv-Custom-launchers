## فارسی

نسخهٔ 0.1.9 بررسی نسخهٔ اندروید را تغییر می‌دهد تا **اندروید ۱۱ و بالاتر**، از جمله نسخهٔ فعلی Android TV OS 16، پذیرفته شود. پیش از این، برنامهٔ نصب فقط اندروید ۱۱ را می‌پذیرفت؛ حالا عدد نسخهٔ اندروید با حداقل ۱۱ مقایسه می‌شود و نسخه‌های ۱۲، ۱۲L، ۱۳ و جدیدتر از این بررسی می‌گذرند. اگر فریموری نسخهٔ اندروید را غیرعددی گزارش کند، برنامه به‌جای آن از سطح SDK (۳۰ به بالا) استفاده می‌کند. آزمون بررسی نسخه تا اندروید ۱۶ را پوشش می‌دهد؛ در عمل فقط نرم‌افزار متناظر با SAM R4 و اندروید ۱۱ آزمایش شده است و برای سایر نرم‌افزارها باید از مسیر «آزمون و نصب آزمایشی» استفاده کرد.

نصب معمولی همچنان فقط برای همان پروفایل تست‌شدهٔ تلویزیون SAM R4 است؛ تلویزیون‌های دیگر با هر نسخهٔ اندروید باید از مسیر «آزمون و نصب آزمایشی» و با مسئولیت خودشان پیش بروند.

برای شروع، فقط [فایل ویندوز](https://github.com/pouyaSamie/SamTv-Custom-launchers/releases/download/v0.1.9/SAM-TV-v0.1.9-windows.zip) یا [فایل لینوکس](https://github.com/pouyaSamie/SamTv-Custom-launchers/releases/download/v0.1.9/SAM-TV-v0.1.9-linux.tar.gz) را متناسب با رایانهٔتان بگیرید و [راهنمای نصب فارسی](https://github.com/pouyaSamie/SamTv-Custom-launchers/blob/v0.1.9/docs/INSTALL.fa.md) را دنبال کنید. در پرسش‌های برنامه، `y` یا Enter یعنی تأیید و `n` یا Esc یعنی رد کردن.

فایل‌های تلویزیون نسبت به نسخهٔ 0.1.8 تغییر نکرده‌اند.

## English

Version 0.1.9 changes the Android-version check to accept **Android 11 and newer**, including the current Android TV OS 16. The installer previously required exactly Android 11; it now compares the numeric Android release against a minimum of 11, so Android 12, 12L, 13, and later releases pass this check. If a firmware reports a non-numeric release string, the installer falls back to the SDK level (30 or higher, the SDK of Android 11). The version gate is exercised through Android 16; only the matching SAM R4 Android 11 firmware has been field-tested, and other firmware requires the Experimental trial path.

The normal setup still targets the exact tested SAM R4 profile; other TVs on any supported Android version must use the **Experimental trial** path at their own risk.

Download only the [Windows installer](https://github.com/pouyaSamie/SamTv-Custom-launchers/releases/download/v0.1.9/SAM-TV-v0.1.9-windows.zip) or [Linux installer](https://github.com/pouyaSamie/SamTv-Custom-launchers/releases/download/v0.1.9/SAM-TV-v0.1.9-linux.tar.gz). `y` or Enter accepts each yes/no prompt; `n` or Esc declines it.

TV APKs are unchanged from 0.1.8.
