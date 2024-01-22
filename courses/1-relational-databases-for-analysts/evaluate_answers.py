import re
import requests
from typing import List, Dict
from colorama import Fore, Style, init

init(autoreset=True)

ANSWERS_FILE_PATH = '/workspace/work/1-relational-databases-for-analysts/answers.txt'

def get_correct_answers() -> Dict[str, str]:
    response = requests.get("https://api.instituteofdataarchitecture.com/api/training/1-relational-databases-for-analysts")
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Failed to fetch correct answers from the API")

def evaluate_answers() -> None:
    with open(ANSWERS_FILE_PATH, 'r') as file:
        content = file.read()

    pattern = re.compile(r'(\d+\.\d+\.\d+):\s*((?:(?!\d+\.\d+\.\d+:).)*)', re.DOTALL)
    answers = {match[0]: match[1].strip() for match in pattern.findall(content)}
    passed, failed, skipped = 0, 0, 0
    failed_tests: List[str] = []
    skipped_tests: List[str] = []

    correct_answers: Dict[str, str] = get_correct_answers()

    for question, student_answer in answers.items():
        if student_answer == '':
            skipped += 1
            skipped_tests.append(f'{ANSWERS_FILE_PATH}[{question}]')
        elif student_answer == correct_answers.get(question, ''):
            passed += 1
        else:
            failed += 1
            failed_tests.append(f'{ANSWERS_FILE_PATH}[{question}]')

    print()
    print(Style.BRIGHT + Fore.BLUE + "Test Summary:")
    print(Fore.GREEN + f"Passed: {passed}")
    print(Fore.RED + f"Failed: {failed}")
    print(Fore.YELLOW + f"Skipped: {skipped}")

    if failed_tests:
        print(Style.BRIGHT + Fore.BLUE + "\nFailed Tests:")
        for test in failed_tests:
            print(Fore.RED + f"- {test}")

    if skipped_tests:
        print(Style.BRIGHT + Fore.BLUE + "\nSkipped Tests:")
        for test in skipped_tests:
            print(Fore.YELLOW + f"- {test}")

    if failed == 0 and skipped == 0:
        print(Style.BRIGHT + Fore.BLUE + f"\nYou did it, you answered all {len(correct_answers)} questions correctly, you are amazing 🎉")

    print()

if __name__ == "__main__":
    evaluate_answers()
