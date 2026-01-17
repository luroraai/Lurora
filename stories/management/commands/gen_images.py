#  Author : Wosvo Interactive
#  Developer : Fürkan Göktaş
#  Email : furkan@wosvo.com
#  Date : 17.02.2025 02:04
#  Filename : gen_images.py
#  Last Modified : 17.02.2025 02:04
#  Project : backend
#  Module : backend
#
#  Copyright (c) 2025
import cv2
import os
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Görsele belirli bir metni gizler ve kaydeder."

    def add_arguments(self, parser):
        parser.add_argument("image_path", type=str, help="İşlenecek görüntü dosyasının yolu")
        parser.add_argument("text", type=str, help="Gizlenecek metin")
        parser.add_argument("output_path", type=str, help="Kaydedilecek yeni dosyanın yolu")
        parser.add_argument("--position", type=int, nargs=2, default=(50, 50), help="Metnin konumu (x, y)")
        parser.add_argument("--font_scale", type=float, default=0.6, help="Yazı boyutu")
        parser.add_argument("--color", type=int, nargs=3, default=(30, 30, 30), help="Metin rengi (B, G, R)")
        parser.add_argument("--thickness", type=int, default=1, help="Yazı kalınlığı")

    def handle(self, *args, **options):
        image_path = options["image_path"]
        text = options["text"]
        output_path = options["output_path"]
        position = tuple(options["position"])
        font_scale = options["font_scale"]
        color = tuple(options["color"])
        thickness = options["thickness"]

        if not os.path.exists(image_path):
            self.stderr.write(self.style.ERROR(f"Görsel bulunamadı: {image_path}"))
            return

        # Görseli yükle
        image = cv2.imread(image_path)
        if image is None:
            self.stderr.write(self.style.ERROR("Görsel yüklenemedi!"))
            return

        # Metni görsele ekleyelim
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(image, text, position, font, font_scale, color, thickness, cv2.LINE_AA)

        # Yeni görseli kaydet
        cv2.imwrite(output_path, image)
        self.stdout.write(self.style.SUCCESS(f"Metin başarıyla gizlendi: {output_path}"))
