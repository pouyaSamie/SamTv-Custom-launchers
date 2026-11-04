<div dir="rtl" align="right">

# خانه و کنترل دلخواه برای تلویزیون SAM

نسخهٔ **0.1.4** · [English](README.md)

اگر از نوار سام‌بازار روی صفحهٔ تلویزیون خسته شده‌اید، این بسته کمک می‌کند با دکمهٔ **Home** وارد لانچر دلخواهتان شوید و همچنان بتوانید بین ورودی‌های HDMI جابه‌جا شوید. دکمهٔ چهاررنگ کنترل را هم می‌توانید برای باز کردن تنظیمات تلویزیون، یک برنامه مثل VLC یا نوار قدیمی سام‌بازار تنظیم کنید.

این نسخه روی تلویزیون **SAM R4 با اندروید ۱۱** آزمایش شده است. ممکن است روی مدل‌های دیگر هم کار کند، اما هنوز آن‌ها را آزمایش نکرده‌ایم. برنامهٔ نصب پیش از هر تغییری سازگاری تلویزیون را بررسی می‌کند و اگر مطمئن نباشد، نصب را متوقف می‌کند.

## چه چیزهایی نصب می‌شود؟

- **تنظیم دکمه‌ها (Remote Buttons):** انتخاب کار دکمهٔ چهاررنگ. مدیریت دکمه‌های Home و Source هم در همین بسته است.
- **انتخاب صفحهٔ خانه (Choose Home):** انتخاب لانچری که با Home باز می‌شود؛ مثلاً صفحهٔ اصلی اندروید تی‌وی یا Projectivy. این میان‌بر به‌طور پیش‌فرض برای نصب انتخاب شده و می‌توانید هنگام نصب از آن صرف‌نظر کنید.
- **تنظیمات تلویزیون (TV Settings):** میان‌بری برای باز کردن تنظیمات تصویر، صدا و سایر تنظیمات خود تلویزیون. این مورد هم به‌طور پیش‌فرض انتخاب شده است.

برنامهٔ اصلی تلویزیون برای نمایش HDMI و قابلیت‌های سخت‌افزاری باقی می‌ماند. نصب این بسته برنامه‌ها و اطلاعات شخصی شما را پاک نمی‌کند.

## نصب در چند قدم

برای **ویندوز ۶۴بیتی** و **لینوکس ۶۴بیتی** فایل جداگانه آماده شده است. تلویزیون و رایانه باید به یک شبکهٔ خانگی وصل باشند.

۱. فایل مناسب رایانه‌تان، **`SAM-TV-v0.1.4-windows.zip`** یا **`SAM-TV-v0.1.4-linux.tar.gz`**، را از بخش Releases دریافت و از حالت فشرده خارج کنید.

۲. برنامهٔ [**Activity Launcher** در F-Droid](https://f-droid.org/en/packages/de.szalkowski.activitylauncher/) را روی تلویزیون نصب و باز کنید. `DevelopmentActivity` را جست‌وجو کنید؛ شناسهٔ آن `system.development.developmentActivity` است. در آن صفحه فقط **Developer Mode** و **USB Debugging** را روشن کنید. سپس آدرس IP تلویزیون را از تنظیمات شبکه یادداشت کنید. [توضیح بیشتر](docs/INSTALL.fa.md) در راهنمای نصب آمده است.

۳. در ویندوز روی **`Install-SAM-TV.cmd`** دوبار کلیک کنید. در لینوکس فایل اجرایی **`Install-SAM-TV`** را اجرا کنید.

۴. زبان و گزینهٔ «نصب» را انتخاب کنید، آدرس IP تلویزیون را وارد کنید و اگر تلویزیون درخواست اجازهٔ اتصال نشان داد، آن را تأیید کنید. برنامه ابتدا سازگاری را بررسی می‌کند. برای نصب هر دو میان‌بر اختیاری، در سؤال‌های بعدی فقط **Enter** بزنید. در پایان، برای شروع نصب `INSTALL` یا «نصب» را تایپ کنید.

۵. پس از نصب، با کنترل تلویزیون **Home**، سپس **Source/Input** و انتخاب یک HDMI، و در آخر دکمهٔ **چهاررنگ** را امتحان کنید. برای تغییر لانچر، برنامهٔ **Choose Home** را باز کنید.

اگر در هر مرحله پیام ناسازگاری دیدید، نصب را به‌زور ادامه ندهید. اگر بعد از نصب دکمه‌ای درست کار نکرد، روش بازگرداندن تنظیم قبلی در [راهنمای نصب و بازیابی](docs/INSTALL.fa.md) آمده است.

## لانچرهای تست‌شده

**[Projectivy Launcher](https://play.google.com/store/apps/details?id=com.spocky.projengmenu) — تست شده و پیشنهاد ما.** ظاهر مرتب‌تری دارد. داخل بسته نیست؛ آن را جداگانه نصب کنید و سپس در **Choose Home** انتخاب کنید.

<img src="https://play-lh.googleusercontent.com/U1hhfK4bw9Q9C-qbj1AfReA-lpDqrovDLZxfl99V1UdBnCcijmNCXEcj9MFDkC00eTF6mt2-b072VYjbUsGJwA=w1052-h592" width="520" alt="نمای عمومی Projectivy Launcher از صفحهٔ رسمی برنامه در Google Play">

*تصویر نمونه از [صفحهٔ Projectivy در Google Play](https://play.google.com/store/apps/details?id=com.spocky.projengmenu)؛ چیدمان برنامه‌ها و تصویر پس‌زمینهٔ تلویزیون شما ممکن است فرق کند.*

**[صفحهٔ اصلی Android TV گوگل](https://play.google.com/store/apps/details?id=com.google.android.tvlauncher) — تست شده.** این گزینه از ابتدا روی تلویزیون نصب بود.

<img src="https://play-lh.googleusercontent.com/kmvrlAqiL1m2HV91XvR5lP8g7h9AXx1VB2jPIWdpVUIRo2F93o5nSyJ65naRBsXvl-M3z-H5kM6mnh5Dadpx=w1052-h592" width="520" alt="نمای عمومی Android TV Home از صفحهٔ رسمی گوگل">

*تصویر نمونه از [صفحهٔ Android TV Home در Google Play](https://play.google.com/store/apps/details?id=com.google.android.tvlauncher).*

**[LTvLauncher](https://github.com/leanbitlab-org/LtvLauncher) — تست شده.** این لانچر جداگانه نصب می‌شود.

<img src="https://raw.githubusercontent.com/leanbitlab-org/LtvLauncher/master/docs/images/screenshot_1.png" width="520" alt="نمای عمومی LTvLauncher از مخزن رسمی سازنده">

*تصویر نمونه از [مخزن رسمی LTvLauncher](https://github.com/leanbitlab-org/LtvLauncher).*

در **Choose Home** می‌توانید هر لانچر نصب‌شدهٔ سازگار را برای دکمهٔ Home انتخاب کنید. گزینهٔ **Install new launcher** جست‌وجوی لانچر را در Play Store تلویزیون باز می‌کند.

برای جزئیات بیشتر [راهنمای نصب و بازیابی](docs/INSTALL.fa.md) را بخوانید. [متن انگلیسی](README.md) هم در همین بسته موجود است.

کد و نوشته‌های اصلی این پروژه با [مجوز MIT](LICENSE) منتشر می‌شوند. فایل‌های متعلق به سازندگان دیگر مجوزهای جداگانه دارند؛ [توضیح مجوزها](NOTICE.md) را ببینید.

</div>
