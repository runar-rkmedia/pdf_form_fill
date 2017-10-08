import { TSAppViewModel } from "./AppViewModel"
import { RoomInterface, Room } from "./Room"
import { RoomList } from "./RoomList"
import { Company } from "./ControlPanel"
import { StrIndex, AddressFullInterface, HTTPVerbs, Post, AddressInterface } from "./Common"
// This will be removed once `addresses` have been updated.
let titleCase = require('title-case')


export interface CustomerInterface {
  id: number;
  name: string;
  address: AddressFullInterface;
  rooms?: RoomInterface[];
}

export class Customer extends Post {
  url = '/json/v1/customer/'
  name: KnockoutObservable<string> = this.obs_mod()
  address1: KnockoutObservable<string> = this.obs_mod()
  address2: KnockoutObservable<string> = this.obs_mod()
  post_code: KnockoutObservable<number> = this.obs_mod()
  post_area: KnockoutObservable<string> = this.obs_mod()
  corporate_customer: KnockoutObservable<boolean> = ko.observable(false)
  extra_info: KnockoutObservable<boolean> = ko.observable(true)
  exstra_address: KnockoutObservable<boolean> = ko.observable(false)
  root: TSAppViewModel
  loading: KnockoutObservable<boolean> = ko.observable(false)
  rooms: KnockoutObservable<RoomList> = ko.observable(new RoomList(this.root, this))
  validationModel = ko.validatedObservable({
    name: this.name,
    address1: this.address1,
    address2: this.address2,
    post_code: this.post_code,
    post_area: this.post_area,
  })
  company = new Company()
  orgnumber: KnockoutObservable<number> = ko.observable()
  id: KnockoutObservable<number> = ko.observable()
  serialize: KnockoutObservable<CustomerInterface>
  constructor(parent: TSAppViewModel, id: number = -1000, root: TSAppViewModel = parent) {
    super(parent)
    this.root = parent
    this.id(id)
    this.name.extend(
      { required: false, minLength: 3, maxLength: 100 });
    this.address1.extend(
      { required: true, minLength: 2, maxLength: 200 });
    this.address2.extend(
      { required: false, maxLength: 200 });
    this.post_area.extend(
      { required: true, minLength: 2, maxLength: 100 });
    this.post_code.extend(
      { required: true, number: true, min: 0, max: 9999 });
    this.serialize = ko.computed((): CustomerInterface => {
      let t = {
        name: this.name(),
        id: this.id(),
        address: {
          address1: this.address1(),
          address2: this.address2(),
          post_code: this.post_code(),
          post_area: this.post_area(),
        }
      }
      return t
    })
    ko.computed(() => {
      if (this.corporate_customer()) {
        this.name(this.company.name())
        this.address1(this.company.address1())
        this.address2(this.company.address2())
        this.post_area(this.company.post_area())
        this.post_code(this.company.post_code())
        this.validationModel.errors.showAllMessages(false)
      }
    })
  }
  sub_modified = ko.computed(() => {
    if (this.rooms()) {
      for (let room of this.rooms().list()) {
        if (room.modified() || room.sub_modified()) {
          return true
        }
      }
    }
    return false
  })
  can_fill_form = ko.computed(() => {
    if (this.modified() || this.sub_modified()) {
      return false
    }
    if (this.rooms().list().length == 0) {
      return false
    }
    for (let room of this.rooms().list()) {
      if (room.heating_cables().list().length > 0) {
        return true
      }
    }
    return false
  })


  set(result: CustomerInterface) {
    if (result.id) {
      this.id(result.id)
    }
    if (result.name) {
      this.name(result.name)
    }
    if (result.address) {
      this.address1(result.address.address1)
      this.address2(result.address.address2)
      this.post_code(result.address.post_code)
      this.post_area(result.address.post_area)
    }
    if (result.rooms) {
      this.rooms(new RoomList(this.root, this, result.rooms))
    }
    this.save()
  }
  remove_instance() {
    this.parent.customer(new Customer(this.parent))
  }
  confirm_create_new = () => {
    if (this.modified() || this.sub_modified()) {
      this.comfirm_unsaved_dialog('Opprette ny kunde', 'Er du sikker på at du vil opprette en ny kunde?', this.create_new)
    } else {
      this.create_new()
    }
  }
  create_new = () => {
    this.set({
      id: -1,
      name: '',
      address: {
        address1: '',
        address2: '',
        post_code: null,
        post_area: ''
      },
      rooms: []
    })
    this.validationModel.errors.showAllMessages(false)
    $('#customer_form_collapse').collapse('show')
  }
  get = (id?: number) => {
    this.loading(true)
    $.get("/json/v1/customer/", { id })
      .done((result: CustomerInterface) => {
        this.set(result)
      })
      .always(() => {
        this.loading(false)
      })
  }
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
    if (this.address1()) {
      url += '&p=' + this.address1()
    }
    return url
    // We need a rateLimiter here so that the url doesn't change too early
    // when a user clicks a selection.
  }).extend({ rateLimit: 50 })
}
