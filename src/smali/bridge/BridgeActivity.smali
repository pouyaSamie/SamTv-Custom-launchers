.class public Lorg/pouya/tvhomebridge/BridgeActivity;
.super Landroid/app/Activity;
.method public constructor <init>()V
.locals 0
invoke-direct {p0}, Landroid/app/Activity;-><init>()V
return-void
.end method
.method protected onCreate(Landroid/os/Bundle;)V
.locals 2
invoke-super {p0, p1}, Landroid/app/Activity;->onCreate(Landroid/os/Bundle;)V
new-instance v0, Landroid/content/Intent;
const-class v1, Lorg/pouya/tvhomebridge/KeyProbeService;
invoke-direct {v0, p0, v1}, Landroid/content/Intent;-><init>(Landroid/content/Context;Ljava/lang/Class;)V
invoke-virtual {p0, v0}, Lorg/pouya/tvhomebridge/BridgeActivity;->startService(Landroid/content/Intent;)Landroid/content/ComponentName;
invoke-virtual {p0}, Lorg/pouya/tvhomebridge/BridgeActivity;->finish()V
return-void
.end method
