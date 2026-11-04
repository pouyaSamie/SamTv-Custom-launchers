.class public Lorg/pouya/tvhomebridge/LauncherRouterActivity;
.super Landroid/app/Activity;

.method public constructor <init>()V
.locals 0
invoke-direct {p0}, Landroid/app/Activity;-><init>()V
return-void
.end method

.method protected onCreate(Landroid/os/Bundle;)V
.locals 0
invoke-super {p0, p1}, Landroid/app/Activity;->onCreate(Landroid/os/Bundle;)V
invoke-static {p0}, Lorg/pouya/tvhomebridge/LauncherTarget;->open(Landroid/content/Context;)V
invoke-virtual {p0}, Lorg/pouya/tvhomebridge/LauncherRouterActivity;->finish()V
return-void
.end method
