import re
import sys
import requests
from typing import List, Dict, Tuple
from colorama import Fore, Style, init


def get_course_mapping(course_key: str) -> str:
    course_mapping = {
        "one": "1-relational-databases-for-analysts",
        "two": "2-expert-sql-for-analysts",
        "three": "3-dimensional-modeling"
    }
    return course_mapping.get(course_key)


def get_correct_answers(course: str) -> Dict[str, str]:
    try:
        response = requests.get(f"https://api.instituteofdataarchitecture.com/api/training/{course}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise SystemExit(f"Error fetching answers: {e}")


def parse_answers_file(file_path: str) -> Dict[str, str]:
    try:
        with open(file_path, 'r') as file:
            content = file.read()
        pattern = re.compile(r'(\d+\.\d+\.\d+):\s*((?:(?!\d+\.\d+\.\d+:).)*)', re.DOTALL)
        return {match[0]: match[1].strip() for match in pattern.findall(content)}
    except IOError as e:
        raise SystemExit(f"Error reading file: {e}")


def compare_answers(student_answers: Dict[str, str], correct_answers: Dict[str, str]) -> Tuple[int, int, int, List[str], List[str]]:
    passed, failed, skipped = 0, 0, 0
    failed_tests, skipped_tests = [], []

    for question, student_answer in student_answers.items():
        if student_answer == '':
            skipped += 1
            skipped_tests.append(f'{answers_file_path}[{question}]')
        elif student_answer == correct_answers.get(question, ''):
            passed += 1
        else:
            failed += 1
            failed_tests.append(f'{answers_file_path}[{question}]')

    return passed, failed, skipped, failed_tests, skipped_tests


def print_results(passed: int, failed: int, skipped: int, failed_tests: List[str], skipped_tests: List[str], total_questions: int):
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

    if failed == 0 and skipped == 0 and passed != 0 and passed != total_questions:
        print(Style.BRIGHT + Fore.BLUE + f"\nSo far everything is correct, keep going 👍")
    elif failed == 0 and skipped == 0 and passed == total_questions:
        print(Style.BRIGHT + Fore.BLUE + f"\nYou did it, you answered all {total_questions} questions correctly, you are amazing 🎉")

    print()


if __name__ == "__main__":
    init(autoreset=True)
    course_key = sys.argv[1] if len(sys.argv) > 1 else sys.exit("Course key not provided.")
    course = get_course_mapping(course_key)
    if not course:
        sys.exit("Invalid course parameter passed.")

    answers_file_path = f'/workspace/work/{course}/answers.txt'
    correct_answers = get_correct_answers(course)
    student_answers = parse_answers_file(answers_file_path)
    passed, failed, skipped, failed_tests, skipped_tests = compare_answers(student_answers, correct_answers)
    print_results(passed, failed, skipped, failed_tests, skipped_tests, len(correct_answers))
