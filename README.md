# Neural Machine Translation Quality and Post-Editing Performance

This is a repository for an experiment relating NMT quality and post-editing efforts.

<!-- ## Processing

- exp1 top - pe times per model
- exp2 models - same as exp1 with BLEU ordering, but same distances
- exp3 docs - pe times per document
- exp4 user - pe times per user
- exp5 ter - ter per model
- exp6 len - output len per model
- exp7 unigram - output unigram F1 score per model -->

## Documents

| Document name | domain | lines | src words | description |
|-|-|-|-|-|
| Hole | news | 10 | 272 | sky.com.20667 |
| Whistle | news | 6 | 219 | nytimes.231903 |
| China | news | 12 | 357 | en.ndtv.com.13143 |
| Turner | news | 8 | 303 | euronews-en.185744 |
| QTLeap | technical | 11 | 178 | Batch2q\_cs\_v1010, Batch1a\_en\_v1.4.NAF |
| Lease | agreement | 29 | 597 | Translated by Ondřej |
| Audit (I)ntroduction | audit | 17 | 433 | Provided by NKÚ |
| Audit (R)ecommendation | audit | 6 | 121 | Provided by NKÚ |
| __Total__ | | __99__ | __2480__ | |

## Acknowledgement

Supported by [Memsource](https://memsource.com).

## Related References
1. https://www.cs.jhu.edu/~phi/publications/machine-translation-quality.pdf
2. https://www.dlsi.ua.es/~fsanchez/pub/pdf/forcada17a.pdf
