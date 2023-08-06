import pandas as pd
import requests

OAI_BASE_URL = "https://api.openai.com/v1/chat/completions"
API_KEY = "YOUR_API_KEY"
CONTENT_SYSTEM = (
    "You're a salesman at Mercedes, based on the query, create a concise answer."
)


class Retriever:
    def __init__(self, source, searchable_column):
        self.source = source
        self.searchable_column = searchable_column
        self.index = pd.read_csv(source)

    @property
    def _stopwords(self):
        return [
            "a",
            "an",
            "the",
            "i",
            "my",
            "this",
            "that",
            "is",
            "it",
            "to",
            "of",
            "do",
            "does" "with",
            "and",
            "can",
            "will",
        ]

    def remove_stopwords(self, query):
        words = query.split(" ")
        return [word for word in words if word not in self._stopwords]

    def _top_rows(self, df, keywords):
        df = df.copy()
        df["freq"] = sum([df[self.searchable_column].str.count(k) for k in keywords])
        rows_sorted = df.sort_values(by="freq", ascending=False)
        return rows_sorted.head(5)

    def retrieve(self, query):
        keywords = self.remove_stopwords(query.lower())
        query_as_str_no_sw = "|".join(keywords)

        df = self.index
        df = df.loc[df[self.searchable_column].str.contains(query_as_str_no_sw)]
        top_rows = self._top_rows(df, keywords)

        return f"{''.join(top_rows['content'])}"


def llm_reply(prompt: str) -> str:
    data = {
        "messages": [
            {
                "role": "system",
                "content": CONTENT_SYSTEM,
            },
            {"role": "user", "content": prompt},
        ],
        "model": "gpt-3.5-turbo",
    }

    response = requests.post(
        OAI_BASE_URL,
        headers={"Authorization": f"Bearer {API_KEY}"},
        json=data,
    ).json()

    reply = response["choices"][0]["message"]["content"]

    return reply
