- sent = sentence-level CUBBITT 2020
- doc  = document-level CUBBITT 2020

- The number in the filename is the number of training steps.
- The batch size was 23200 tokens for sent model and 18000 tokens for the doc model.
- The subword vocabulary size was 32k.
- The training speed was about 3466 steps per hour (on 10 GPUs).

| MODEL              | BLEU<br>pe  | BLEU<br>wmt0818 | Name | Previous Name | Note |
|-|-|-|-|-|-|
| sent-25385.txt     | 25.35 | 19.07 | M01 | P01 | the first checkpoint available with avg8 (after 7 hours of training)|
| sent-29022.txt     | 31.61 | 22.44 | M02 | P02.1 | |
| sent-29333.txt     | 33.09 | 23.86 | M03 | P02.2 | |
| sent-32966.txt     | 33.63 | 24.42 | M04 | P02 | |
| sent-72836.txt     | 35.22 | 26.25 | M05 | P03 | until here the dev-set BLEU curves grows monotonically (despite BlockBT training), the "second peak" ~ 6-7auth + 1-2synth checkpoints in avg8 |
| sent-148593.txt    | 37.17 | 27.87 |     | P04 | the nearest following "first peak" ~ 1-2 synth + 6-7 auth |
| sent-184873.txt    | 36.64 | 28.00 |     | P05 | the nearest following "second peak" ~ 6-7 auth + 1-2 synth |
| sent-271937.txt    | 37.12 | 28.38 |     | P06 | the nearest following "first peak" ~ 1-2 synth + 6-7 auth |
| sent-311870.txt    | 36.13 | 28.60 |     | P07 | the nearest following "second peak" ~ 6-7 auth + 1-2 synth |
| sent-997083.txt    | 35.68 | 26.64 | M06 | P08 | "end of valley" ~ 8 synth |
| sent-1015168.txt   | 36.58 | 28.14 | M07 | P09 | "before the first peak" ~ 5 auth + 3 synth |
| sent-1022401.txt   | 36.41 | 28.84 | M08 | P10 | "first peak" ~ 1-2 synth + 6-7 auth |
| sent-1054981.txt   | 37.40 | 28.72 | M09 | P11 | "before the second peak" ~ 8 auth|
| sent-1058593.txt   | 37.44 | 28.95 | M10 | P12 | submitted to WMT2020 as CUNI-Transformer; "second peak" ~ 6-7 auth + 1-2 synth |
| doc-698515.txt     | 37.37 | 28.46 | M11 | P13 | submitted to WMT2020 as CUNI-DocTransformer; "second peak" ~ 5 auth + 3 synth |
| google.txt         | 37.56 | 26.06 |     |     |  |
| microsoft.txt      | 33.06 | 26.30 |     |     |  |

BLEU was computed with `sacrebleu -w 2`.

BLEU-pe is BLEU computed on [our PE set](https://github.com/ELITR/nmt-pe-effects-2020/blob/master/docs/translations/sgm/REFERENCE.sgm).
BLEU-wmt0818 is BLEU computed on the dev set: WMT08, WMT09...WMT18 concatenated, but only orig-en and orig-cs docs.

The graph below shows "sacrebleu -lc -tok intl", but the "PE" test set contained extra lines with "DOC=monsoon", so the BLEU scores are bit different than above - I am sorry for this confusion.

![BLEU learning curves](BLEU-sent-cubbitt-2020.png)
