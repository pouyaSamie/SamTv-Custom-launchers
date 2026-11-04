.class public Lorg/pouya/tvhomebridge/LauncherTarget;
.super Ljava/lang/Object;

.method public constructor <init>()V
.locals 0
invoke-direct {p0}, Ljava/lang/Object;-><init>()V
return-void
.end method

.method public static open(Landroid/content/Context;)V
.locals 5
invoke-virtual {p0}, Landroid/content/Context;->getContentResolver()Landroid/content/ContentResolver;
move-result-object v0
const-string v1, "tv_home_bridge_home_component"
invoke-static {v0, v1}, Landroid/provider/Settings$Global;->getString(Landroid/content/ContentResolver;Ljava/lang/String;)Ljava/lang/String;
move-result-object v1
if-eqz v1, :google
invoke-static {v1}, Landroid/content/ComponentName;->unflattenFromString(Ljava/lang/String;)Landroid/content/ComponentName;
move-result-object v2
if-eqz v2, :google
invoke-virtual {v2}, Landroid/content/ComponentName;->getPackageName()Ljava/lang/String;
move-result-object v3
const-string v4, "org.pouya.tvhomebridge"
invoke-virtual {v4, v3}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z
move-result v3
if-nez v3, :google
goto :launch
:google
new-instance v2, Landroid/content/ComponentName;
const-string v3, "com.google.android.tvlauncher"
const-string v4, "com.google.android.tvlauncher.MainActivity"
invoke-direct {v2, v3, v4}, Landroid/content/ComponentName;-><init>(Ljava/lang/String;Ljava/lang/String;)V
:launch
new-instance v0, Landroid/content/Intent;
const-string v1, "android.intent.action.MAIN"
invoke-direct {v0, v1}, Landroid/content/Intent;-><init>(Ljava/lang/String;)V
invoke-virtual {v0, v2}, Landroid/content/Intent;->setComponent(Landroid/content/ComponentName;)Landroid/content/Intent;
const-string v1, "android.intent.category.HOME"
invoke-virtual {v0, v1}, Landroid/content/Intent;->addCategory(Ljava/lang/String;)Landroid/content/Intent;
const/high16 v1, 0x10000000
invoke-virtual {v0, v1}, Landroid/content/Intent;->addFlags(I)Landroid/content/Intent;
:try_start
invoke-virtual {p0, v0}, Landroid/content/Context;->startActivity(Landroid/content/Intent;)V
:try_end
goto :done
.catch Ljava/lang/Exception; {:try_start .. :try_end} :fallback
:fallback
move-exception v0
new-instance v0, Landroid/content/Intent;
const-string v1, "android.intent.action.MAIN"
invoke-direct {v0, v1}, Landroid/content/Intent;-><init>(Ljava/lang/String;)V
const-string v2, "com.google.android.tvlauncher"
const-string v3, "com.google.android.tvlauncher.MainActivity"
invoke-virtual {v0, v2, v3}, Landroid/content/Intent;->setClassName(Ljava/lang/String;Ljava/lang/String;)Landroid/content/Intent;
const/high16 v1, 0x10000000
invoke-virtual {v0, v1}, Landroid/content/Intent;->addFlags(I)Landroid/content/Intent;
invoke-virtual {p0, v0}, Landroid/content/Context;->startActivity(Landroid/content/Intent;)V
:done
return-void
.end method
