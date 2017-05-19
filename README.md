 -negfdf - -fdfgen
https://github.com/ccnmtl/fdfgen
https://github.com/ccnmtl/fdfgenfdf# wip pdf-fill-forms

This is a work in progress. The goal of this project is to create a webpage or an app that workers can use on-site to fill pdfforms.


## To do:

### MWE:
 - [ ] Type
 - [ ] Nominell motstand
 - [ ] ohm
 - [ ] mohm
 - [ ] dato
 - [ ] oppvarmet_areal
 - [X] flateeffekt(calc)
 - [ ] Følertype

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
