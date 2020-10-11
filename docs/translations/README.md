- sent = sentence-level CUBBITT 2020
- doc  = document-level CUBBITT 2020

- The number in the filename is the number of training steps.
- The batch size was 23.200 tokens for sent model and 18.000 tokens for the doc model.
- The subword vocabulary size was 32k.
- The training speed was about 3466 steps per hour (on 10 GPUs).

| MODEL              | BLEU  | Name | note |
|-|-|-|-|
| sent-25385.txt     | 23.29 | M01 | |
| sent-32966.txt     | 31.58 | M02 | |
| sent-72836.txt     | 33.05 | M03 | |
| sent-148593.txt    | 34.96 | M04 | |
| sent-184873.txt    | 34.83 | M05 | |
| sent-271937.txt    | 35.25 | M06 | |
| sent-311870.txt    | 34.67 | M07 | |
| sent-997083.txt    | 32.69 | M08 | |
| sent-1015168.txt   | 34.44 | M09 | |
| sent-1022401.txt   | 34.81 | M10 | |
| sent-1054981.txt   | 35.55 | M11 | |
| sent-1058593.txt   | 34.77 | M12 | submitted to WMT2020 as CUNI-Transformer |
| doc-698515.sgm	 | 35.38 | M13 | submitted to WMT2020 as CUNI-DocTransformer |

## Details:
BLEU was computed with "sacrebleu -w 2". The checkpoints were chosen according to their dev-set (WMT08..WMT18 concatenated) BLEU.

- sent-25385 - the first checkpoint available with avg8 (after 7 hours of training)
- sent-32966 - 
- sent-72836 - until here the dev-set BLEU curves grows monotonically (despite BlockBT training), the "second peak" ~ 6-7auth + 1-2synth checkpoints in avg8 
- sent-148593 - the nearest following "first peak" ~ 1-2 synth + 6-7 auth
- sent-184873 - the nearest following "second peak" ~ 6-7 auth + 1-2 synth
- sent-271937 - the nearest following "first peak" ~ 1-2 synth + 6-7 auth
- sent-311870 - the nearest following "second peak" ~ 6-7 auth + 1-2 synth
- sent-997083 - "end of valley" ~ 8 synth
- sent-1015168 - "before the first peak" ~ 5 auth + 3 synth
- sent-1022401 - "first peak" ~ 1-2 synth + 6-7 auth
- sent-1054981 - "before the second peak" ~ 8 auth
- sent-1058593 - "second peak" ~ 6-7 auth + 1-2 synth
- doc-698515 - "second peak" ~ 5 auth + 3 synth