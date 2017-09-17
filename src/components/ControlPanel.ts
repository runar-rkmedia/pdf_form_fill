require("knockout-template-loader?name=brregsuggestion-template!html-loader?-minimize!./brregsuggestion.html");
import { } from '@types/googlemaps';


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
  lat: KnockoutObservable<number> = ko.observable()
  lng: KnockoutObservable<number> = ko.observable()
  geocoder: google.maps.Geocoder
  map: any
  marker: any
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
    this.get_geo_code(data)
  }
  get_geo_data(data: {}) {
    return $.get('https://maps.googleapis.com/maps/api/geocode/json',
      Object.assign(data, { key: 'AIzaSyD8P9OPG70WZhy2YjxdF - oR47FQHJOiFFA' })
    )
  }
  get_geo_code(address: Brreg_addresse) {
    let query: any[] = []
    let query_components = [
      address.adresse,
      address.poststed,
      address.postnummer,
      address.land
    ]
    for (let component of query_components) {
      if (component) {
        query.push(component)
      }
    }
    this.get_geo_data({
      address: query.join(', '),
    }).done((result) => {
      if (result.status == 'OK') {
        this.lat(result.results[0].geometry.location.lat)
        this.lng(result.results[0].geometry.location.lng)
      } else {
        query.splice(query.indexOf(address.adresse), 1)
        this.get_geo_data({ address: query.join(', ') })
          .done((result => {
            if (result.status == 'OK') {
              this.lat(result.results[0].geometry.location.lat)
              this.lng(result.results[0].geometry.location.lng)
            } else {
              console.log('failed geo-lookup twice:', result, address)
            }
          }))
      }
    }
      )
  }
  addMapsScript() {
    let googleMapsUrl = 'https://maps.googleapis.com/maps/api/js?key=AIzaSyD8P9OPG70WZhy2YjxdF-oR47FQHJOiFFA'
    if (!document.querySelectorAll(`[src="${googleMapsUrl}"]`).length) {
      document.body.appendChild(Object.assign(
        document.createElement('script'), {
          type: 'text/javascript',
          src: googleMapsUrl,
          onload: () => this.doMapInitLogic()
        }));
    } else {
      this.doMapInitLogic();
    }
  }
  doMapInitLogic() {
    this.geocoder = new google.maps.Geocoder
    this.map = new google.maps.Map(document.getElementById('map'), {
      zoom: 4,
      center: { lat: 65, lng: 12.5 }
    });
    this.marker = new google.maps.Marker({
      position: { lat: 65, lng: 12 },
      map: this.map,
      draggable: true
    });
    this.marker.addListener('dragend', (event: any) => {
      this.lat(event.latLng.lat())
      this.lng(event.latLng.lng())
    })
    if (this.lat() && this.lng()) {
      this.lat.notifySubscribers()
    }
  }
  set_geo_from_address() {
    this.get_geo_code({
      adresse: this.address1(),
      postnummer: this.post_code(),
      poststed: this.post_area(),
      kommunenummer: -1,
      kommune: '',
      landkode: -1,
      land: 'Norge'
    })
  }
  geoListener = ko.computed(() => {
    if (this.lat() && this.lng() && this.map) {
      let position = new google.maps.LatLng(this.lat(), this.lng())
      let zoom = this.map.getZoom()
      google.maps.event.trigger(this.map, 'resize')
      this.marker.setPosition(position)
      this.map.panTo(position)
      this.map.setZoom(10)
    }
  })
  autocompleteBRreg = ko.computed(() => {
    let url: string = "https://data.brreg.no/enhetsregisteret/enhet.json?$filter=startswith(navn,'%QUERY')&size=10"
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
  }
  get_invite() {
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
