.class public Lorg/pouya/tvhomebridge/KeyProbeService;
.super Landroid/app/Service;
.implements Lcom/realtek/system/KeyEventManager$OnKeyListener;
.field private manager:Lcom/realtek/system/KeyEventManager;
.field private registered:Z
.method public constructor <init>()V
.locals 0
invoke-direct {p0}, Landroid/app/Service;-><init>()V
return-void
.end method
.method public onBind(Landroid/content/Intent;)Landroid/os/IBinder;
.locals 1
const/4 v0, 0x0
return-object v0
.end method
.method public onStartCommand(Landroid/content/Intent;II)I
.locals 7
const-string v0, "notification"
invoke-virtual {p0, v0}, Lorg/pouya/tvhomebridge/KeyProbeService;->getSystemService(Ljava/lang/String;)Ljava/lang/Object;
move-result-object v0
check-cast v0, Landroid/app/NotificationManager;
new-instance v1, Landroid/app/NotificationChannel;
const-string v2, "tv_home_bridge"
const-string v3, "TV Home Bridge"
const/4 v4, 0x2
invoke-direct {v1, v2, v3, v4}, Landroid/app/NotificationChannel;-><init>(Ljava/lang/String;Ljava/lang/CharSequence;I)V
invoke-virtual {v0, v1}, Landroid/app/NotificationManager;->createNotificationChannel(Landroid/app/NotificationChannel;)V
new-instance v0, Landroid/app/Notification$Builder;
invoke-direct {v0, p0, v2}, Landroid/app/Notification$Builder;-><init>(Landroid/content/Context;Ljava/lang/String;)V
const-string v1, "TV Home Bridge"
invoke-virtual {v0, v1}, Landroid/app/Notification$Builder;->setContentTitle(Ljava/lang/CharSequence;)Landroid/app/Notification$Builder;
move-result-object v0
const-string v1, "Home and Source buttons active"
invoke-virtual {v0, v1}, Landroid/app/Notification$Builder;->setContentText(Ljava/lang/CharSequence;)Landroid/app/Notification$Builder;
move-result-object v0
const v1, 0x7f0f0000
invoke-virtual {v0, v1}, Landroid/app/Notification$Builder;->setSmallIcon(I)Landroid/app/Notification$Builder;
move-result-object v0
invoke-virtual {v0}, Landroid/app/Notification$Builder;->build()Landroid/app/Notification;
move-result-object v0
const/16 v1, 0x65
invoke-virtual {p0, v1, v0}, Lorg/pouya/tvhomebridge/KeyProbeService;->startForeground(ILandroid/app/Notification;)V
iget-boolean v0, p0, Lorg/pouya/tvhomebridge/KeyProbeService;->registered:Z
if-eqz v0, :register_keys
const/4 v0, 0x1
return v0
:register_keys
invoke-static {}, Lcom/realtek/system/KeyEventManager;->getInstance()Lcom/realtek/system/KeyEventManager;
move-result-object v0
iput-object v0, p0, Lorg/pouya/tvhomebridge/KeyProbeService;->manager:Lcom/realtek/system/KeyEventManager;
invoke-virtual {v0, p0}, Lcom/realtek/system/KeyEventManager;->setKeyEventListener(Lcom/realtek/system/KeyEventManager$OnKeyListener;)V
const/4 v1, 0x2
invoke-virtual {v0, v1}, Lcom/realtek/system/KeyEventManager;->registerAllKey(I)Z
move-result v1
iput-boolean v1, p0, Lorg/pouya/tvhomebridge/KeyProbeService;->registered:Z
const-string v0, "TVHomeBridge"
invoke-static {v1}, Ljava/lang/String;->valueOf(Z)Ljava/lang/String;
move-result-object v2
invoke-static {v0, v2}, Landroid/util/Log;->i(Ljava/lang/String;Ljava/lang/String;)I
const/4 v0, 0x1
return v0
.end method
.method public onDestroy()V
.locals 2
iget-object v0, p0, Lorg/pouya/tvhomebridge/KeyProbeService;->manager:Lcom/realtek/system/KeyEventManager;
if-eqz v0, :done
const/4 v1, 0x2
invoke-virtual {v0, v1}, Lcom/realtek/system/KeyEventManager;->unregisterAllKey(I)Z
:done
invoke-super {p0}, Landroid/app/Service;->onDestroy()V
return-void
.end method
.method public onKeyDown(ILjava/lang/String;)I
.locals 4
const/4 v0, 0x3
if-eq p1, v0, :home
const/16 v0, 0x89
if-eq p1, v0, :source
const/16 v0, 0x8a
if-eq p1, v0, :settings
const/4 v0, 0x0
return v0
:home
const-string v0, "TVHomeBridge"
const-string v1, "HOME key -> selected launcher"
invoke-static {v0, v1}, Landroid/util/Log;->i(Ljava/lang/String;Ljava/lang/String;)I
invoke-static {p0}, Lorg/pouya/tvhomebridge/LauncherTarget;->open(Landroid/content/Context;)V
const/4 v0, 0x1
return v0
:source
const-string v0, "TVHomeBridge"
const-string v1, "SOURCE key -> Realtek input selector"
invoke-static {v0, v1}, Landroid/util/Log;->i(Ljava/lang/String;Ljava/lang/String;)I
new-instance v2, Landroid/content/Intent;
const-string v0, "android.intent.action.MAIN"
invoke-direct {v2, v0}, Landroid/content/Intent;-><init>(Ljava/lang/String;)V
const-string v0, "com.realtek.tv"
const-string v1, "com.realtek.tv.SelectInputActivity"
invoke-virtual {v2, v0, v1}, Landroid/content/Intent;->setClassName(Ljava/lang/String;Ljava/lang/String;)Landroid/content/Intent;
const/high16 v0, 0x10000000
invoke-virtual {v2, v0}, Landroid/content/Intent;->addFlags(I)Landroid/content/Intent;
invoke-virtual {p0, v2}, Lorg/pouya/tvhomebridge/KeyProbeService;->startActivity(Landroid/content/Intent;)V
const/4 v0, 0x1
return v0
:settings
invoke-direct {p0}, Lorg/pouya/tvhomebridge/KeyProbeService;->handleColor()I
move-result v0
return v0
.end method

.method private handleColor()I
.locals 6
invoke-virtual {p0}, Lorg/pouya/tvhomebridge/KeyProbeService;->getContentResolver()Landroid/content/ContentResolver;
move-result-object v0
const-string v1, "tv_home_bridge_color_action"
invoke-static {v0, v1}, Landroid/provider/Settings$Global;->getString(Landroid/content/ContentResolver;Ljava/lang/String;)Ljava/lang/String;
move-result-object v1
const-string v2, "original"
invoke-virtual {v2, v1}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z
move-result v2
if-eqz v2, :not_original
const/4 v0, 0x0
return v0
:not_original
new-instance v3, Landroid/content/Intent;
const-string v0, "android.intent.action.MAIN"
invoke-direct {v3, v0}, Landroid/content/Intent;-><init>(Ljava/lang/String;)V
const-string v2, "sambazar"
invoke-virtual {v2, v1}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z
move-result v2
if-eqz v2, :not_sambazar
const-string v0, "com.realtek.tv"
const-string v1, "com.realtek.tv.LauncherMainActivity"
invoke-virtual {v3, v0, v1}, Landroid/content/Intent;->setClassName(Ljava/lang/String;Ljava/lang/String;)Landroid/content/Intent;
goto :launch
:not_sambazar
const-string v2, "app:"
if-eqz v1, :default_settings
invoke-virtual {v1, v2}, Ljava/lang/String;->startsWith(Ljava/lang/String;)Z
move-result v4
if-eqz v4, :default_settings
const/4 v4, 0x4
invoke-virtual {v1, v4}, Ljava/lang/String;->substring(I)Ljava/lang/String;
move-result-object v1
invoke-static {v1}, Landroid/content/ComponentName;->unflattenFromString(Ljava/lang/String;)Landroid/content/ComponentName;
move-result-object v1
if-eqz v1, :default_settings
invoke-virtual {v3, v1}, Landroid/content/Intent;->setComponent(Landroid/content/ComponentName;)Landroid/content/Intent;
goto :launch
:default_settings
const-string v0, "com.realtek.menu"
const-string v1, "com.realtek.menu.MainActivity"
invoke-virtual {v3, v0, v1}, Landroid/content/Intent;->setClassName(Ljava/lang/String;Ljava/lang/String;)Landroid/content/Intent;
:launch
const/high16 v0, 0x10000000
invoke-virtual {v3, v0}, Landroid/content/Intent;->addFlags(I)Landroid/content/Intent;
:try_start
invoke-virtual {p0, v3}, Lorg/pouya/tvhomebridge/KeyProbeService;->startActivity(Landroid/content/Intent;)V
:try_start_end
goto :success
.catch Ljava/lang/Exception; {:try_start .. :try_start_end} :catch_start
:catch_start
move-exception v4
const-string v0, "TVHomeBridge"
const-string v1, "Mapped app unavailable"
invoke-static {v0, v1, v4}, Landroid/util/Log;->e(Ljava/lang/String;Ljava/lang/String;Ljava/lang/Throwable;)I
:success
const/4 v0, 0x1
return v0
.end method
.method public onKeyUp(ILjava/lang/String;)I
.locals 1
const/4 v0, 0x0
return v0
.end method
