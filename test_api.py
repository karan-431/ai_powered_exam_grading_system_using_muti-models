import httpx
import asyncio
from PIL import Image, ImageDraw
import io

async def test_evaluate():
    # Create a dummy image
    img = Image.new('RGB', (400, 200), color=(255, 255, 255))
    d = ImageDraw.Draw(img)
    d.text((10,10), "Q1: The capital of France is Paris.", fill=(0,0,0))
    d.text((10,40), "Q2: The speed of light is 3e8 m/s.", fill=(0,0,0))
    
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='JPEG')
    img_byte_arr.seek(0)

    url = "http://127.0.0.1:8000/evaluate"
    
    files = {
        'answer_sheet': ('dummy.jpg', img_byte_arr, 'image/jpeg')
    }
    
    data = {
        'roll_number': '12346',
        'max_marks': '10',
        'answer_key_text': "Q1: Paris (5 marks)\nQ2: 3e8 m/s (5 marks)"
    }
    
    print("Sending POST request to /evaluate...")
    async with httpx.AsyncClient(timeout=300) as client:
        try:
            response = await client.post(url, data=data, files=files)
            print(f"Status Code: {response.status_code}")
            try:
                print("Response JSON:", response.json())
            except:
                print("Response Text:", response.text)
        except Exception as e:
            print("Request Failed:", e)

if __name__ == "__main__":
    asyncio.run(test_evaluate())
