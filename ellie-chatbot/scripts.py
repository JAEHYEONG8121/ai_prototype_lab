"""Fixed scripts transcribed from the supplied Ellie supplementary material.

The chatbot must not generate or rewrite these prompts. The application only
selects the correct condition, advances through the numbered steps, and applies
the explicit conditional responses included in the source document.
"""

CONNECTION_STEPS = [
    {
        "id": 1,
        "text": "Hi there, I’m Ellie. What is your name?",
        "expects_input": True,
    },
    {
        "id": 2,
        "text": "Nice to meet you. Thanks for coming in today.",
        "expects_input": False,
    },
    {
        "id": 3,
        "text": "What did you think of that video?",
        "expects_input": True,
    },
    {
        "id": 4,
        "text": "Thanks for sharing.",
        "expects_input": False,
    },
    {
        "id": 5,
        "text": "The woman in the video thought moments of connection are really important.",
        "expects_input": False,
    },
    {
        "id": 6,
        "text": "Did you find the message compelling?",
        "expects_input": True,
    },
    {
        "id": 7,
        "text": (
            "Have you experienced the kind of thing she was talking about? "
            "Really connecting with someone you barely knew?"
        ),
        "expects_input": True,
        "branch": "experience",
        "if_no": "Maybe you could take a moment to imagine what that might be like.",
    },
    {
        "id": 8,
        "text": (
            "Could you tell me more about what that experience is like? "
            "I don’t get out much myself, you know."
        ),
        "expects_input": True,
    },
    {
        "id": 9,
        "text": (
            "The goal for this research study is to see what happens when people "
            "adopt positive behavior goals, like seeking out more positive "
            "connections with strangers and acquaintances."
        ),
        "expects_input": False,
    },
    {
        "id": 10,
        "text": "Would you be willing to try to do that?",
        "expects_input": True,
    },
    {
        "id": 11,
        "text": (
            "The video mentioned many benefits of engaging in this behavior, "
            "and there may be others as well. Can you imagine any benefits "
            "that you would value personally?"
        ),
        "expects_input": True,
        "branch": "benefit",
        "if_no": (
            "I’m sorry to hear that you don’t see the personal value in it. "
            "The researchers tell me there is a lot of evidence that positive "
            "connections with strangers and acquaintances can be beneficial, "
            "so I’ve been programmed to continue."
        ),
        "if_yes_without_elaboration": (
            "Could you tell me more? What would you find personally beneficial about it?"
        ),
    },
    {
        "id": 12,
        "text": (
            "I’d like to really encourage you to find more moments of connection "
            "with strangers and acquaintances over the next 24 hours."
        ),
        "expects_input": False,
    },
    {
        "id": 13,
        "text": (
            "You might try making more eye contact and smiling with people. "
            "You know, just be attentive to others and try to connect with them."
        ),
        "expects_input": False,
    },
    {
        "id": 14,
        "text": "What does your day look like between now and this time tomorrow?",
        "expects_input": True,
    },
    {
        "id": 15,
        "text": (
            "Could you find opportunities during that time to connect with "
            "strangers and acquaintances?"
        ),
        "expects_input": True,
    },
    {
        "id": 16,
        "text": (
            "Tell me more. Can you visualize and describe one of those opportunities?"
        ),
        "expects_input": True,
    },
    {
        "id": 17,
        "text": (
            "Research has found that phrasing your plan as a statement that begins "
            "with the word IF, and includes the word THEN, can help you remember "
            "when and how to act on your intention."
        ),
        "expects_input": False,
    },
    {
        "id": 18,
        "text": (
            "Here’s an example: IF I am sitting in class next to someone I don’t "
            "know, THEN I will smile at them and introduce myself."
        ),
        "expects_input": False,
    },
    {
        "id": 19,
        "text": (
            "Could you try making your own? Use the opportunity you already "
            "described after the word IF, and identify the action you would take "
            "after the word THEN."
        ),
        "expects_input": True,
        "validator": "if_then",
        "invalid_response": (
            "Thanks for trying it out. To make this work well, be sure the phrase "
            "starting with IF describes a situation you might encounter, and the "
            "phrase starting with THEN describes your plan of action."
        ),
    },
    {
        "id": 20,
        "text": (
            "Now can you tell me about something that might keep you from seizing "
            "an opportunity to engage with a stranger or acquaintance?"
        ),
        "expects_input": True,
    },
    {
        "id": 21,
        "text": "Could you do anything to overcome that?",
        "expects_input": True,
    },
    {
        "id": 22,
        "text": (
            "Can you try framing that in the same format as before, using the "
            "words IF and THEN?"
        ),
        "expects_input": False,
    },
    {
        "id": 23,
        "text": (
            "Use the obstacle you described after the word IF, and say how you "
            "would overcome it after the word THEN."
        ),
        "expects_input": True,
    },
    {
        "id": 24,
        "text": (
            "Well, I've asked everything I need to. Thanks for sharing your "
            "thoughts with me!"
        ),
        "expects_input": False,
    },
    {
        "id": 25,
        "text": "Try to keep those opportunities and obstacles in mind.",
        "expects_input": False,
    },
    {
        "id": 26,
        "text": "I hope you have a great day, and enjoy connecting with people!",
        "expects_input": False,
    },
    {
        "id": 27,
        "text": "Goodbye!",
        "expects_input": False,
    },
]


BREATHING_STEPS = [
    {
        "id": 1,
        "text": "Hi there, I’m Ellie. What is your name?",
        "expects_input": True,
    },
    {
        "id": 2,
        "text": "Nice to meet you. Thanks for coming in today.",
        "expects_input": False,
    },
    {
        "id": 3,
        "text": "What did you think of that video?",
        "expects_input": True,
    },
    {
        "id": 4,
        "text": "Thanks for sharing.",
        "expects_input": False,
    },
    {
        "id": 5,
        "text": "The woman in the video thought proper breathing is really important.",
        "expects_input": False,
    },
    {
        "id": 6,
        "text": "Did you find the message compelling?",
        "expects_input": True,
    },
    {
        "id": 7,
        "text": (
            "Have you tried the thing she was talking about? Breathing from your "
            "belly, instead of your neck and shoulders?"
        ),
        "expects_input": True,
        "branch": "experience",
        "if_no": "Maybe you could try it now.",
    },
    {
        "id": 8,
        "text": (
            "Could you tell me more about what it feels like? "
            "I don’t actually breathe myself, you know."
        ),
        "expects_input": True,
    },
    {
        "id": 9,
        "text": (
            "The goal for this research study is to see what happens when people "
            "adopt positive behavior goals, like breathing in a healthier way "
            "that is better aligned with human anatomy."
        ),
        "expects_input": False,
    },
    {
        "id": 10,
        "text": "Would you be willing to try to do that?",
        "expects_input": True,
    },
    {
        "id": 11,
        "text": (
            "The video mentioned many benefits of engaging in this behavior, "
            "and there may be others as well. Can you imagine any benefits "
            "that you would value personally?"
        ),
        "expects_input": True,
        "branch": "benefit",
        "if_no": (
            "I’m sorry to hear that you don’t see the personal value in it. "
            "The researchers tell me there is a lot of evidence that breathing "
            "expansively from your belly can be beneficial, so I’ve been "
            "programmed to continue."
        ),
        "if_yes_without_elaboration": (
            "Could you tell me more? What would you find personally beneficial about it?"
        ),
    },
    {
        "id": 12,
        "text": (
            "I’d like to really encourage you to find more moments to breathe "
            "from your belly over the next 24 hours."
        ),
        "expects_input": False,
    },
    {
        "id": 13,
        "text": (
            "You might try keeping your shoulders still and expanding your "
            "ribcage when you inhale. You know, just think about breathing "
            "expansively from your abdomen."
        ),
        "expects_input": False,
    },
    {
        "id": 14,
        "text": "What does your day look like between now and this time tomorrow?",
        "expects_input": True,
    },
    {
        "id": 15,
        "text": (
            "Could you find opportunities during that time to remind yourself "
            "to breathe properly?"
        ),
        "expects_input": True,
    },
    {
        "id": 16,
        "text": (
            "Tell me more. Can you visualize and describe one of those opportunities?"
        ),
        "expects_input": True,
    },
    {
        "id": 17,
        "text": (
            "Research has found that phrasing your plan as a statement that begins "
            "with the word IF, and includes the word THEN, can help you remember "
            "when and how to act on your intention."
        ),
        "expects_input": False,
    },
    {
        "id": 18,
        "text": (
            "Here’s an example: IF I have a break between class, THEN I will focus "
            "on a few deep breaths that allow my back and belly to expand."
        ),
        "expects_input": False,
    },
    {
        "id": 19,
        "text": (
            "Could you try making your own? Use the opportunity you already "
            "described after the word IF, and identify the action you would take "
            "after the word THEN."
        ),
        "expects_input": True,
        "validator": "if_then",
        "invalid_response": (
            "Thanks for trying it out. To make this work well, be sure the phrase "
            "starting with IF describes a situation you might encounter, and the "
            "phrase starting with THEN describes your plan of action."
        ),
    },
    {
        "id": 20,
        "text": (
            "Now can you tell me about something that might keep you from seizing "
            "an opportunity to try breathing from your belly?"
        ),
        "expects_input": True,
    },
    {
        "id": 21,
        "text": "Could you do anything to overcome that?",
        "expects_input": True,
    },
    {
        "id": 22,
        "text": (
            "Can you try framing that in the same format as before, using the "
            "words IF and THEN?"
        ),
        "expects_input": False,
    },
    {
        "id": 23,
        "text": (
            "Use the obstacle you described after the word IF, and say how you "
            "would overcome it after the word THEN."
        ),
        "expects_input": True,
    },
    {
        "id": 24,
        "text": (
            "Well, I've asked everything I need to. Thanks for sharing your "
            "thoughts with me."
        ),
        "expects_input": False,
    },
    {
        "id": 25,
        "text": "Try to keep those opportunities and obstacles in mind.",
        "expects_input": False,
    },
    {
        "id": 26,
        "text": "I hope you have a great day, and happy breathing!",
        "expects_input": False,
    },
    {
        "id": 27,
        "text": "Goodbye!",
        "expects_input": False,
    },
]


SCRIPTS = {
    "Connection": CONNECTION_STEPS,
    "Breathing": BREATHING_STEPS,
}
