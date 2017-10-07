 -negfdf - -fdfgen
https://github.com/ccnmtl/fdfgen
https://github.com/ccnmtl/fdfgenfdf# wip pdf-fill-forms

This is a work in progress. The goal of this project is to create a webpage or an app that workers can use on-site to fill pdfforms.

## mac-users

One of the dependencies, `pdftk` currently has a problem under El Capitan and newer. This has been fixed unofficially. There is a working release on [StackOverflow](https://stackoverflow.com/a/33248310/3493586).

Notes:

Currently, the pdfs are just stored on the server. This is okey, as the user will most likely be downloading the file straight away. I do not plan on storing the pdfs long-term, since it is cheaper to just store the values, and re-filling the pdf-template-forms as necacary.

Might integrate with DropBox, to simply store the company's files there.

For that reason, I don't see a problem in storing the pdf's on herokus [Ephemeral filesystem](https://devcenter.heroku.com/articles/dynos#ephemeral-filesystem) for the 5-minute-window a user might need to download his pdf.

## Get started:

### Virtial environment

Make sure you have python installed. Create the virtual ennvironment by running `python3 -m venv venv ` then activate it with `. venv/bin/activate `.

Install all pip-requirements with `pip install -r requirements.txt`





The `mongodb`- and `postgres`-databases needs to be initialized before we can run the app. Otherwise, there will only be a timeout when attempting to start the applications.

### mongodb

Make sure `mongodb` is running, either with a `brew services start mongodb`, or running `mongod`.

to set the initial data, run
```
cd addresses
python populate_db_pymongo.py --setup
```

### postgres

Make sure `postgres` is running, with `brew services start postgres`. You then need to create two databases, one for the list of products, and one for user-content and app-related. By default, these are called `varmekabler` and `vk_products`, but can be overridden by environment-variables 'DATABASE_URL' and 'PRODUCT_DATABASE_URL'.

To create the database-tables and intital content run
```
cd vk_data_extract
python setup.py create products rooms
```

also, to create a static json-file with the data, run
`python app.py static`

### npm

run `npm run start` while in dev, `npm run build` when in production. Also, there is `npm run penthouse` to create the critical css.

### Running locally

The application uses OAuth to authenticate users. This only works on https, so to run it on a local computer, set the environment-variable 'OAUTHLIB_INSECURE_TRANSPORT' to 'True'.

Note that you should not do this in production.

It is easiest to set environment-variables locally by using the file `instance/config.cfg`, or you could use `export OAUTHLIB_INSECURE_TRANSPORT=!`.


## To do:

 - [X] Øglænd
 - [ ] TermoFloor
 - [X] Adresse-lookup
 - [X] Lagre skjema
 - [X] Lagre kunder
 - [X] Lagre firma
 - [X] Lagre bruker
 - [X] proff.no

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
https://www.nexans.no/eservice/Norway-no_NO/fileLibrary/Download_540156630/Norway/files/2015_Varmehandboka.pdf
https://www.nexans.no/eservice/Norway-en/fileLibrary/Download_540158896/Norway/files/Warranty_form_heating-cables_multi.pdf
