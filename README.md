# Effects of Neural Machine Translation Quality on Post-Editing Time

Title is WIP. This is a repository for an experiment relating NMT quality and post-editing efforts.

## Rozdíl oproti [1]
- SMT vs NMT
- podivat se na revize, jestli prekladatele u tech kvalitnich (fluent) MT vystupu nemeli tendenci prehlizet fakticke chyby (adequacy)
- Jiný jazykový pár.
- Produkční prostředí.
- Document-level aspekt
- - Lze použít WMT20 Markables tool.
- - Ze budeme vedet, jestli soucasne “document-aware MT” je nebo neni opravdu viditelne v posteditacich lepsi v koherenci napric segmenty
- - Jak závisí počet PE v markables na BLEU?

## Schedule
- Získání dat
- Získání překladů
- Post-editovat překladači
- Validační překlad
- Zpracovat logy & sepsat článek

# Documents

## Proposal 1

| Document name | domain | lines | src words | description |
|-|-|-|-|-|
| Monsoon | news | 11 | 365 | guardian.260810 |
| Dare | news | 13 | 430 | reuters.276702 | 
| Hole | news | 10 | 272 | sky.com.20667 |
| Whistle | news | 6 | 219 | nytimes.231903 |
| China | news | 12 | 357 | en.ndtv.com.13143 |
| Vaping | news | 21 | 533 | heraldscotland.com.7318 |
| Turner | news | 8 | 303 | euronews-en.185744 |
| Bible | bible | 16 | 338 | UEDIN |
| Lease | agreement | 29 | 597 | Translated by Ondřej |
| Audit (I)ntroduction | audit | 18 | 433 | Provided by NKÚ |
| Audit (R)ecommendation | audit | 6 | 121 | Provided by NKÚ |
| __Total__ | | __150__ | __3968__ | |

## Proposal 2

| Document name | domain | lines | src words | description |
|-|-|-|-|-|
| Hole | news | 10 | 272 | sky.com.20667 |
| Whistle | news | 6 | 219 | nytimes.231903 |
| China | news | 12 | 357 | en.ndtv.com.13143 |
| Turner | news | 8 | 303 | euronews-en.185744 |
| Bible | bible | 16 | 338 | UEDIN |
| Lease | agreement | 29 | 597 | Translated by Ondřej |
| Audit (I)ntroduction | audit | 18 | 433 | Provided by NKÚ |
| Audit (R)ecommendation | audit | 6 | 121 | Provided by NKÚ |
| __Total__ | | __105__ | __2640__ | |

## Proposal 3

| Document name | domain | lines | src words | description |
|-|-|-|-|-|
| Hole | news | 10 | 272 | sky.com.20667 |
| Whistle | news | 6 | 219 | nytimes.231903 |
| China | news | 12 | 357 | en.ndtv.com.13143 |
| Turner | news | 8 | 303 | euronews-en.185744 |
| QTLeap | technical | 11 | 178 | Batch2q\_cs\_v1010, Batch1a\_en\_v1.4.NAF |
| Lease | agreement | 29 | 597 | Translated by Ondřej |
| Audit (I)ntroduction | audit | 18 | 433 | Provided by NKÚ |
| Audit (R)ecommendation | audit | 6 | 121 | Provided by NKÚ |
| __Total__ | | __100__ | __2480__ | |

# Acknowledgement

Supported by [Memsource](https://memsource.com).

# References
1. https://www.cs.jhu.edu/~phi/publications/machine-translation-quality.pdf
2. https://www.dlsi.ua.es/~fsanchez/pub/pdf/forcada17a.pdf
