#  Author : Wosvo Interactive
#  Developer : Fürkan Göktaş
#  Email : furkan@wosvo.com
#  Date : 15.02.2025 15:00
#  Filename : utils.py
#  Last Modified : 15.02.2025 15:00
#  Project : backend
#  Module : backend
#
#  Copyright (c) 2025
import google.generativeai as genai
from openai import OpenAI
from django.conf import settings
import logging
import cv2
import numpy as np
import os
from django.utils.text import slugify
from django.utils.crypto import get_random_string
from django.utils.timezone import now
from stories.models import Stories, Scenes
import re

logger = logging.getLogger(__name__)


class StoryGenerator:
    def __init__(self):
        api_key = settings.GEMINI_API_KEY
        print(f"[DEBUG] GEMINI_API_KEY exists: {bool(api_key)}")
        print(f"[DEBUG] GEMINI_API_KEY length: {len(api_key) if api_key else 0}")
        print(f"[DEBUG] GEMINI_API_KEY first 10 chars: {api_key[:10] if api_key and len(api_key) > 10 else 'N/A'}")
        
        if not api_key:
            print("[DEBUG] ERROR: GEMINI_API_KEY is empty!")
            logger.error("GEMINI_API_KEY is empty!")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash')

    def generate_story(self, topic, scene_count):
        try:
            print(f"[DEBUG] generate_story called with topic: {topic}, scene_count: {scene_count}")
            prompt = self._create_story_prompt(topic=topic, scene_count=scene_count)
            print(f"[DEBUG] Prompt created, length: {len(prompt)}")

            print("[DEBUG] Calling Gemini API...")
            response = self.model.generate_content(prompt)
            print(f"[DEBUG] Gemini API response received")
            print(f"[DEBUG] Response type: {type(response)}")
            
            story_text = response.text
            print(f"[DEBUG] Story text length: {len(story_text) if story_text else 0}")
            print(f"[DEBUG] Story text preview: {story_text[:200] if story_text else 'None'}")

            return story_text

        except Exception as e:
            print(f"[DEBUG] Error generating story: {str(e)}")
            print(f"[DEBUG] Error type: {type(e).__name__}")
            logger.error(f"Error generating story: {e}", exc_info=True)
            return None

    def _create_story_prompt(self, topic: str, scene_count: int) -> str:
        return f"""
           Generate a story based on the following criteria:

           Topic: {topic}

           1. Structure:
              - The story must consist of exactly {scene_count} scenes.
              - Each scene should be clearly marked with "SCENE X:" where X is the scene number.
              - After each "SCENE X:" marker, provide the scene title on the same line, separated by a dash (-).
              - Start the scene content on a new line after the title.

           2. Content requirements:
              - Each scene must contain a minimum of 6 sentences.
              - Ensure logical and smooth transitions between scenes.
              - The story should be coherent and engaging as a whole.

           3. Visual aspects:
              - Each scene should be easily visualizable.
              - Include detailed visual descriptions for each scene.

           4. Additional guidelines:
              - Use descriptive language to paint a clear picture of each scene.
              - Maintain consistency in characters, setting, and plot throughout the story.
              - Conclude the story in a satisfying manner within the given number of scenes.

           5. Output format:
              SCENE 1: [Scene Title]
              [Scene content...]

              SCENE 2: [Scene Title]
              [Scene content...]

              [Continue for all scenes...]

           Please generate the complete story following these instructions.
           """

    def _create_scenes(self, story, story_text):
        print(f"Story content:\n{story_text}")  # Tüm hikaye içeriğini yazdır

        # Sahne başlığını ve içeriğini ayıran regex
        scene_pattern = re.compile(r'SCENE (\d+): (.+?)\n([\s\S]+?)(?=\n\nSCENE|\Z)', re.DOTALL)
        scene_matches = scene_pattern.findall(story_text)

        print(f"Number of scenes found: {len(scene_matches)}")  # Bulunan sahne sayısını yazdır

        for number, title, content in scene_matches:
            print(f"\nProcessing Scene {number}")  # Her sahne için işlem başlangıcını belirt

            title = title.strip()
            content = content.strip()

            print(f"Title: {title}")
            print(f"Content (first 100 chars): {content[:100]}...")  # İçeriğin ilk 100 karakterini yazdır

            scene = Scenes.objects.create(
                story=story,
                scene_title=title,
                scene_number=int(number),
                content=content
            )
            print(f"Scene created with ID: {scene.id}")

        # Oluşturulan sahne sayısını kontrol et
        created_scenes = Scenes.objects.filter(story=story).count()
        print(f"\nTotal scenes created: {created_scenes}")

        if created_scenes != story.scene_count:
            print(f"Uyarı: Beklenen sahne sayısı {story.scene_count}, oluşturulan sahne sayısı {created_scenes}")

        # Eğer hiç sahne oluşturulmadıysa, hata mesajı yazdır
        if created_scenes == 0:
            print(f"Uyarı: '{story.title}' için hiç sahne oluşturulamadı.")

    def generate_scenes(self, story):
        # Generate scenes based on the story text
        return self._create_scenes(story, story.content)


class DallEGenerator:
    def __init__(self):
        api_key = settings.OPENAI_API_KEY
        print(f"[DEBUG] OPENAI_API_KEY exists: {bool(api_key)}")
        print(f"[DEBUG] OPENAI_API_KEY length: {len(api_key) if api_key else 0}")
        
        if not api_key:
            print("[DEBUG] ERROR: OPENAI_API_KEY is empty!")
            logger.error("OPENAI_API_KEY is empty!")
        
        self.client = OpenAI(api_key=api_key)

    def generate_image(self, prompt):
        try:
            print(f"[DEBUG] generate_image called with prompt length: {len(prompt)}")
            response = self.client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1024",
                quality="standard",
                n=1,
            )
            image_url = response.data[0].url
            print(f"[DEBUG] Image generated successfully: {image_url[:50]}...")
            return image_url

        except Exception as e:
            print(f"[DEBUG] Error generating image: {str(e)}")
            logger.error(f"Error generating image: {e}", exc_info=True)
            return None


def validate_file_extension(value):
    import os
    from django.core.exceptions import ValidationError

    ext = os.path.splitext(value.name)[1]
    valid_extensions = [".jpg", ".jpeg", ".png", ".gif", ".svg", ".webp"]
    if not ext.lower() in valid_extensions:
        raise ValidationError("Desteklenmeyen dosya formatı.")


def generate_unique_filename(instance, filename, field_name='title', upload_to='', custom_prefix=''):
    # Get the extension of the uploaded file
    ext = filename.split('.')[-1]

    # Get the value of the specified field (default is 'title')
    field_value = getattr(instance, field_name, '')

    # Create a slug from the field value
    slug = slugify(field_value)

    # If a custom prefix is provided, use it; otherwise, use the model name
    if custom_prefix:
        prefix = custom_prefix
    else:
        prefix = instance.__class__.__name__.lower()

    # Generate a random string
    random_string = get_random_string(length=8)

    # Construct the new filename
    new_filename = f"{prefix}-{slug}-{random_string}.{ext}"

    # Return the full path
    return os.path.join(upload_to, new_filename)


def get_upload_path(instance, filename):
    # Get the model name
    model_name = instance.__class__.__name__.lower()

    # Get the field name
    field_name = 'image'  # Default to 'image'
    for field in instance._meta.fields:
        if field.name in filename:
            field_name = field.name
            break

    # Generate the path
    return os.path.join(
        model_name,
        field_name,
        now().strftime("%Y/%m/%d"),
        filename
    )
