
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='LottoRound',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('round_number', models.PositiveIntegerField(unique=True)),
                ('draw_date', models.DateTimeField()),
                ('is_drawn', models.BooleanField(default=False)),
                ('winning_numbers', models.CharField(blank=True, max_length=50)),
                ('bonus_number', models.PositiveIntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numbers', models.CharField(max_length=50)),
                ('is_auto', models.CharField(choices=[('AUTO', '자동'), ('MANUAL', '수동')], max_length=10)),
                ('purchase_date', models.DateTimeField(auto_now_add=True)),
                ('rank', models.IntegerField(default=0)),
                ('round', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lotto.lottoround')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
