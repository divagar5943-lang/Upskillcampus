# Quiz Game - Python Project
# Run with: python QuizGame.py

QUESTIONS = [
    {
        "question": "Which language is commonly used for data analysis?",
        "options": ["A. HTML", "B. Python", "C. CSS", "D. XML"],
        "answer": "B"
    },
    {
        "question": "Which data type stores True or False?",
        "options": ["A. int", "B. str", "C. bool", "D. list"],
        "answer": "C"
    },
    {
        "question": "Which keyword defines a function in Python?",
        "options": ["A. function", "B. def", "C. fun", "D. make"],
        "answer": "B"
    },
    {
        "question": "Which symbol starts a single-line comment in Python?",
        "options": ["A. //", "B. <!--", "C. #", "D. **"],
        "answer": "C"
    },
    {
        "question": "Which collection stores key-value pairs?",
        "options": ["A. tuple", "B. dictionary", "C. set", "D. string"],
        "answer": "B"
    }
]

def run_quiz():
    score = 0
    print("\n=== PYTHON QUIZ GAME ===")
    print("Enter A, B, C, or D for each question.\n")

    for number, item in enumerate(QUESTIONS, start=1):
        print(f"{number}. {item['question']}")
        for option in item["options"]:
            print("   " + option)

        while True:
            choice = input("Your answer: ").strip().upper()
            if choice in {"A", "B", "C", "D"}:
                break
            print("Please enter A, B, C, or D.")

        if choice == item["answer"]:
            print("Correct!\n")
            score += 1
        else:
            print(f"Incorrect. Correct answer: {item['answer']}\n")

    print(f"Quiz completed! Your score is {score}/{len(QUESTIONS)}.")
    percentage = score / len(QUESTIONS) * 100
    print(f"Percentage: {percentage:.0f}%")

if __name__ == "__main__":
    run_quiz()
