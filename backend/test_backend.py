import requests
import os

BASE_URL = "http://127.0.0.1:8000"


def main():
    print("--- Flora-Bot CLI Tester ---")

    # 1. Get Image
    while True:
        image_path = input("Enter the full path to your plant image file: ").strip()
        # Remove quotes if user copied as path
        image_path = image_path.strip('"').strip("'")
        if os.path.exists(image_path):
            break
        print(f"Error: File not found at {image_path}")

    # 2. Predict
    print(f"\nAnalyzing {image_path}...")
    try:
        with open(image_path, "rb") as f:
            files = {"file": f}
            response = requests.post(f"{BASE_URL}/predict", files=files)

        if response.status_code != 200:
            print(f"Error from server: {response.status_code}")
            print(response.text)
            return

        data = response.json()

        diagnosis = data.get("diagnosis")
        confidence = data.get("confidence")
        explanation = data.get("explanation")
        chat_context = data.get("chat_context")

        print("\n" + "=" * 50)
        print(f"Diagnosis: {diagnosis} ({confidence})")
        print("=" * 50)
        print(f"Initial Explanation:\n{explanation}")
        print("=" * 50)

    except Exception as e:
        print(f"Failed to connect to backend: {e}")
        return

    # 3. Chat Loop
    print("\nYou can now ask follow-up questions about this diagnosis.")
    print("Type 'exit' or 'quit' to stop.")

    while True:
        question = input("\nYour Question: ").strip()
        if question.lower() in ["exit", "quit", "q"]:
            break

        if not question:
            continue

        payload = {
            "question": question,
            "context": chat_context,
            "diagnosis": diagnosis,
        }

        try:
            chat_response = requests.post(f"{BASE_URL}/chat", json=payload)
            if chat_response.status_code == 200:
                answer = chat_response.json().get("answer")
                print(f"\nFlora-Bot: {answer}")
            else:
                print(f"Error: {chat_response.text}")
        except Exception as e:
            print(f"Chat error: {e}")


if __name__ == "__main__":
    main()
