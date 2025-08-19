from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from django.contrib.auth.models import User
from .models import Producto

# Notificacion cuando se modifico un producto
@receiver(post_save, sender=Producto)
def notificar_producto_guardado(sender, instance, created, **kwargs):
    if hasattr(instance, "_actor"):
        actor = instance._actor
    else:
        actor = None

    if created: #email
        subject = "Nuevo producto creado"

        valores = [
            f"nombre_producto: {instance.nombre_producto}",
            f"precio_producto_mxn: {instance.precio_producto_mxn}",
            f"marca: {instance.marca}",
        ]
        valores_texto = "\n".join(valores)

        message = (
            f"El producto '{instance.nombre_producto}' ha sido creado "
            f"por {actor.username if actor else 'un administrador'}.\n\n"
            f"Valores:\n{valores_texto}"
        )
    else:
        subject = "Producto modificado"

        # mostrar antes y despues
        old_values = getattr(instance, "_old_values", {})
        cambios = []
        for campo, old_val in old_values.items():
            new_val = getattr(instance, campo)
            if str(old_val) != str(new_val):  # only list changed fields
                cambios.append(f"{campo}: '{old_val}' → '{new_val}'")

        cambios_texto = "\n".join(cambios) if cambios else "Sin cambios detectados."

        message = (
            f"El producto '{instance.nombre_producto}' ha sido modificado "
            f"por {actor.username if actor else 'un administrador'}.\n\n"
            f"Cambios:\n{cambios_texto}"
        )
    # send to all admins except actor
    #admins = User.objects.filter(is_staff=True).exclude(id=getattr(actor, "id", None))
    admins = User.objects.filter(is_staff=True)
    destinatarios = [u.email for u in admins if u.email]

    if destinatarios:
        send_mail(subject, message, "no-reply@miapp.com", destinatarios)

# notificar cuando se borra
@receiver(post_delete, sender=Producto)
def notificar_producto_eliminado(sender, instance, **kwargs):
    actor = getattr(instance, "_actor", None)

    subject = "Producto eliminado"
    message = (
        f"El producto '{instance.nombre_producto}' "
        f"ha sido eliminado por {actor.username if actor else 'un administrador'}."
    )

    #admins = User.objects.filter(is_staff=True).exclude(id=getattr(actor, "id", None))
    admins = User.objects.filter(is_staff=True)
    destinatarios = [u.email for u in admins if u.email]

    if destinatarios:
        send_mail(subject, message, "no-reply@miapp.com", destinatarios)
