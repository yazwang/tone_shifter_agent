import os
from openai import OpenAI, AuthenticationError, RateLimitError
from langdetect import detect
from textblob import TextBlob

# --- OpenAI client (可无密钥运行：会自动走本地回退) ---
api_key = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=api_key) if api_key else None

# --- 语言检测 ---
def detect_language(text: str) -> str:
    try:
        lang = detect(text)  # 可能返回 zh-cn / zh-tw
        return "zh" if str(lang).lower().startswith("zh") else "en"
    except Exception:
        return "en"

# --- 自动语气（情感→tone）---
def auto_tone(text: str) -> str:
    try:
        polarity = TextBlob(text).sentiment.polarity
    except Exception:
        polarity = 0.0
    if polarity < -0.3:
        return "empathetic"
    if polarity > 0.3:
        return "professional"
    return "neutral"

# --- 本地回退（无 key / 配额耗尽 / 网络异常）---
def local_reply(user_input: str, tone: str, lang: str, use_case: str) -> str:
    if lang == "zh":
        prefix = {"neutral": "（中性）", "empathetic": "（共情）", "professional": "（专业）"}[tone]
        if use_case == "finance":
            return f"{prefix} 感谢您的咨询。为保护账户安全，请勿分享敏感信息。我们已记录需求，接下来将给出清晰、可执行、合规的下一步。"
        return f"{prefix} 我理解：{user_input}。建议先梳理重点，并分步骤推进。"
    else:
        prefix = {"neutral": "(Neutral)", "empathetic": "(Empathetic)", "professional": "(Professional)"}[tone]
        if use_case == "finance":
            return f"{prefix} Thanks for reaching out. For security, please avoid sharing sensitive info. I’ll provide clear, compliant, actionable next steps."
        return f"{prefix} I understand: {user_input}. A practical next step is to prioritize and proceed incrementally."

# --- 核心回复（优先走 OpenAI，可回退本地）---
def tone_shifted_reply(user_input: str, tone: str = "neutral", use_case: str = "general") -> str:
    lang = detect_language(user_input)

    if tone == "auto":
        tone = auto_tone(user_input)

    # Finance 场景提示更专业
    role = "a financial support assistant who is concise, compliant and action-oriented" if use_case == "finance" \
           else "a helpful assistant"

    prompt = (
        f"Respond to the user in a {tone} tone as {role}.\n"
        f"User said ({lang.upper()}): {user_input}"
    )

    if client:
        try:
            resp = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
            )
            return resp.choices[0].message.content
        except (AuthenticationError, RateLimitError):
            return local_reply(user_input, tone, lang, use_case)
        except Exception:
            return local_reply(user_input, tone, lang, use_case)
    else:
        return local_reply(user_input, tone, lang, use_case)

# --- 交互主循环 ---
if __name__ == "__main__":
    print("Tone Shifter Agent started. Type 'quit' to exit.")
    last_tone = "auto"      # 默认自动语气
    last_mode = "general"   # 默认通用场景

    while True:
        mode_in = input(f"Mode (general / finance) [{last_mode}]: ").strip().lower()
        use_case = mode_in or last_mode
        if use_case not in {"general", "finance"}:
            print("Invalid mode, fallback to 'general'.")
            use_case = "general"
        last_mode = use_case

        text = input("You: ").strip()
        if text.lower() == "quit":
            break
        if not text:
            print("Please enter a message.")
            continue

        tone_in = input(f"Tone (neutral / empathetic / professional / auto) [{last_tone}]: ").strip().lower()
        tone = tone_in or last_tone
        if tone not in {"neutral", "empathetic", "professional", "auto"}:
            print("Invalid tone, fallback to 'auto'.")
            tone = "auto"
        last_tone = tone

        reply = tone_shifted_reply(text, tone, use_case)
        print("Bot:", reply)
