text = "🍅🐍 UTF-8 — распространённый стандарт кодирования символов."
encoding = "utf-8"

with open("text.txt", "w", encoding=encoding) as f:
    f.write(text)

encode_text = text.encode(encoding)  # Кодирование
print(len(encode_text))

decode_text = encode_text.decode(encoding)  # Декодирование
print(len(decode_text))
