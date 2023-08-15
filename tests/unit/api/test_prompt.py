# vim: ft=python fileencoding=utf-8 sw=4 et sts=4

"""Tests for vimiv.api.prompt."""

import pytest

from vimiv.qt.core import QObject

from vimiv.api import prompt


class QuestionAnswerer(QObject):
    """Stub class answering an asked question with a defined value."""

    def __init__(self, *, title: str, body: str, answer=None):
        super().__init__()
        self.title = title
        self.body = body
        self.answered = False
        self.answer = answer
        prompt.question_asked.connect(self.answer_question)

    def answer_question(self, question: prompt.Question):
        assert question.title == self.title
        assert question.body == self.body
        question.answer = self.answer
        self.answered = True


@pytest.mark.parametrize("answer", (None, 42, "answer"))
def test_ask_question(answer):
    title = "Question"
    body = "Does this test work?"
    answerer = QuestionAnswerer(title=title, body=body, answer=answer)
    received_answer = prompt.ask_question(title=title, body=body)
    assert answerer.answered
    assert received_answer == answer
