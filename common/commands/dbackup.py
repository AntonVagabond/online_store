from datetime import datetime

from django.core.management import BaseCommand, call_command


class Command(BaseCommand):
    """
    Команда для резервной копии базы данных.
    """

    def handle(self, *args, **options):
        """
        Метод для запуска пользовательской команды.
        """
        self.stdout.write('Ожидание копии базы данных')
        call_command(
            'dumpdata',
            '--natural-foreign',
            '--natural-primary',
            '--indent=2',
            '--exclude=contenttypes',
            '--exclude=admin.logentry',
            f'--output=database-{datetime.now().strftime("%Y-%m-%d-%H-%M-%S")}.json'
        )
        self.stdout.write(
            self.style.SUCCESS('Успешное резервное копирование базы данных')
        )
