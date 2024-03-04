import pandas as pd

bleu_scores = (
    ('src', 0, 0),
    ('ref', 100, 100),
    ('m01', 25.35, 19.07),
    ('m02', 31.61, 22.44),
    ('m03', 33.09, 23.86),
    ('m04', 33.63, 24.42),
    ('m05', 35.22, 26.25),
    ('m06', 35.68, 26.64),
    ('m07', 36.58, 28.14),
    ('m08', 36.41, 28.84),
    ('m09', 37.40, 28.72),
    ('m10', 37.44, 28.95),
    ('m11', 37.37, 28.46),
    ('google', 37.56, 26.06),
    ('microsoft', 33.06, 26.30),
)
bleu_scores_df = pd.DataFrame(bleu_scores, columns=("mt_name", "bleu_docs", "bleu_wmt"))

df1 = pd.read_json("docs/memsource/data-after-phase-1.jsonl", lines=True).merge(
    bleu_scores_df, on=["mt_name"]
)


df1["position"] = [
    "first" if x["is_first"] else "last" if x["is_last"] else "middle"
    for _, x in df1.iterrows()
]
df1.drop(["is_last", "is_first", "job_uid", "tunit_id"], inplace=True, axis=1)
df1.rename(
    columns={
        "user_a": "user",
        "comments": "user_comment",
        "provided": "text_provided",
        "source": "text_source",
        "target": "text_finished",
    },
    inplace=True,
)
# fake revision to make HF happy
df1["revisions"] = [[{"error_category": -1, "error_severity": -1}] for _ in df1["user"]]
# change order of columns
df1 = df1[
    [
        'user',
        'text_source',
        'text_provided',
        'text_finished',
        'edit_time',
        'edit_time_word',
        'think_time',
        'think_time_word',
        'bleu_docs',
        'bleu_wmt',
        'mt_name',
        'doc_name',
        'position',
        "revisions",
        'user_comment',
    ]
]


df2 = pd.read_json("docs/memsource/data-phase-2.jsonl", lines=True).merge(
    bleu_scores_df, on=["mt_name"]
)

df2["position"] = [
    "first" if x["revision_is_first"] else "last" if x["revision_is_last"] else "middle"
    for _, x in df2.iterrows()
]
df2.drop(
    ["job_uid", "tunit_id", "revision_is_last", "revision_is_first"],
    inplace=True,
    axis=1,
)
df2.rename(
    columns={
        "user_a": "user",
        "source": "text_source",
        "revision_provided": "text_provided",
        "target": "text_finished",
        "revision_edit_time": "edit_time",
        "revision_edit_time_word": "edit_time_word",
        "revision_think_time": "think_time",
        "revision_think_time_word": "think_time_word",
        "revision_conversation": "revisions",
    },
    inplace=True,
)
df2["user_comment"] = ["" for _ in df2["user"]]
df2 = df2[
    [
        'user',
        'text_source',
        'text_provided',
        'text_finished',
        'edit_time',
        'edit_time_word',
        'think_time',
        'think_time_word',
        'bleu_docs',
        'bleu_wmt',
        'mt_name',
        'doc_name',
        'position',
        'revisions',
        "user_comment",
    ]
]

# simplify revisions
rev_new = []
for _, line in df2.iterrows():
    rev_new.append(
        [
            {"error_category": x["errorCategoryId"], "error_severity": x["severityId"]}
            for rev in line["revisions"]
            if "lqa" in rev["references"]
            for x in rev["references"]["lqa"]
        ]
    )


def str_to_user_id(x):
    return -int("".join([str(ord(y)) for y in x]))


df2["revisions"] = rev_new
df2["user"] = [x if type(x) != str else str_to_user_id(x) for x in df2["user"]]
df1.to_json("docs/phase_1.json", orient="records", indent=2, force_ascii=False)
df2.to_json("docs/phase_2.json", orient="records", indent=2, force_ascii=False)

print(len(df1), "P1 records")
print(len(df2), "P2 records")

print(df1.columns)
print(df2.columns)
