.class public Lorg/pouya/tvhomebridge/HomeAccessibilityService;
.super Landroid/accessibilityservice/AccessibilityService;
.method public constructor <init>()V
.locals 0
invoke-direct {p0}, Landroid/accessibilityservice/AccessibilityService;-><init>()V
return-void
.end method
.method public onInterrupt()V
.locals 0
return-void
.end method
.method public onAccessibilityEvent(Landroid/view/accessibility/AccessibilityEvent;)V
.locals 3
if-eqz p1, :done
invoke-virtual {p1}, Landroid/view/accessibility/AccessibilityEvent;->getEventType()I
move-result v0
const/16 v1, 0x20
if-ne v0, v1, :done
invoke-virtual {p1}, Landroid/view/accessibility/AccessibilityEvent;->getPackageName()Ljava/lang/CharSequence;
move-result-object v0
if-eqz v0, :done
invoke-interface {v0}, Ljava/lang/CharSequence;->toString()Ljava/lang/String;
move-result-object v0
const-string v1, "com.realtek.tv"
invoke-virtual {v1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z
move-result v2
if-eqz v2, :done
invoke-virtual {p1}, Landroid/view/accessibility/AccessibilityEvent;->getClassName()Ljava/lang/CharSequence;
move-result-object v0
if-eqz v0, :done
invoke-interface {v0}, Ljava/lang/CharSequence;->toString()Ljava/lang/String;
move-result-object v0
const-string v1, "com.realtek.tv.LauncherMainActivity"
invoke-virtual {v1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z
move-result v2
if-eqz v2, :done
const-string v0, "TVHomeBridge"
const-string v1, "Realtek ribbon observed; launching Google Home"
invoke-static {v0, v1}, Landroid/util/Log;->i(Ljava/lang/String;Ljava/lang/String;)I
invoke-direct {p0}, Lorg/pouya/tvhomebridge/HomeAccessibilityService;->launchGoogleHome()V
:done
return-void
.end method
.method protected onKeyEvent(Landroid/view/KeyEvent;)Z
.locals 2
invoke-virtual {p1}, Landroid/view/KeyEvent;->getAction()I
move-result v0
if-nez v0, :pass
invoke-virtual {p1}, Landroid/view/KeyEvent;->getKeyCode()I
move-result v0
const/4 v1, 0x3
if-ne v0, v1, :pass
const-string v0, "TVHomeBridge"
const-string v1, "Home key observed; launching Google Home"
invoke-static {v0, v1}, Landroid/util/Log;->i(Ljava/lang/String;Ljava/lang/String;)I
invoke-direct {p0}, Lorg/pouya/tvhomebridge/HomeAccessibilityService;->launchGoogleHome()V
const/4 v0, 0x1
return v0
:pass
invoke-super {p0, p1}, Landroid/accessibilityservice/AccessibilityService;->onKeyEvent(Landroid/view/KeyEvent;)Z
move-result v0
return v0
.end method
.method private launchGoogleHome()V
.locals 4
:try_start
new-instance v0, Landroid/content/Intent;
const-string v1, "android.intent.action.MAIN"
invoke-direct {v0, v1}, Landroid/content/Intent;-><init>(Ljava/lang/String;)V
const-string v1, "com.google.android.tvlauncher"
const-string v2, "com.google.android.tvlauncher.MainActivity"
invoke-virtual {v0, v1, v2}, Landroid/content/Intent;->setClassName(Ljava/lang/String;Ljava/lang/String;)Landroid/content/Intent;
const/high16 v1, 0x10000000
invoke-virtual {v0, v1}, Landroid/content/Intent;->addFlags(I)Landroid/content/Intent;
invoke-virtual {p0, v0}, Lorg/pouya/tvhomebridge/HomeAccessibilityService;->startActivity(Landroid/content/Intent;)V
:try_end
goto :done
.catch Ljava/lang/Throwable; {:try_start .. :try_end} :catch
:catch
move-exception v0
const-string v1, "TVHomeBridge"
const-string v2, "Google Home launch failed"
invoke-static {v1, v2, v0}, Landroid/util/Log;->e(Ljava/lang/String;Ljava/lang/String;Ljava/lang/Throwable;)I
:done
return-void
.end method
