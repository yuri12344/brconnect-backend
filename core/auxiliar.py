import qrcode
import json
from io import BytesIO
from django.core.files import File
from django.db import models

def generate_qr_code(data) -> File:
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr_data = json.dumps(data)
    qr.add_data(qr_data)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    temp_handle = BytesIO()
    img.save(temp_handle, format='png')
    temp_handle.seek(0)
    return File(temp_handle) # Retorne a imagem do QR Code como um arquivo


class QRCodeMixin(models.Model):
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True)
    class Meta:
        abstract = True
    def get_qr_data(self):
        raise NotImplementedError("Subclasses must implement this method.")
    def save(self, *args, **kwargs):
        if self.pk is None:  # Se o objeto ainda não existe (ou seja, é uma nova criação)
            super().save(*args, **kwargs)  # Primeiro, salve o objeto para obter um ID
        qr_data = self.get_qr_data()
        qr_code_file = generate_qr_code(qr_data)# Gere a imagem do QR Code
        self.qr_code.save(f'qr_code_{self.pk}.png', qr_code_file, save=False) # Salve a imagem do QR Code no campo qr_code
        super().save(*args, **kwargs)