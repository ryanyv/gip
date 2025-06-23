from django.db import migrations, models


def forwards_func(apps, schema_editor):
    User = apps.get_model("accounts", "User")
    User.objects.filter(role="staff").update(role="user")


def backwards_func(apps, schema_editor):
    User = apps.get_model("accounts", "User")
    User.objects.filter(role="user").update(role="staff")


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0003_add_extra_fields"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="role",
            field=models.CharField(
                choices=[
                    ("superadmin", "Super Admin"),
                    ("admin", "Admin"),
                    ("user", "User"),
                ],
                default="user",
                max_length=20,
            ),
        ),
        migrations.RunPython(forwards_func, backwards_func),
    ]
