import random 

def generate_text(level: str, topic: str = None):
    # For now use placeholders instead of the real AI model
    samples = {
        "beginner": [
            "The sun rises in the east and sets in the west.",
            "Typing helps improve your focus and speed."
        ],
        "intermediate": [
            "The universe is full of mysteries waiting to be explored.",
            "Artificial intelligence is transforming how human learn."
        ],
        "advanced": [
            "Quantum computing redefines the limits of classical algorithems.",
            "Understanding neural nerworks requires both theory and intuition."
        ],
    }

    return random.choice(samples.get(level, samples["beginner"]))