import openai
import os

# 設定 OpenAI API 密鑰
# openai.api_key = os.environ["OPENAI_API_KEY"]
openai.api_key = "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"

# 輸入文本
input_text = "請用中文說一個好笑的笑話"

# 設定 GPT-3.5 模型的檢索引擎
model_engine = "text-davinci-003"

# 設定生成的文本長度
output_length = 500

# 使用 GPT-3.5 模型生成文本
response = openai.Completion.create(
    engine=model_engine,
    prompt=input_text,
    max_tokens=output_length,
)

# 取得生成的文本
output_text = response.choices[0].text.strip()

# 印出生成的文本
print(output_text)