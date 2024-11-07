# Generated by Django 5.1.2 on 2024-11-05 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mailing", "0002_alter_message_options_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="mailing",
            name="date_end_message",
            field=models.DateTimeField(
                auto_now=True, verbose_name="Дата и время окончания отправки"
            ),
        ),
        migrations.AlterField(
            model_name="mailing",
            name="date_first_message",
            field=models.DateTimeField(
                auto_now_add=True, verbose_name="Дата и время первой отправки"
            ),
        ),
        migrations.AlterField(
            model_name="message",
            name="text",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="recipient",
            name="email",
            field=models.EmailField(
                max_length=254, unique=True, verbose_name="Email получателя"
            ),
        ),
        migrations.AlterField(
            model_name="recipient",
            name="full_name",
            field=models.CharField(unique=True, verbose_name="ФИО получателя"),
        ),
    ]
