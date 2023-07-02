# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import Book, BookInstance, Reader, Order
#
#
# @receiver(post_save, sender=Book)
# def create_book_instance(sender, instance, created, **kwargs):
#     if created:
#         for i in range(instance.quantity):
#             BookInstance.objects.create(book=instance)
#             print('Создан экземпляр')
#             print(instance)
#             print(sender)
