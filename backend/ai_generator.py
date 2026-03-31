"""
AI Question Generator and Answer Evaluator
============================================
100% dynamic — uses Google Gemini API to generate exam questions
and evaluate viva answers.  No static/hardcoded question bank.

Reads GEMINI_API_KEY from the .env file (loaded by app.py via python-dotenv).
"""

import json
import re
import os
import time
import random
from difflib import SequenceMatcher

# ==================== GEMINI CLIENT SETUP ====================

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-2.0-flash")

_gemini_client = None
_USE_NEW_SDK = False


def _init_gemini():
    """Lazy-initialise the Gemini client (called once on first use)."""
    global _gemini_client, _USE_NEW_SDK

    if _gemini_client is not None:
        return  # already initialised

    api_key = GEMINI_API_KEY
    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is not set. "
            "Add it to backend/.env  ->  GEMINI_API_KEY=your-key-here"
        )

    try:
        from google import genai
    except ImportError:
        try:
            import google.generativeai as legacy_genai
            legacy_genai.configure(api_key=api_key)
            _gemini_client = legacy_genai.GenerativeModel(GEMINI_MODEL)
            _USE_NEW_SDK = False
            print(f"[Gemini] Initialised (legacy SDK)  model={GEMINI_MODEL}")
        except ImportError as import_err:
            raise RuntimeError(
                "Google Gemini SDK not found. Install dependencies with: "
                "pip install -r backend/requirements.txt"
            ) from import_err
    else:
        try:
            _gemini_client = genai.Client(api_key=api_key)
            _USE_NEW_SDK = True
            print(f"[Gemini] Initialised (new SDK)  model={GEMINI_MODEL}")
        except Exception as client_err:
            raise RuntimeError(f"Failed to initialize Gemini client: {client_err}") from client_err


def _call_gemini(prompt: str, retries: int | None = None) -> str:
    """Send a prompt to Gemini and return the raw text response.
    Retries with short increasing waits to recover from transient rate limits."""
    _init_gemini()

    if retries is None:
        retries = int(os.environ.get("GEMINI_RETRIES", "2"))

    for attempt in range(retries):
        try:
            if _USE_NEW_SDK:
                response = _gemini_client.models.generate_content(
                    model=GEMINI_MODEL, contents=prompt
                )
                return response.text
            else:
                response = _gemini_client.generate_content(prompt)
                return response.text
        except Exception as e:
            err_str = str(e)
            if "429" in err_str or "RESOURCE_EXHAUSTED" in err_str or "quota" in err_str.lower():
                wait = min(5 * (attempt + 1), 15)  # 5s, 10s, 15s...
                print(f"[Gemini] Rate limited, waiting {wait}s (attempt {attempt+1}/{retries})...")
                time.sleep(wait)
            elif "API_KEY_INVALID" in err_str or "API key not valid" in err_str:
                raise RuntimeError("INVALID_API_KEY: Please update GEMINI_API_KEY in backend/.env")
            else:
                raise
    raise RuntimeError("RATE_LIMIT_EXCEEDED: Gemini API is busy. Please try again in a moment.")


# ==================== JSON HELPERS ====================

def _extract_json(text: str):
    """Parse a JSON array or object out of Gemini's response text."""
    # Strip markdown code fences
    text = re.sub(r"```(?:json)?", "", text).strip()
    text = text.strip("`").strip()

    # Try array first, then object
    match = re.search(r"\[.*\]", text, re.DOTALL)
    if match:
        return json.loads(match.group())

    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        return json.loads(match.group())

    return json.loads(text)


# ==================== QUESTION GENERATION ====================

_QUESTION_PROMPT = """You are an expert exam paper setter.

Subject  : {subject}
Difficulty: {difficulty}
Total Marks: {total_marks}
Total Questions: {total_questions}

Generate a well-balanced set of EXACTLY {total_questions} exam questions.

DISTRIBUTION RULES:
- MCQ questions        -> EXACTLY {mcq_count} (1 mark each)
- True/False questions -> EXACTLY {tf_count} (1 mark each)
- Viva (short answer)  -> EXACTLY {viva_count} (2 marks each)

IMPORTANT RULES:
1. Every question MUST be unique — no duplicates.
2. Questions must be standard academic quality for the given difficulty.
3. Cover different topics within the subject — do not repeat the same topic.
4. Use varied wording styles and avoid repeating the same sentence pattern.
5. Mix conceptual, scenario-based, application-based, comparison, and error-detection style questions.
6. Use diverse stems like identify, choose, analyze, infer, compare, predict, evaluate.
7. Avoid boilerplate intros like repeating the same opening phrase for many questions.
8. For MCQ: always give exactly 4 options.
9. For True/False: options must be ["True", "False"].
10. For Viva: options must be an empty array [].
11. Correct answer for MCQ = "A", "B", "C", or "D".
12. Correct answer for True/False = "A" for True, "B" for False.
13. Correct answer for Viva = a full model answer string.

Return ONLY a valid JSON array, nothing else.  Each object must have:
{{
  "question": "...",
  "type": "MCQ" | "True/False" | "Viva",
  "options": ["...", "...", "...", "..."],
  "correct_answer": "...",
  "explanation": "one-line explanation",
  "marks": 1 or 2,
  "topic": "specific topic name"
}}
"""


_SUBJECT_TOPICS = {
    "Artificial Intelligence": [
        "Search Algorithms", "Knowledge Representation", "Machine Learning",
        "Neural Networks", "Expert Systems", "Natural Language Processing",
        "Planning", "Reasoning Under Uncertainty", "Computer Vision", "Ethics in AI"
    ],
    "Computer Networks": [
        "OSI Model", "TCP/IP", "Routing", "Switching", "DNS",
        "HTTP/HTTPS", "Congestion Control", "Subnetting", "Network Security", "Wireless Networks"
    ],
    "Computer Graphics": [
        "Rasterization", "2D Transformations", "3D Transformations", "Projection",
        "Clipping", "Shading", "Rendering Pipeline", "Color Models", "Curves and Surfaces", "Animation"
    ],
    "Compiler Design": [
        "Lexical Analysis", "Parsing", "Syntax Trees", "Semantic Analysis", "Type Checking",
        "Intermediate Code", "Optimization", "Code Generation", "Symbol Tables", "Error Handling"
    ],
}


def _letters(index: int) -> str:
    return ["A", "B", "C", "D"][index]


def _is_near_duplicate(candidate: str, seen_questions: list[str], threshold: float = 0.86) -> bool:
    candidate_norm = candidate.strip().lower()
    for seen in seen_questions:
        if SequenceMatcher(None, candidate_norm, seen.strip().lower()).ratio() >= threshold:
            return True
    return False


def _build_mcq(subject: str, topic: str, difficulty: str, idx: int) -> dict:
    correct_index = idx % 4
    correct_text = f"A core concept in {topic} used to solve {subject} problems"
    distractors = [
        f"A hardware-only technique unrelated to {topic}",
        f"A deprecated method that ignores problem constraints",
        f"A random strategy with no evaluation criteria"
    ]
    options = distractors.copy()
    options.insert(correct_index, correct_text)

    question_templates = [
        f"Which option best describes {topic}?",
        f"For a real-world {subject} use case, which statement about {topic} is most accurate?",
        f"A learner confuses {topic}. Which choice shows the correct understanding?",
        f"Select the best interpretation of {topic} in practice.",
        f"Which option reflects a valid application of {topic}?"
    ]

    return {
        "question": question_templates[idx % len(question_templates)],
        "type": "MCQ",
        "options": options,
        "correct_answer": _letters(correct_index),
        "explanation": f"{topic} focuses on principled methods, not random or unrelated approaches.",
        "marks": 1,
        "topic": topic,
    }


def _build_true_false(subject: str, topic: str, idx: int) -> dict:
    is_true = idx % 2 == 0
    true_templates = [
        f"{topic} is an important area in {subject}.",
        f"{topic} is commonly used to improve outcomes in {subject}.",
        f"A strong foundation in {topic} helps in {subject} problem-solving."
    ]
    false_templates = [
        f"{topic} has no relevance to {subject}.",
        f"{topic} is never applied in practical {subject} systems.",
        f"{topic} is unrelated to modern {subject} methods."
    ]

    if is_true:
        statement = true_templates[idx % len(true_templates)]
        explanation = f"True: {topic} is a recognized topic within {subject}."
    else:
        statement = false_templates[idx % len(false_templates)]
        explanation = f"False: {topic} is relevant to {subject}."

    return {
        "question": statement,
        "type": "True/False",
        "options": ["True", "False"],
        "correct_answer": "A" if is_true else "B",
        "explanation": explanation,
        "marks": 1,
        "topic": topic,
    }


def _build_viva(subject: str, topic: str, difficulty: str) -> dict:
    question_templates = [
        f"Explain {topic} in {subject} and describe one practical application.",
        f"How would you explain {topic} to a beginner in {subject}? Include one example.",
        f"Compare a correct and incorrect use of {topic} in {subject}.",
        f"Why is {topic} important in {subject}? Support with a real scenario."
    ]

    return {
        "question": random.choice(question_templates),
        "type": "Viva",
        "options": [],
        "correct_answer": (
            f"A good answer defines {topic}, explains its role in {subject}, "
            "and includes at least one realistic application scenario."
        ),
        "explanation": f"Key points: definition, role, and application of {topic}.",
        "marks": 2,
        "topic": topic,
    }


def _compute_distribution(total_questions: int) -> tuple:
    viva_count = max(1, round(total_questions * 0.25))
    tf_count = max(1, round(total_questions * 0.15))
    mcq_count = total_questions - viva_count - tf_count

    if mcq_count < 1:
        deficit = 1 - mcq_count
        mcq_count = 1
        while deficit > 0 and viva_count > 1:
            viva_count -= 1
            deficit -= 1
        while deficit > 0 and tf_count > 1:
            tf_count -= 1
            deficit -= 1

    while (mcq_count + tf_count + viva_count) > total_questions and viva_count > 1:
        viva_count -= 1
    while (mcq_count + tf_count + viva_count) > total_questions and tf_count > 1:
        tf_count -= 1
    while (mcq_count + tf_count + viva_count) < total_questions:
        mcq_count += 1

    return mcq_count, tf_count, viva_count


def _normalize_question_type(raw_type: str) -> str:
    t = str(raw_type or '').strip().lower()
    if t in ('mcq', 'multiple choice', 'multiple-choice'):
        return 'MCQ'
    if t in ('true/false', 'true false', 'tf', 'boolean'):
        return 'True/False'
    return 'Viva'


def _distribution_from_pattern(total_questions: int, exam_pattern: dict | None):
    if exam_pattern and exam_pattern.get('distribution'):
        dist = exam_pattern['distribution']
        return (
            int(dist.get('MCQ', 0)),
            int(dist.get('True/False', 0)),
            int(dist.get('Viva', 0)),
        )
    return _compute_distribution(total_questions)


def _generate_offline_questions(subject: str, total_questions: int, difficulty: str, start_id: int = 0, exam_pattern: dict | None = None) -> list:
    topics = _SUBJECT_TOPICS.get(subject, [
        "Fundamentals", "Core Concepts", "Design Principles", "Applications", "Evaluation"
    ])

    mcq_count, tf_count, viva_count = _distribution_from_pattern(total_questions, exam_pattern)
    result = []
    q_id = start_id + 1

    for i in range(mcq_count):
        topic = topics[i % len(topics)]
        q = _build_mcq(subject, topic, difficulty, i)
        q["id"] = q_id
        result.append(q)
        q_id += 1

    for i in range(tf_count):
        topic = topics[(i + mcq_count) % len(topics)]
        q = _build_true_false(subject, topic, i)
        q["id"] = q_id
        result.append(q)
        q_id += 1

    for i in range(viva_count):
        topic = topics[(i + mcq_count + tf_count) % len(topics)]
        q = _build_viva(subject, topic, difficulty)
        q["id"] = q_id
        result.append(q)
        q_id += 1

    return result


# ==================== QUESTION GENERATION ====================


def generate_questions_ai(subject: str, total_marks: int, difficulty: str, exam_pattern: dict | None = None) -> list:
    """
    Generate exam questions dynamically via Gemini API.
    All questions come from the AI — no static fallback.
    Raises RuntimeError with a user-friendly message if the API is unavailable.
    """
    if exam_pattern:
        total_questions = int(exam_pattern.get('total_questions', total_marks))
    else:
        total_questions = int(total_marks)

    mcq_count, tf_count, viva_count = _distribution_from_pattern(total_questions, exam_pattern)

    prompt = _QUESTION_PROMPT.format(
        subject=subject,
        difficulty=difficulty,
        total_marks=total_marks,
        total_questions=total_questions,
        mcq_count=mcq_count,
        tf_count=tf_count,
        viva_count=viva_count,
    )

    try:
        # This will retry up to 4 times before raising
        raw = _call_gemini(prompt)
    except RuntimeError as api_err:
        if "RATE_LIMIT_EXCEEDED" in str(api_err):
            print("[Gemini] Busy/rate-limited. Using offline fallback generator.")
            return _generate_offline_questions(subject, total_questions, difficulty, exam_pattern=exam_pattern)
        raise

    try:
        questions = _extract_json(raw)
    except Exception as parse_err:
        print(f"[Gemini] Invalid response format ({parse_err}). Using offline fallback generator.")
        return _generate_offline_questions(subject, total_questions, difficulty, exam_pattern=exam_pattern)

    # Validate, deduplicate, and clean each question
    cleaned_by_type = {'MCQ': [], 'True/False': [], 'Viva': []}
    seen_questions = []   # prevent duplicates and near-duplicates within the same paper
    for q in questions:
        if sum(len(v) for v in cleaned_by_type.values()) >= total_questions:
            break

        q_text = str(q.get("question", "")).strip().lower()
        if not q_text or _is_near_duplicate(q_text, seen_questions):
            continue  # skip empty or duplicate questions

        q_type = _normalize_question_type(q.get("type", "MCQ"))
        marks = int(q.get("marks", 2 if q_type == "Viva" else 1))

        if q_type == 'MCQ' and len(cleaned_by_type['MCQ']) >= mcq_count:
            continue
        if q_type == 'True/False' and len(cleaned_by_type['True/False']) >= tf_count:
            continue
        if q_type == 'Viva' and len(cleaned_by_type['Viva']) >= viva_count:
            continue

        if q_type == 'MCQ' and marks != 1:
            marks = 1
        if q_type == 'True/False' and marks != 1:
            marks = 1
        if q_type == 'Viva' and marks != 2:
            marks = 2

        options = q.get("options") if isinstance(q.get("options"), list) else []
        if q_type == 'True/False':
            options = ["True", "False"]
        if q_type == 'Viva':
            options = []

        seen_questions.append(q_text)
        cleaned_by_type[q_type].append({
            "question": str(q.get("question", "")),
            "type": q_type,
            "options": options,
            "correct_answer": str(q.get("correct_answer", "")),
            "explanation": str(q.get("explanation", "")),
            "marks": marks,
            "topic": str(q.get("topic", subject)),
        })

    current_mcq = len(cleaned_by_type['MCQ'])
    current_tf = len(cleaned_by_type['True/False'])
    current_viva = len(cleaned_by_type['Viva'])
    if current_mcq < mcq_count or current_tf < tf_count or current_viva < viva_count:
        missing = {
            'MCQ': max(0, mcq_count - current_mcq),
            'True/False': max(0, tf_count - current_tf),
            'Viva': max(0, viva_count - current_viva),
        }
        print(f"[Gemini] Partial generation. Filling missing counts offline: {missing}")
        offline_fill = _generate_offline_questions(
            subject,
            total_questions,
            difficulty,
            exam_pattern={
                'distribution': missing,
                'total_questions': sum(missing.values())
            }
        )
        for item in offline_fill:
            q_type = _normalize_question_type(item.get('type'))
            if q_type == 'MCQ' and len(cleaned_by_type['MCQ']) < mcq_count:
                cleaned_by_type['MCQ'].append(item)
            elif q_type == 'True/False' and len(cleaned_by_type['True/False']) < tf_count:
                cleaned_by_type['True/False'].append(item)
            elif q_type == 'Viva' and len(cleaned_by_type['Viva']) < viva_count:
                cleaned_by_type['Viva'].append(item)

    cleaned = cleaned_by_type['MCQ'] + cleaned_by_type['True/False'] + cleaned_by_type['Viva']
    cleaned = cleaned[:total_questions]
    for idx, q in enumerate(cleaned, start=1):
        q['id'] = idx

    return cleaned


def _generate_filler_mcqs(subject, difficulty, marks_needed, start_id, seen_questions=None):
    """Ask Gemini for extra MCQs to fill any remaining marks gap, skipping already-seen questions."""
    if seen_questions is None:
        seen_questions = set()
    prompt = (
        f"Generate exactly {marks_needed} unique MCQ questions for "
        f"{subject} ({difficulty} level). "
        f"Each worth 1 mark, 4 options, correct answer as A/B/C/D.\n"
        f'Return ONLY a JSON array: '
        f'[{{"question":"...","type":"MCQ","options":[...], '
        f'"correct_answer":"A","explanation":"...","marks":1,"topic":"..."}}]'
    )
    try:
        raw = _call_gemini(prompt)
        extras = _extract_json(raw)
        result = []
        filler_idx = start_id + 1
        for q in extras:
            q_text = str(q.get("question", "")).strip().lower()
            if not q_text or q_text in seen_questions:
                continue  # skip duplicates
            seen_questions.add(q_text)
            result.append({
                "id": filler_idx,
                "question": str(q.get("question", "")),
                "type": "MCQ",
                "options": q.get("options") if isinstance(q.get("options"), list) else [],
                "correct_answer": str(q.get("correct_answer", "A")),
                "explanation": str(q.get("explanation", "")),
                "marks": 1,
                "topic": str(q.get("topic", subject)),
            })
            filler_idx += 1
            if len(result) >= marks_needed:
                break
        return result
    except Exception as e:
        print(f"[Gemini] Filler generation failed: {e}")
        return []


# ==================== ANSWER EVALUATION ====================

_EVAL_PROMPT = """You are a strict but fair exam evaluator.

Question    : {question}
Model Answer: {correct_answer}
Student Answer: {user_answer}

Score the student's answer out of 2 marks.
- 2   = Excellent, covers all key points
- 1.5 = Good but missing minor details
- 1   = Partially correct
- 0.5 = Mostly wrong but shows some understanding
- 0   = Completely wrong or irrelevant

Return ONLY this JSON (no other text):
{{"marks": <number>, "is_correct": <true if marks >= 1 else false>, "feedback": "<one sentence>"}}
"""


def evaluate_answer_ai(question_text: str, correct_answer: str, user_answer: str) -> dict:
    """
    Evaluate a Viva/short-answer response using Gemini.
    Falls back to similarity scoring if Gemini is unavailable.
    """
    if not user_answer or not user_answer.strip():
        return {"is_correct": False, "marks": 0, "feedback": "No answer provided."}

    # --- Try Gemini ---
    try:
        prompt = _EVAL_PROMPT.format(
            question=question_text,
            correct_answer=correct_answer,
            user_answer=user_answer,
        )
        raw = _call_gemini(prompt)
        result = _extract_json(raw)
        return {
            "marks": float(result.get("marks", 0)),
            "is_correct": bool(result.get("is_correct", False)),
            "feedback": str(result.get("feedback", "")),
        }
    except Exception as e:
        print(f"[Gemini] Evaluation failed ({e}), using similarity fallback.")

    # --- Similarity fallback ---
    similarity = SequenceMatcher(None, correct_answer.lower(), user_answer.lower()).ratio()
    correct_terms = set(correct_answer.lower().split())
    user_terms = set(user_answer.lower().split())
    common = correct_terms & user_terms
    coverage = len(common) / len(correct_terms) if correct_terms else 0
    score = (similarity * 0.6) + (coverage * 0.4)

    if score >= 0.75:
        return {"is_correct": True, "marks": 2, "feedback": "Excellent answer."}
    elif score >= 0.5:
        return {"is_correct": True, "marks": 1.5, "feedback": "Good, but could be more detailed."}
    elif score >= 0.3:
        return {"is_correct": False, "marks": 1, "feedback": "Partially correct."}
    else:
        return {"is_correct": False, "marks": 0.5, "feedback": "Answer needs improvement."}
