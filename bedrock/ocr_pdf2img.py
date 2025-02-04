import json
import boto3
from pathlib import Path
from pdf2image import convert_from_path
import io
from PIL import Image

def perform_ocr() -> dict:      
    client = boto3.client(
        service_name='bedrock-runtime',
        region_name='us-west-2'
    )

    images = convert_from_path("samples/image.pdf")
    
    # 最初のページを使用（複数ページの場合は必要に応じて処理を追加）
    first_page = images[0]
    
    # 画像を一時的にファイルとして保存
    first_page.save("samples/temp.png", format='PNG')
    
    with open("samples/temp.png", 'rb') as f:
        img_bytes = f.read()

    try:
        response = client.converse(
            modelId="anthropic.claude-3-5-sonnet-20241022-v2:0",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "image": {
                                "format": "png",
                                "source": {
                                    "bytes": img_bytes
                                },
                            }
                        },
                        {
                            "text": """このpngに含まれているテキストを全て抽出してください。
    日本語が書かれているので、そのまま日本語で出力してください。
    抽出したテキストは、できるだけ元の文書のレイアウトを保持するように出力してください。"""
                        }
                    ]
                }
            ]
        )

        response_body = response["output"]["message"]["content"][0]["text"]
        return response_body

    except Exception as e:
        print(f"Error performing OCR: {str(e)}")
        return None

    finally:
        # 一時ファイルの削除
        try:
            Path("samples/temp.png").unlink()
        except:
            pass

def main():
    result = perform_ocr()
    
    if result:
        print("OCR結果:")
        print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
