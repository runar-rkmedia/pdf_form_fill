import { Company } from "./ControlPanel"

import { StrIndex, AddressFullInterface, Base, Post, AddressInterface, ObsMod } from "./Common"
require("knockout-template-loader?name=customer-input-template!html-loader?-minimize!./customer_input.html");
// This will be removed once `addresses` have been updated.
let titleCase = require('title-case')

export interface CustomerDataInterface {
  data_type: string
  address: AddressFullInterface;
  customer_name: string;
  contact_name: string;
  phone: number | null;
  mobile: number | null;
  orgnumber: number | null;
}
var patterns = {
  email: /^([\d\w-\.]+@([\d\w-]+\.)+[\w]{2,4})?$/,
  phone: /^\d{8}$|^00\d{3,20}$/,
  postcode: /^\d{4}$/
};

ko.validation.rules['norPhone'] = {
  validator: function(val, required) {
    if (!required && !val) {
      return true
    }
    return /^\d{8}$|^00\d{3,20}$/.test(val);
  },
  message: '8 siffer. For internasjonale nummer, bruk 00 foran.'
};
ko.validation.rules['orgnumber'] = {

  validator: function(val, required) {
    if (!required && !val) {
      return true
    }
    return /^\d{9}$/.test(val);
  },
  message: 'Organisasjonsnummer skal ha 9 siffer'
};
ko.validation.rules['post_code'] = {
  validator: function(val, condition) {
    let required = false;
    if (typeof condition == 'function') {
      required = condition();
    }
    else {
      required = condition;
    }

    if (required) {
      return /^$|^\d{4}$/.test(val);
    }
    else {
      return /^$|^\d{4}$/.test(val);
    }
  },
  message: '4 siffer'
};

let pad = (n: string, width: number, z: string = "0") => {
  // Pad a string(n), to a certain (width), and pad with (z)
  n = n + '';
  return n.length >= width ? n : new Array(width - n.length + 1).join(z) + n;
}
ko.validation.registerExtenders();
export class CustomerData extends Base {
  data_type: string
  name: KnockoutObservable<string> = this.obs_mod()
  address1: KnockoutObservable<string> = this.obs_mod()
  address2: KnockoutObservable<string> = this.obs_mod()
  post_code: KnockoutObservable<string | null> = this.obs_mod()
  post_area: KnockoutObservable<string> = this.obs_mod()
  contact_name: KnockoutObservable<string> = this.obs_mod()
  phone: KnockoutObservable<number> = this.obs_mod()
  mobile: KnockoutObservable<number> = this.obs_mod()
  corporate_customer: KnockoutObservable<boolean> = ko.observable(false)
  company = new Company()
  validationModel = ko.validatedObservable({
    name: this.name,
    address1: this.address1,
    address2: this.address2,
    post_code: this.post_code,
    post_area: this.post_area,
    contact_name: this.contact_name,
    phone: this.phone,
    mobile: this.mobile,
    orgnumber: this.company.orgnumber,
  })
  constructor(data_type: string, required: boolean) {
    super()
    this.data_type = data_type
    let as_long_as = (params: any) => {
      let d = { onlyIf: () => { return required || this.address1() }, params: params }
      return d
    }
    this.name.extend(
      { required: false, minLength: 3, maxLength: 100 });
    this.address1.extend(
      { required: required, minLength: { onlyIf: () => { return required }, params: 2 }, maxLength: 200 });
    this.address2.extend(
      { required: false, maxLength: 200 });
    this.post_area.extend({
      required: as_long_as(true), minLength: as_long_as(2), maxLength: 100
    });
    this.post_code.extend({ required: as_long_as(true), post_code: as_long_as(true) });
    this.contact_name.extend({ required: false, minLength: 2, maxLength: 100 });
    this.phone.extend({ required: false, norPhone: false });
    this.mobile.extend({ required: false, norPhone: false });
    this.company.orgnumber.extend({
      required: false, orgnumber: false
    });
    ko.computed(() => {
      if (this.corporate_customer()) {
        if (this.company.name()) {
          this.name(this.company.name())
        }
        if (this.company.address1()) {
          this.address1(this.company.address1())
          this.address2(this.company.address2())
          this.post_area(this.company.post_area())
          this.post_code(this.company.post_code())
        }
      }
    })
  }
  serialize = ko.computed((): CustomerDataInterface => {
    let t: any = {
      data_type: this.data_type,
      address: {
        address1: this.address1(),
        address2: this.address2(),
        post_code: this.post_code(),
        post_area: this.post_area(),
      },
      // orgnumber: undefined,
      contact_name: this.contact_name(),
      orgnumber: this.company.orgnumber(),
      phone: this.phone(),
      mobile: this.mobile(),
      customer_name: this.name(),
    }
    return t
  })
  save() {
    this.company.save()
    super.save()
  }
  set(result: CustomerDataInterface) {
    this.company.orgnumber(result.orgnumber)
    this.corporate_customer(Boolean(result.orgnumber))
    this.address1(result.address.address1)
    this.address2(result.address.address2)
    this.post_code(pad(result.address.post_code || '0', 4))
    this.post_area(result.address.post_area)
    this.phone(result.phone)
    this.mobile(result.mobile)
    this.contact_name(result.contact_name)
    this.name(result.customer_name)
    this.company.name(result.customer_name)

    this.save()
  }
  modified = ko.computed(() => {
    if (this.company.modified()) {
      return true
    }
    return this.modification_check(this.modification_tracking_list())
  })
  suggestionOnSelect = (
    value: KnockoutObservable<{}>,
    address: AddressInterface,
    event: Event,
    element: any) => {
    value(titleCase(address.street_name))
    this.post_code((address.post_code))
    this.post_area(address.post_area.toUpperCase())
    setTimeout(() => {
      $(event.target).focus()
    }, 50)
  }
  autocompleteAddress = ko.computed(() => {
    let url: string = '/address/?q=%QUERY'
    if (this.address1) {
      if (this.address1()) {
        url += '&p=' + this.address1()
      }
    }
    return url
    // We need a rateLimiter here so that the url doesn't change too early
    // when a user clicks a selection.
  }).extend({ rateLimit: 50 })
}
