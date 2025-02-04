import json
import boto3
from pathlib import Path

def perform_ocr() -> dict:      
    client = boto3.client(
        service_name='bedrock-runtime',
        region_name='us-west-2'
    )

    with open("samples/image.pdf", 'rb') as f: # samples/text.pdf であれば、出力される
        pdf = f.read()

    try:
        response = client.converse(
            modelId="anthropic.claude-3-5-sonnet-20241022-v2:0",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "document": {
                                "name": "PDF Document",
                                "format": "pdf",
                                "source": {
                                    "bytes": pdf
                                },
                            }
                        },
                        {
                            "text": """このPDFに含まれているテキストを全て抽出してください。
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

def main():
    result = perform_ocr()
    
    if result:
        print("OCR結果:")
        print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
