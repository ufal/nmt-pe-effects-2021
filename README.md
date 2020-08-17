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

# Acknowledgement

Supported by [Memsource](https://memsource.com).

# References
1. https://www.cs.jhu.edu/~phi/publications/machine-translation-quality.pdf
2. https://www.dlsi.ua.es/~fsanchez/pub/pdf/forcada17a.pdf