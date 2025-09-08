from aiohttp.helpers import quoted_string
from aiohttp.web_exceptions import HTTPConflict, HTTPUnauthorized, HTTPNotFound
from aiohttp_apispec import request_schema, response_schema

from app.quiz.schemes import ThemeSchema, ThemeListSchema, QuestionSchema
from app.web.app import View
from app.web.schemes import OkResponseSchema
from app.web.utils import json_response

# TODO: добавить проверку авторизации для этого View
class ThemeAddView(View):
    @request_schema(ThemeSchema)
    @response_schema(OkResponseSchema, 200)
    async def post(self):
        title = (await self.request.json()).get('title')
        if await self.store.quizzes.get_theme_by_title(title) is not None:
            raise HTTPConflict
        theme = await self.store.quizzes.create_theme(title=title)
        return json_response(data={"id": theme.id, "title": theme.title})


class ThemeListView(View):
    @request_schema(ThemeListSchema)
    @response_schema(OkResponseSchema, 200)
    async def get(self):
        themes = await self.store.quizzes.list_themes()
        themes_data = [{"id": thema.id, "title": thema.title} for thema in themes]
        return json_response(data={"themes": themes_data})


class QuestionAddView(View):
    @request_schema(QuestionSchema)
    @response_schema(OkResponseSchema, 200)
    async def post(self):
        data = await self.request.json()
        title = data.get('title')
        theme_id = data.get('theme_id')
        if await self.store.quizzes.get_theme_by_id(theme_id) is None:
            raise HTTPNotFound
        if await self.store.quizzes.get_question_by_title(title) is not None:
            raise HTTPConflict
        answers = data.get('answers')
        question = await self.store.quizzes.create_question(
            title=title, theme_id=theme_id, answers=answers
        )
        return json_response(data={"id": question.id,
                                   "title": question.title,
                                   "theme_id": question.theme_id,
                                   "answers": question.answers
                                   })


class QuestionListView(View):
    @response_schema(OkResponseSchema, 200)
    async def get(self):
        theme_id = self.request.query.get('theme_id')
        questions = await self.store.quizzes.list_questions(
            None if theme_id is None else int(theme_id))

        questions_data = [{
            "id": question.id,
            "title": question.title,
            "theme_id": question.theme_id,
            "answers": [
                {
                    "title": a.title if hasattr(a, "title") else a["title"],
                    "is_correct": a.is_correct if hasattr(a, "is_correct") else a["is_correct"],
                } for a in question.answers
            ]
            } for question in questions
        ]
        return json_response(data={"questions": questions_data})