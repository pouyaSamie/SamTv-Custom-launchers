.class public Lorg/pouya/tvhomebridge/LauncherSelectActivity;
.super Landroid/app/Activity;
.implements Landroid/widget/AdapterView$OnItemClickListener;

.field private rows:Ljava/util/ArrayList;
.field private actions:Ljava/util/ArrayList;
.field private grid:Landroid/widget/GridView;

.method public constructor <init>()V
.locals 0
invoke-direct {p0}, Landroid/app/Activity;-><init>()V
return-void
.end method

.method protected onCreate(Landroid/os/Bundle;)V
.locals 8
invoke-super {p0, p1}, Landroid/app/Activity;->onCreate(Landroid/os/Bundle;)V
const-string v0, "Select default launcher"
invoke-virtual {p0, v0}, Lorg/pouya/tvhomebridge/LauncherSelectActivity;->setTitle(Ljava/lang/CharSequence;)V
invoke-virtual {p0}, Lorg/pouya/tvhomebridge/LauncherSelectActivity;->getResources()Landroid/content/res/Resources;
move-result-object v4
const-string v5, "home_selector"
const-string v6, "layout"
invoke-virtual {p0}, Lorg/pouya/tvhomebridge/LauncherSelectActivity;->getPackageName()Ljava/lang/String;
move-result-object v7
invoke-virtual {v4, v5, v6, v7}, Landroid/content/res/Resources;->getIdentifier(Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;)I
move-result v4
invoke-virtual {p0, v4}, Lorg/pouya/tvhomebridge/LauncherSelectActivity;->setContentView(I)V
new-instance v0, Ljava/util/ArrayList;
invoke-direct {v0}, Ljava/util/ArrayList;-><init>()V
iput-object v0, p0, Lorg/pouya/tvhomebridge/LauncherSelectActivity;->rows:Ljava/util/ArrayList;
new-instance v1, Ljava/util/ArrayList;
invoke-direct {v1}, Ljava/util/ArrayList;-><init>()V
iput-object v1, p0, Lorg/pouya/tvhomebridge/LauncherSelectActivity;->actions:Ljava/util/ArrayList;
invoke-direct {p0}, Lorg/pouya/tvhomebridge/LauncherSelectActivity;->addLaunchers()V
const-string v2, "Install new launcher"
invoke-virtual {v0, v2}, Ljava/util/ArrayList;->add(Ljava/lang/Object;)Z
const-string v2, "install"
invoke-virtual {v1, v2}, Ljava/util/ArrayList;->add(Ljava/lang/Object;)Z
new-instance v2, Lorg/pouya/tvhomebridge/LauncherPreviewAdapter;
invoke-virtual {p0}, Lorg/pouya/tvhomebridge/LauncherSelectActivity;->getResources()Landroid/content/res/Resources;
move-result-object v4
const-string v5, "home_card"
const-string v6, "layout"
invoke-virtual {p0}, Lorg/pouya/tvhomebridge/LauncherSelectActivity;->getPackageName()Ljava/lang/String;
move-result-object v7
invoke-virtual {v4, v5, v6, v7}, Landroid/content/res/Resources;->getIdentifier(Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;)I
move-result v3
const v4, 0x1020014
move-object v7, v1
move-object v6, v0
move v5, v4
move v4, v3
move-object v3, p0
invoke-direct/range {v2 .. v7}, Lorg/pouya/tvhomebridge/LauncherPreviewAdapter;-><init>(Landroid/content/Context;IILjava/util/ArrayList;Ljava/util/ArrayList;)V
invoke-virtual {p0}, Lorg/pouya/tvhomebridge/LauncherSelectActivity;->getResources()Landroid/content/res/Resources;
move-result-object v4
const-string v5, "home_grid"
const-string v6, "id"
invoke-virtual {p0}, Lorg/pouya/tvhomebridge/LauncherSelectActivity;->getPackageName()Ljava/lang/String;
move-result-object v7
invoke-virtual {v4, v5, v6, v7}, Landroid/content/res/Resources;->getIdentifier(Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;)I
move-result v4
invoke-virtual {p0, v4}, Lorg/pouya/tvhomebridge/LauncherSelectActivity;->findViewById(I)Landroid/view/View;
move-result-object v7
check-cast v7, Landroid/widget/GridView;
iput-object v7, p0, Lorg/pouya/tvhomebridge/LauncherSelectActivity;->grid:Landroid/widget/GridView;
invoke-virtual {v7, v2}, Landroid/widget/GridView;->setAdapter(Landroid/widget/ListAdapter;)V
invoke-virtual {v7, p0}, Landroid/widget/GridView;->setOnItemClickListener(Landroid/widget/AdapterView$OnItemClickListener;)V
invoke-virtual {p0}, Lorg/pouya/tvhomebridge/LauncherSelectActivity;->getContentResolver()Landroid/content/ContentResolver;
move-result-object v4
const-string v5, "tv_home_bridge_home_component"
invoke-static {v4, v5}, Landroid/provider/Settings$Global;->getString(Landroid/content/ContentResolver;Ljava/lang/String;)Ljava/lang/String;
move-result-object v5
invoke-virtual {v1, v5}, Ljava/util/ArrayList;->indexOf(Ljava/lang/Object;)I
move-result v6
if-ltz v6, :no_selection
iget-object v7, p0, Lorg/pouya/tvhomebridge/LauncherSelectActivity;->grid:Landroid/widget/GridView;
invoke-virtual {v7, v6}, Landroid/widget/GridView;->setSelection(I)V
:no_selection
return-void
.end method

.method private addLaunchers()V
.locals 10
new-instance v0, Landroid/content/Intent;
const-string v1, "android.intent.action.MAIN"
invoke-direct {v0, v1}, Landroid/content/Intent;-><init>(Ljava/lang/String;)V
const-string v1, "android.intent.category.HOME"
invoke-virtual {v0, v1}, Landroid/content/Intent;->addCategory(Ljava/lang/String;)Landroid/content/Intent;
invoke-virtual {p0}, Lorg/pouya/tvhomebridge/LauncherSelectActivity;->getPackageManager()Landroid/content/pm/PackageManager;
move-result-object v1
const/4 v2, 0x0
invoke-virtual {v1, v0, v2}, Landroid/content/pm/PackageManager;->queryIntentActivities(Landroid/content/Intent;I)Ljava/util/List;
move-result-object v0
invoke-interface {v0}, Ljava/util/List;->iterator()Ljava/util/Iterator;
move-result-object v2
:loop
invoke-interface {v2}, Ljava/util/Iterator;->hasNext()Z
move-result v3
if-eqz v3, :done
invoke-interface {v2}, Ljava/util/Iterator;->next()Ljava/lang/Object;
move-result-object v3
check-cast v3, Landroid/content/pm/ResolveInfo;
iget-object v4, v3, Landroid/content/pm/ResolveInfo;->activityInfo:Landroid/content/pm/ActivityInfo;
iget-object v5, v4, Landroid/content/pm/ActivityInfo;->packageName:Ljava/lang/String;
const-string v6, "org.pouya.tvhomebridge"
invoke-virtual {v6, v5}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z
move-result v6
if-nez v6, :loop
const-string v6, "com.realtek."
invoke-virtual {v5, v6}, Ljava/lang/String;->startsWith(Ljava/lang/String;)Z
move-result v6
if-nez v6, :loop
const-string v6, "com.android.tv.settings"
invoke-virtual {v6, v5}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z
move-result v6
if-nez v6, :loop
new-instance v6, Landroid/content/ComponentName;
iget-object v7, v4, Landroid/content/pm/ActivityInfo;->name:Ljava/lang/String;
invoke-direct {v6, v5, v7}, Landroid/content/ComponentName;-><init>(Ljava/lang/String;Ljava/lang/String;)V
invoke-virtual {v6}, Landroid/content/ComponentName;->flattenToString()Ljava/lang/String;
move-result-object v6
iget-object v7, p0, Lorg/pouya/tvhomebridge/LauncherSelectActivity;->actions:Ljava/util/ArrayList;
invoke-virtual {v7, v6}, Ljava/util/ArrayList;->contains(Ljava/lang/Object;)Z
move-result v8
if-nez v8, :loop
invoke-virtual {v3, v1}, Landroid/content/pm/ResolveInfo;->loadLabel(Landroid/content/pm/PackageManager;)Ljava/lang/CharSequence;
move-result-object v3
invoke-interface {v3}, Ljava/lang/CharSequence;->toString()Ljava/lang/String;
move-result-object v3
iget-object v8, p0, Lorg/pouya/tvhomebridge/LauncherSelectActivity;->rows:Ljava/util/ArrayList;
invoke-virtual {v8, v3}, Ljava/util/ArrayList;->add(Ljava/lang/Object;)Z
invoke-virtual {v7, v6}, Ljava/util/ArrayList;->add(Ljava/lang/Object;)Z
goto :loop
:done
return-void
.end method

.method public onItemClick(Landroid/widget/AdapterView;Landroid/view/View;IJ)V
.locals 5
iget-object v0, p0, Lorg/pouya/tvhomebridge/LauncherSelectActivity;->actions:Ljava/util/ArrayList;
invoke-virtual {v0, p3}, Ljava/util/ArrayList;->get(I)Ljava/lang/Object;
move-result-object v0
check-cast v0, Ljava/lang/String;
const-string v1, "install"
invoke-virtual {v1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z
move-result v1
if-eqz v1, :select_launcher
new-instance v0, Landroid/content/Intent;
const-string v1, "android.intent.action.VIEW"
invoke-direct {v0, v1}, Landroid/content/Intent;-><init>(Ljava/lang/String;)V
const-string v1, "market://search?q=Android%20TV%20launcher"
invoke-static {v1}, Landroid/net/Uri;->parse(Ljava/lang/String;)Landroid/net/Uri;
move-result-object v1
invoke-virtual {v0, v1}, Landroid/content/Intent;->setData(Landroid/net/Uri;)Landroid/content/Intent;
const-string v1, "com.android.vending"
invoke-virtual {v0, v1}, Landroid/content/Intent;->setPackage(Ljava/lang/String;)Landroid/content/Intent;
:try_store_start
invoke-virtual {p0, v0}, Lorg/pouya/tvhomebridge/LauncherSelectActivity;->startActivity(Landroid/content/Intent;)V
:try_store_end
return-void
.catch Ljava/lang/Exception; {:try_store_start .. :try_store_end} :store_failed
:store_failed
move-exception v0
const-string v1, "Play Store is unavailable"
const/4 v2, 0x1
invoke-static {p0, v1, v2}, Landroid/widget/Toast;->makeText(Landroid/content/Context;Ljava/lang/CharSequence;I)Landroid/widget/Toast;
move-result-object v1
invoke-virtual {v1}, Landroid/widget/Toast;->show()V
return-void
:select_launcher
invoke-virtual {p0}, Lorg/pouya/tvhomebridge/LauncherSelectActivity;->getContentResolver()Landroid/content/ContentResolver;
move-result-object v1
const-string v2, "tv_home_bridge_home_component"
invoke-static {v1, v2, v0}, Landroid/provider/Settings$Global;->putString(Landroid/content/ContentResolver;Ljava/lang/String;Ljava/lang/String;)Z
move-result v1
if-eqz v1, :failed
invoke-static {p0}, Lorg/pouya/tvhomebridge/LauncherTarget;->open(Landroid/content/Context;)V
invoke-virtual {p0}, Lorg/pouya/tvhomebridge/LauncherSelectActivity;->finish()V
return-void
:failed
const-string v2, "Could not save Home launcher"
const/4 v3, 0x1
invoke-static {p0, v2, v3}, Landroid/widget/Toast;->makeText(Landroid/content/Context;Ljava/lang/CharSequence;I)Landroid/widget/Toast;
move-result-object v2
invoke-virtual {v2}, Landroid/widget/Toast;->show()V
return-void
.end method

.method protected onRestart()V
.locals 0
invoke-super {p0}, Landroid/app/Activity;->onRestart()V
invoke-virtual {p0}, Lorg/pouya/tvhomebridge/LauncherSelectActivity;->recreate()V
return-void
.end method
