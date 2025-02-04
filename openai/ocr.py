import json
from pathlib import Path
from pdf2image import convert_from_path
from openai import OpenAI
import base64

def encode_image_to_base64(image_path: str) -> str:
    """画像をbase64エンコードする"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def perform_ocr() -> dict:
    client = OpenAI()
    
    # PDFを画像に変換（最初のページのみ）
    images = convert_from_path("samples/image.pdf")
    first_page = images[0]
    temp_file = "samples/temp.png"

    try:
        # 画像を一時的にファイルとして保存
        first_page.save(temp_file, format='PNG')
        
        # 画像をbase64エンコード
        base64_image = encode_image_to_base64(temp_file)

        # OpenAI Vision APIを使用してOCR処理
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": """このPDFに含まれているテキストを全て抽出してください。
日本語が書かれているので、そのまま日本語で出力してください。
抽出したテキストは、できるだけ元の文書のレイアウトを保持するように出力してください。"""
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=4096
        )

        return response.choices[0].message.content

    except Exception as e:
        print(f"Error performing OCR: {str(e)}")
        return None

    finally:
        # 一時ファイルの削除
        try:
            Path(temp_file).unlink()
        except:
            pass

def main():
    result = perform_ocr()
    
    if result:
        print("OCR結果:")
        print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
