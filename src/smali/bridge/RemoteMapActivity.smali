.class public Lorg/pouya/tvhomebridge/RemoteMapActivity;
.super Landroid/app/ListActivity;

.field private rows:Ljava/util/ArrayList;
.field private actions:Ljava/util/ArrayList;

.method public constructor <init>()V
.locals 0
invoke-direct {p0}, Landroid/app/ListActivity;-><init>()V
return-void
.end method

.method protected onCreate(Landroid/os/Bundle;)V
.locals 6
invoke-super {p0, p1}, Landroid/app/ListActivity;->onCreate(Landroid/os/Bundle;)V
const-string v0, "Four-color button: choose action"
invoke-virtual {p0, v0}, Lorg/pouya/tvhomebridge/RemoteMapActivity;->setTitle(Ljava/lang/CharSequence;)V
new-instance v0, Ljava/util/ArrayList;
invoke-direct {v0}, Ljava/util/ArrayList;-><init>()V
iput-object v0, p0, Lorg/pouya/tvhomebridge/RemoteMapActivity;->rows:Ljava/util/ArrayList;
new-instance v1, Ljava/util/ArrayList;
invoke-direct {v1}, Ljava/util/ArrayList;-><init>()V
iput-object v1, p0, Lorg/pouya/tvhomebridge/RemoteMapActivity;->actions:Ljava/util/ArrayList;
const-string v2, "TV Settings"
invoke-virtual {v0, v2}, Ljava/util/ArrayList;->add(Ljava/lang/Object;)Z
const-string v2, "settings"
invoke-virtual {v1, v2}, Ljava/util/ArrayList;->add(Ljava/lang/Object;)Z
const-string v2, "Original colored ribbon"
invoke-virtual {v0, v2}, Ljava/util/ArrayList;->add(Ljava/lang/Object;)Z
const-string v2, "original"
invoke-virtual {v1, v2}, Ljava/util/ArrayList;->add(Ljava/lang/Object;)Z
const-string v2, "Sambazar Home overlay"
invoke-virtual {v0, v2}, Ljava/util/ArrayList;->add(Ljava/lang/Object;)Z
const-string v2, "sambazar"
invoke-virtual {v1, v2}, Ljava/util/ArrayList;->add(Ljava/lang/Object;)Z
const-string v2, "android.intent.category.LEANBACK_LAUNCHER"
invoke-direct {p0, v2}, Lorg/pouya/tvhomebridge/RemoteMapActivity;->addApps(Ljava/lang/String;)V
const-string v2, "android.intent.category.LAUNCHER"
invoke-direct {p0, v2}, Lorg/pouya/tvhomebridge/RemoteMapActivity;->addApps(Ljava/lang/String;)V
new-instance v3, Landroid/widget/ArrayAdapter;
const v4, 0x1090003
invoke-direct {v3, p0, v4, v0}, Landroid/widget/ArrayAdapter;-><init>(Landroid/content/Context;ILjava/util/List;)V
invoke-virtual {p0, v3}, Lorg/pouya/tvhomebridge/RemoteMapActivity;->setListAdapter(Landroid/widget/ListAdapter;)V
return-void
.end method

.method private addApps(Ljava/lang/String;)V
.locals 10
new-instance v0, Landroid/content/Intent;
const-string v1, "android.intent.action.MAIN"
invoke-direct {v0, v1}, Landroid/content/Intent;-><init>(Ljava/lang/String;)V
invoke-virtual {v0, p1}, Landroid/content/Intent;->addCategory(Ljava/lang/String;)Landroid/content/Intent;
invoke-virtual {p0}, Lorg/pouya/tvhomebridge/RemoteMapActivity;->getPackageManager()Landroid/content/pm/PackageManager;
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
new-instance v5, Landroid/content/ComponentName;
iget-object v6, v4, Landroid/content/pm/ActivityInfo;->packageName:Ljava/lang/String;
iget-object v7, v4, Landroid/content/pm/ActivityInfo;->name:Ljava/lang/String;
invoke-direct {v5, v6, v7}, Landroid/content/ComponentName;-><init>(Ljava/lang/String;Ljava/lang/String;)V
invoke-virtual {v5}, Landroid/content/ComponentName;->flattenToString()Ljava/lang/String;
move-result-object v5
new-instance v8, Ljava/lang/StringBuilder;
const-string v9, "app:"
invoke-direct {v8, v9}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V
invoke-virtual {v8, v5}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;
invoke-virtual {v8}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;
move-result-object v5
iget-object v8, p0, Lorg/pouya/tvhomebridge/RemoteMapActivity;->actions:Ljava/util/ArrayList;
invoke-virtual {v8, v5}, Ljava/util/ArrayList;->contains(Ljava/lang/Object;)Z
move-result v9
if-nez v9, :loop
invoke-virtual {v3, v1}, Landroid/content/pm/ResolveInfo;->loadLabel(Landroid/content/pm/PackageManager;)Ljava/lang/CharSequence;
move-result-object v3
invoke-interface {v3}, Ljava/lang/CharSequence;->toString()Ljava/lang/String;
move-result-object v3
iget-object v9, p0, Lorg/pouya/tvhomebridge/RemoteMapActivity;->rows:Ljava/util/ArrayList;
invoke-virtual {v9, v3}, Ljava/util/ArrayList;->add(Ljava/lang/Object;)Z
invoke-virtual {v8, v5}, Ljava/util/ArrayList;->add(Ljava/lang/Object;)Z
goto :loop
:done
return-void
.end method

.method protected onListItemClick(Landroid/widget/ListView;Landroid/view/View;IJ)V
.locals 5
invoke-super/range {p0 .. p5}, Landroid/app/ListActivity;->onListItemClick(Landroid/widget/ListView;Landroid/view/View;IJ)V
iget-object v0, p0, Lorg/pouya/tvhomebridge/RemoteMapActivity;->actions:Ljava/util/ArrayList;
invoke-virtual {v0, p3}, Ljava/util/ArrayList;->get(I)Ljava/lang/Object;
move-result-object v0
check-cast v0, Ljava/lang/String;
invoke-virtual {p0}, Lorg/pouya/tvhomebridge/RemoteMapActivity;->getContentResolver()Landroid/content/ContentResolver;
move-result-object v1
const-string v2, "tv_home_bridge_color_action"
invoke-static {v1, v2, v0}, Landroid/provider/Settings$Global;->putString(Landroid/content/ContentResolver;Ljava/lang/String;Ljava/lang/String;)Z
move-result v1
if-eqz v1, :failed
iget-object v2, p0, Lorg/pouya/tvhomebridge/RemoteMapActivity;->rows:Ljava/util/ArrayList;
invoke-virtual {v2, p3}, Ljava/util/ArrayList;->get(I)Ljava/lang/Object;
move-result-object v2
check-cast v2, Ljava/lang/String;
const/4 v3, 0x0
invoke-static {p0, v2, v3}, Landroid/widget/Toast;->makeText(Landroid/content/Context;Ljava/lang/CharSequence;I)Landroid/widget/Toast;
move-result-object v2
invoke-virtual {v2}, Landroid/widget/Toast;->show()V
invoke-virtual {p0}, Lorg/pouya/tvhomebridge/RemoteMapActivity;->finish()V
return-void
:failed
const-string v2, "Could not save button action"
const/4 v3, 0x1
invoke-static {p0, v2, v3}, Landroid/widget/Toast;->makeText(Landroid/content/Context;Ljava/lang/CharSequence;I)Landroid/widget/Toast;
move-result-object v2
invoke-virtual {v2}, Landroid/widget/Toast;->show()V
return-void
.end method
