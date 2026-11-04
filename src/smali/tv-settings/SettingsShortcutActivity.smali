.class public Lorg/pouya/tvsettingsshortcut/SettingsShortcutActivity;
.super Landroid/app/Activity;
.method public constructor <init>()V
.locals 0
invoke-direct {p0}, Landroid/app/Activity;-><init>()V
return-void
.end method
.method protected onCreate(Landroid/os/Bundle;)V
.locals 3
invoke-super {p0, p1}, Landroid/app/Activity;->onCreate(Landroid/os/Bundle;)V
new-instance v0, Landroid/content/Intent;
const-string v1, "android.intent.action.MAIN"
invoke-direct {v0, v1}, Landroid/content/Intent;-><init>(Ljava/lang/String;)V
const-string v1, "com.realtek.menu"
const-string v2, "com.realtek.menu.MainActivity"
invoke-virtual {v0, v1, v2}, Landroid/content/Intent;->setClassName(Ljava/lang/String;Ljava/lang/String;)Landroid/content/Intent;
const/high16 v1, 0x10000000
invoke-virtual {v0, v1}, Landroid/content/Intent;->addFlags(I)Landroid/content/Intent;
invoke-virtual {p0, v0}, Lorg/pouya/tvsettingsshortcut/SettingsShortcutActivity;->startActivity(Landroid/content/Intent;)V
invoke-virtual {p0}, Lorg/pouya/tvsettingsshortcut/SettingsShortcutActivity;->finish()V
return-void
.end method
