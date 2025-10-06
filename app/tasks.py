import os
import uuid
from .celery_app import app as celery_app
from PIL import Image, ImageDraw, ImageFont  

@celery_app.task(bind=True, name='app.tasks.process_image')
def process_image(self, filepath: str):
    try:
        im = Image.open(filepath).convert("RGBA") 
        resized_im = im.resize((500, 500))

        watermark_text = "Image Processor"
        draw = ImageDraw.Draw(resized_im)

        try:
            font = ImageFont.truetype("arial.ttf", 24)
        except IOError:
            font = ImageFont.load_default()

        text_color = (255, 255, 255, 128)  
        try:
            bbox = draw.textbbox((0, 0), watermark_text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
        except AttributeError:
            text_width, text_height = draw.textsize(watermark_text, font=font)

        image_width, image_height = resized_im.size
        margin = 20
        position = (image_width - text_width - margin, image_height - text_height - margin)
        draw.text(position, watermark_text, font=font, fill=text_color)

        output_dir = "static"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        unique_filename = f"watermarked_{uuid.uuid4().hex}.png"
        output_path = os.path.join(output_dir, unique_filename)

        resized_im.save(output_path)
        print(f"Successfully processed and saved image to: {output_path}")

        return output_path

    except FileNotFoundError:
        print(f"Error: The input file was not found at {filepath}")
        raise
    except Exception as e:
        print(f"An unexpected error occurred during image processing: {e}")
        raise

# if __name__ == "__main__":
#     print("Dispatching test task to Celery queue...")
#     test_file = 'app/test.png'
#     task = process_image.delay(test_file)
#     print(f"Task ID: {task.id}")
#     print("To check status, run a worker: celery -A app.celery_app worker -l info")
