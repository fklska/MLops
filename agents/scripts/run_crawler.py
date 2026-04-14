from typing import List
from agents.schemas import MovieList, ReviewAnalysis
from config.settings import get_api_key
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from ddgs import DDGS
import json

api_key = get_api_key()
llm = ChatOpenAI(
    openai_api_key=api_key,
    openai_api_base="https://openrouter.ai/api/v1",
    model_name="nvidia/nemotron-3-super-120b-a12b:free",
    temperature=0.1,
    max_tokens=500,
    default_headers={
        "HTTP-Referer": "http://localhost:8000",
        "X-Title": "MovieCrawlerAgent",
    }
)


def agent_1_find_new_movies(query: str = "новинки кино 2025 список фильмов") -> MovieList:
    """
    Агент 1: Ищет новинки кино и возвращает структурированный список.
    """
    print(f"___Агент 1: Ищу новинки по запросу: '{query}'____")

    search_results = DDGS().text(query, max_results=5, region='ru-ru')
    if not search_results:
        # print("Агент 1: Ничего не найдено через поиск.")
        return MovieList(movies=[])

    search_context = "\n".join([f"- {res['title']}: {res['body']}" for res in search_results])

    parser = PydanticOutputParser(pydantic_object=MovieList)

    prompt = ChatPromptTemplate.from_messages([
        ("system", "Ты — помощник, который извлекает названия фильмов-новинок из результатов поиска. {format_instructions}"),
        ("human", "Вот результаты поиска по запросу 'новинки кино':\n{context}\n\nИзвлеки из них список фильмов (до 5 штук).")
    ])

    chain = prompt | llm | parser

    try:
        movie_list = chain.invoke({
            "format_instructions": parser.get_format_instructions(),
            "context": search_context
        })
        print(f"Агент 1: Найдено фильмов: {len(movie_list.movies)}")
        return movie_list
    except Exception as e:
        print(f"Ошибка в Агенте 1: {e}")
        return MovieList(movies=[])



def agent_2_find_reviews(movie_list: MovieList) -> List[ReviewAnalysis]:
    """
    Агент 2: Для каждого фильма ищет рецензию на kp.ru и анализирует её.
    """
    all_reviews = []
    print(f"___Агент 2: Анализирую {len(movie_list.movies)} фильмов____")
    
    parser = PydanticOutputParser(pydantic_object=ReviewAnalysis)
    
    for movie in movie_list.movies:
        print(f"\nОбрабатываю фильм: {movie.title}")
        search_query = f"site:kp.ru {movie.title} рецензия"
        search_results = DDGS().text(search_query, max_results=1, region='ru-ru')
        print('search_results:    ____________\n', search_results)

        if not search_results:
            print(f"  -> Не найдено рецензий на kp.ru для '{movie.title}'")
            continue

        review_url = search_results[0]['href']
        print(f"  -> Найдена рецензия: {review_url}")

        extracted_content = DDGS().extract(review_url, fmt='text_plain')
        page_text = extracted_content.get('content', '')

        if not page_text or len(page_text) < 100:
            print(f"  -> Не удалось извлечь достаточный текст со страницы.")
            continue

        # parser = PydanticOutputParser(pydantic_object=ReviewAnalysis)

        prompt = ChatPromptTemplate.from_messages([
            ("system", "Ты — критик, анализирующий рецензии на фильмы. {format_instructions}"),
            ("human", "Проанализируй следующую рецензию на фильм '{movie_title}'. Выдели плюсы, минусы, краткое содержание и оценку, если она есть.\n\nТекст рецензии:\n{review_text}")
        ])

        chain = prompt | llm | parser

        try:
            analysis = chain.invoke({
                "format_instructions": parser.get_format_instructions(),
                "movie_title": movie.title,
                "review_text": page_text[:6000] # Ограничиваем длину текста
            })
            analysis.source_url = review_url
            all_reviews.append(analysis)
            print(f"  -> Рецензия успешно проанализирована.")
        except Exception as e:
            print(f"  -> Ошибка при анализе рецензии: {e}")

    return all_reviews



if __name__ == "__main__":
    new_movies = agent_1_find_new_movies()
    if new_movies.movies:
        reviews = agent_2_find_reviews(new_movies)
        print(json.dumps([r.dict() for r in reviews], indent=2, ensure_ascii=False))