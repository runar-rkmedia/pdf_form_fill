 -negfdf - -fdfgen
https://github.com/ccnmtl/fdfgen
https://github.com/ccnmtl/fdfgenfdf# wip pdf-fill-forms

This is a work in progress. The goal of this project is to create a webpage or an app that workers can use on-site to fill pdfforms.

## mac-users

One of the dependencies, `pdftk` currently has a problem under El Capitan and newer. This has been fixed unofficially. There is a working release on [StackOverflow](https://stackoverflow.com/a/33248310/3493586).

Notes:

Currently, the pdfs are just stored on the server. This is okey, as the user will most likely be downloading the file straight away. I do not plan on storing the pdfs long-term, since it is cheaper to just store the values, and re-filling the pdf-template-forms as necacary.

For that reason, I don't see a problem in storing the pdf's on herokus [Ephemeral filesystem](https://devcenter.heroku.com/articles/dynos#ephemeral-filesystem) for the 5-minute-window a user might need to download his pdf.

## To do:

 - [X] Øglænd
 - [ ] TermoFloor
 - [ ] VarmeComfort
 - [ ] 1881
 - [ ] Lagre skjema
 - [ ] Lagre kunder
 - [ ] Lagre firma
 - [ ] Lagre bruker
 - [ ] proff.no

## Why not just use Acrobat?

Many times in these pdfs, the same information is filled every time manually, with no logic behind the scenes. Filling company info, name, date and signature is of course something existing applications can do, but this solution is more specific to our campanys usecase, allthough it can easily be extended to other usecases.

For instance, filling information about a product used is often a chore, with many different fields needing input, like produkt-name, spesifications, values and so on. By simply inputting manufacturor from a drop-down-menu, selecting its type and main value, we have enough enformation to fill all the other fields about the product.

## Dependencies:

- [PDF Toolkit][pdftk]
- [fdfgen library][8e184bcc]

  [pdftk]: http://www.pdflabs.com/tools/pdftk-server/
  [8e184bcc]: https://github.com/ccnmtl/fdfgen "fdfgen library"

## Referances:

http://evanfredericksen.blogspot.no/2014/03/manipulating-pdf-form-fields-with-python.html
