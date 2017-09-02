require("knockout-template-loader?name=brregsuggestion-template!html-loader?-minimize!./brregsuggestion.html");

// https://confluence.brreg.no/display/DBNPUB/Informasjonsmodell+for+Enhetsregisteret+og+Foretaksregisteret

interface Brreg_addresse {
  adresse: string
  postnummer: number
  poststed: string
  kommunenummer: number
  kommune: string
  landkode: number
  land: string
  type?: string
}

interface Brreg_links {
  rel: string
  href: string
}
interface Brreg {
  navn: string
  organisasjonsnummer: number
  postadresse: Brreg_addresse
  forretningsadresse: Brreg_addresse
  links: Brreg_links[]
}


export class Company {
  search: KnockoutObservable<string> = ko.observable()
  addresses: KnockoutObservableArray<Brreg_addresse> = ko.observableArray()
  selected_result: KnockoutObservable<Brreg> = ko.observable()
  name: KnockoutObservable<string> = ko.observable()
  address1: KnockoutObservable<string> = ko.observable()
  address2: KnockoutObservable<string> = ko.observable()
  post_code: KnockoutObservable<number> = ko.observable()
  post_area: KnockoutObservable<string> = ko.observable()

  links: KnockoutObservableArray<Brreg_links> = ko.observableArray([])
  orgnumber: KnockoutObservable<number> = ko.observable()
  suggestionOnSelect = (
    value: KnockoutObservable<{}>,
    data: Brreg,
    event: any,
    element: any) => {
    this.name()
    console.log(data)
    value(data.navn)
    this.name(data.navn)
    this.links(data.links)
    this.orgnumber(data.organisasjonsnummer)
    this.selected_result(data)
    this.addresses.removeAll()
    if (data.forretningsadresse) {
      this.addresses.push(Object.assign(data.forretningsadresse, { type: 'Forretningsadresse' }))
    }
    if (data.postadresse) {
      this.addresses.push(Object.assign(data.postadresse, { type: 'Forretningsadresse' }))
    }
    if (this.addresses().length > 0) {
      this.address1(this.addresses()[0].adresse)
      this.address2(null)
      this.post_code(this.addresses()[0].postnummer)
      this.post_area(this.addresses()[0].poststed)
    }
  }
  autocompleteBRreg = ko.computed(() => {
    let url: string = "http://data.brreg.no/enhetsregisteret/enhet.json?$filter=startswith(navn,'%QUERY')&size=10"
    return url
    // We need a rateLimiter here so that the url doesn't change too early
    // when a user clicks a selection.
  }).extend({ rateLimit: 50 })
  brreg_remote_filter = (response: any) => {
    return response.data;
  }
}
