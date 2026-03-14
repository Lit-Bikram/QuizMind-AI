from typing import Dict, List, Any


def score_quiz(mcqs: List[Dict], user_answers: Dict[str, str]) -> Dict[str, Any]:
    total_questions = len(mcqs)
    correct_count = 0
    incorrect_count = 0

    difficulty_stats = {
        "easy": {"total": 0, "correct": 0},
        "medium": {"total": 0, "correct": 0},
        "hard": {"total": 0, "correct": 0}
    }

    question_reviews = []
    weak_areas = []

    for idx, mcq in enumerate(mcqs, start=1):
        qid = str(idx)

        correct_answer = mcq.get("correct_answer", "").strip().upper()
        user_answer = user_answers.get(qid, "").strip().upper()
        difficulty = mcq.get("difficulty", "medium").strip().lower()

        if difficulty not in difficulty_stats:
            difficulty = "medium"

        difficulty_stats[difficulty]["total"] += 1

        is_correct = user_answer == correct_answer

        if is_correct:
            correct_count += 1
            difficulty_stats[difficulty]["correct"] += 1
        else:
            incorrect_count += 1
            weak_areas.append(mcq.get("question", "Unknown topic"))

        question_reviews.append({
            "question_id": qid,
            "question": mcq.get("question"),
            "user_answer": user_answer if user_answer else None,
            "correct_answer": correct_answer,
            "is_correct": is_correct,
            "difficulty": difficulty,
            "explanation": mcq.get("explanation"),
            "confidence_score": mcq.get("confidence_score"),
            "is_verified": mcq.get("is_verified")
        })

    percentage = round((correct_count / total_questions) * 100, 2) if total_questions > 0 else 0.0

    difficulty_breakdown = {}
    for level, stats in difficulty_stats.items():
        total = stats["total"]
        correct = stats["correct"]
        accuracy = round((correct / total) * 100, 2) if total > 0 else 0.0

        difficulty_breakdown[level] = {
            "total": total,
            "correct": correct,
            "accuracy": accuracy
        }

    return {
        "total_questions": total_questions,
        "correct_count": correct_count,
        "incorrect_count": incorrect_count,
        "percentage": percentage,
        "difficulty_breakdown": difficulty_breakdown,
        "question_reviews": question_reviews,
        "weak_areas": weak_areas
    }