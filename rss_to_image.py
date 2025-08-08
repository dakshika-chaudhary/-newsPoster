import feedparser
import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import openai
import os

print("openai is working!")

openai.api_key = os.getenv("OPENAI_API_KEY")

FEED_URL = "https://www.thehindu.com/feeder/default.rss"
OUTPUT_DIR = "news_cards"
NUM_ITEMS = 6
TITLE_FONT_PATH = "C:/Windows/Fonts/arialbd.ttf"
BODY_FONT_PATH = "C:/Windows/Fonts/arial.ttf"


os.makedirs(OUTPUT_DIR, exist_ok=True)
feed = feedparser.parse(FEED_URL)
items = feed.entries[:NUM_ITEMS]

# openai---gpt-4.1-nano
def rephrase_text(text, purpose="rephrase"):
    prompt_map = {
        "rephrase": f"Rephrase this headline: {text}",
    }

    try:
        response = openai.chat.completions.create(
            model="gpt-4.1-nano-2025-04-14",
            messages=[
                {"role": "user", "content": prompt_map.get(purpose, text)}
            ],
            temperature=0.7,
            max_tokens=100
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
      print("GPT error:", e)
      return text
    
def wrap_text(text, draw, font, max_width):
   
    lines = []
    words = text.split()
    line = ""
    for word in words:
        test_line = f"{line} {word}".strip()
        if draw.textlength(test_line, font=font) <= max_width:
            line = test_line
        else:
            lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines

for i, item in enumerate(items):
    title = rephrase_text(item.title, "rephrase")
    description = rephrase_text(item.description, "rephrase")
    category = item.get("category", "News")
    pub_date = item.published
    image_url = item.media_content[0]['url'] if 'media_content' in item else None

    
    if image_url:
        response = requests.get(image_url)
        thumbnail = Image.open(BytesIO(response.content)).resize((400, 250))
    else:
        thumbnail = Image.new("RGB", (400, 250), "gray")

    
    card = Image.new("RGB", (800, 400), color="white")
    card.paste(thumbnail, (20, 75))

    draw = ImageDraw.Draw(card)

    title_font = ImageFont.truetype(TITLE_FONT_PATH, 24)
    body_font = ImageFont.truetype(BODY_FONT_PATH, 16)

    draw.text((20, 20), f"{category} - {pub_date}", font=body_font, fill="gray")

    wrapped_title = wrap_text(title, draw, title_font, 360)
    wrapped_desc = wrap_text(description, draw, body_font, 360)

    y_offset = 75
    for line in wrapped_title:
        draw.text((440, y_offset), line, font=title_font, fill="black")
        y_offset += 28

    y_offset += 10
    for line in wrapped_desc[:6]:
        draw.text((440, y_offset), line, font=body_font, fill="darkgray")
        y_offset += 22

    output_path = os.path.join(OUTPUT_DIR, f"news_{i+1}.jpg")
    card.save(output_path)
    print(f"✅ Saved: {output_path}")
