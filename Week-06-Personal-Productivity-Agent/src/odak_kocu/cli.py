"""OdakKoçu komut satırı arayüzü."""

from __future__ import annotations

import argparse

try:
    from dotenv import load_dotenv
except ImportError:
    def load_dotenv() -> bool:
        return False

from .agent import FocusAgent


def main() -> None:
    load_dotenv()
    parser = argparse.ArgumentParser(description="Türkçe Pomodoro ve rutin agent'ı")
    parser.add_argument("question", nargs="*", help="Agent'a verilecek komut")
    parser.add_argument("--chat", action="store_true", help="Etkileşimli sohbet modunu aç")
    args = parser.parse_args()
    agent = FocusAgent()
    if args.chat:
        print("OdakKoçu hazır. Çıkmak için 'çık' yazın.")
        while True:
            question = input("\nSiz: ").strip()
            if question.lower() in {"çık", "exit", "quit"}:
                break
            result = agent.run(question)
            print(f"OdakKoçu [{result.mode}] ({', '.join(result.tool_calls) or 'tool yok'}):\n{result.answer}")
        return
    question = " ".join(args.question).strip() or input("Komutunuz: ").strip()
    result = agent.run(question)
    print(f"[mod: {result.mode}] [tool'lar: {', '.join(result.tool_calls) or 'yok'}]\n")
    print(result.answer)


if __name__ == "__main__":
    main()
