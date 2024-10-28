from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = """
    Добавления моделей группы Модератора
    """

    def handle(self, *args, **options):


        # Список групп и их права
        group_list = {
            "Product Moderator":
                [
                    "can_publish_product",
                    "can_delete_product",
                ],
            "Content Manager":
                [
                    "can_publish_blog",
                    "delete_blog",
                ]
        }

        # Удаляем уже созданную группу если таковая имеется
        for group_name, permissions_list in group_list.items():
            is_exists = any([x.name == group_name for x in Group.objects.all()])
            if is_exists:
                user_input = input('Данная группа уже существует. Удаляем? [Y/n]: ')
                if user_input in ['Y', '']:
                    Group.objects.get(name=group_name).delete()
                else:
                    return print('Неопределённый ответ. Команда не выполнена')

            moderators = Group.objects.create(name=group_name)
            for perm in permissions_list:
                moderators.permissions.add(Permission.objects.get(codename=perm))

            moderators.save()

            print(f'\nГруппа "{group_name}" с правами ({', '.join(permissions_list)}) успешно создана')

        self.stdout.write(self.style.SUCCESS('Группы модераторов продуктов успешно созданы'))