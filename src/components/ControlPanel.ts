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

ko.bindingHandlers.initValue = {
  init: function(element, valueAccessor) {
    var value = valueAccessor();
    if (!ko.isWriteableObservable(value)) {
      throw new Error('Knockout "initValue" binding expects an observable.');
    }
    value(element.value);
  }
};

ko.bindingHandlers.valueWithInit = {
  init: function(element, valueAccessor, allBindings, data, context) {
    ko.applyBindingsToNode(element, { initValue: valueAccessor() }, context);
    ko.applyBindingsToNode(element, { value: valueAccessor() }, context);
  }
};

export class Company {
  search: KnockoutObservable<string> = ko.observable()
  addresses: KnockoutObservableArray<Brreg_addresse> = ko.observableArray()
  selected_result: KnockoutObservable<Brreg> = ko.observable()
  name: KnockoutObservable<string> = ko.observable()
  address1: KnockoutObservable<string> = ko.observable()
  address2: KnockoutObservable<string> = ko.observable()
  post_code: KnockoutObservable<number> = ko.observable()
  post_area: KnockoutObservable<string> = ko.observable()
  selected_address: KnockoutComputed<number> = ko.computed(() => {
    if (this.address2() != null) {
      return -1
    }
    for (let i = 0; i < this.addresses().length; i++) {
      let address = this.addresses()[i]
      if (
        address.adresse == this.address1() &&
        address.postnummer == this.post_code() &&
        address.poststed == this.post_area()
      ) {
        return i
      }
    }
    return -1
  })

  links: KnockoutObservableArray<Brreg_links> = ko.observableArray([])
  orgnumber: KnockoutObservable<number> = ko.observable()
  suggestionOnSelect = (
    value: KnockoutObservable<{}>,
    data: Brreg,
    event: any,
    element: any) => {
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
      this.addresses.push(Object.assign(data.postadresse, { type: 'Postadresse' }))
    }
    if (this.addresses().length > 0) {
      this.set_address(this.addresses()[0])
    }
  }
  set_address = (data: Brreg_addresse) => {
    this.address1(data.adresse)
    this.address2(null)
    this.post_code(data.postnummer)
    this.post_area(data.poststed)
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

export class ControlPanel {
  invites: KnockoutObservableArray<string> = ko.observableArray()
  base_url: KnockoutObservable<string> = ko.observable('abc')
  constructor() {
    $.get("/invite.json")
      .done((result) => {
        this.invites(result.invites);
        this.base_url(result.base_url);
      });
  }
  createInvite() {
    $.post("/invite.json")
      .done((result) => {
        if (result.invites) {
          this.invites(result.invites);
        }
        if (result.base_url) {
          this.base_url(result.base_url);
        }
      })
      .fail(function(result, t, d) {
        $('.flash').append('<li class="error">' + result.responseText + '</li>')
      })
  }
}
