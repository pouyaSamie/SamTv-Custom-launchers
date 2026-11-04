.class public Lorg/pouya/tvhomebridge/BootReceiver;
.super Landroid/content/BroadcastReceiver;
.method public constructor <init>()V
.locals 0
invoke-direct {p0}, Landroid/content/BroadcastReceiver;-><init>()V
return-void
.end method
.method public onReceive(Landroid/content/Context;Landroid/content/Intent;)V
.locals 3
new-instance v0, Landroid/content/Intent;
const-class v1, Lorg/pouya/tvhomebridge/KeyProbeService;
invoke-direct {v0, p1, v1}, Landroid/content/Intent;-><init>(Landroid/content/Context;Ljava/lang/Class;)V
invoke-virtual {p1, v0}, Landroid/content/Context;->startForegroundService(Landroid/content/Intent;)Landroid/content/ComponentName;
const-string v1, "TVHomeBridge"
const-string v2, "Boot receiver started key service"
invoke-static {v1, v2}, Landroid/util/Log;->i(Ljava/lang/String;Ljava/lang/String;)I
return-void
.end method
