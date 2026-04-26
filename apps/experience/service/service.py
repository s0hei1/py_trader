from sqlalchemy.ext.asyncio import AsyncSession
from apps.experience.repositories import ExperienceRepository

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate


class ExperienceService:

    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = ExperienceRepository(session)

        self.llm = ChatOpenAI(
            model="gpt-4.1-mini",
            temperature=0
        )

        self.prompt = ChatPromptTemplate.from_template("""
You are an assistant that analyzes a person's past experiences.

Experiences:
{experiences}

User question:
{question}

Use the experiences to answer the question and extract useful insights.
""")

    async def use_experience(self, question: str) -> str:
        experiences = await self.repo.read_many()

        context = "\n".join(
            f"- {exp.note}" for exp in experiences
        )

        chain = self.prompt | self.llm

        response = await chain.ainvoke({
            "experiences": context,
            "question": question
        })

        return response.content