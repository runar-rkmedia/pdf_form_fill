import { TSAppViewModel } from "./AppViewModel"
import { RoomInterface, Rooms, Room } from "./Rooms"
import { StrIndex, AddressFullInterface, HTTPVerbs, Post, AddressInterface } from "./Common"
import ko = require("knockout");
let titleCase = require('title-case')


export interface CustomerInterface {
  id: number;
  name: string;
  address: AddressFullInterface;
  rooms?: RoomInterface[];
}

export class Customer extends Post {
  url = '/json/v1/customer/'
  name: KnockoutObservable<string> = this.observable_modification()
  address1: KnockoutObservable<string> = this.observable_modification()
  address2: KnockoutObservable<string> = this.observable_modification()
  post_code: KnockoutObservable<number> = this.observable_modification()
  post_area: KnockoutObservable<string> = this.observable_modification()
  root: TSAppViewModel
  rooms: KnockoutObservable<Rooms> = ko.observable(new Rooms(this.root, this))
  validationModel = ko.validatedObservable({
    name: this.name,
    address1: this.address1,
    address2: this.address2,
    post_code: this.post_code,
    post_area: this.post_area,
  })
  id: KnockoutObservable<number> = ko.observable()
  serialize: KnockoutObservable<CustomerInterface>
  constructor(parent: TSAppViewModel, id: number = -1, root: TSAppViewModel = parent) {
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

  }


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
      this.rooms(new Rooms(this.root, this, result.rooms))
    }
    this.save()
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
  }
  get = (id?: number) => {
    $.get("/json/v1/customer/", { id })
      .done((result: CustomerInterface) => {
        this.set(result)
      })
  }
  suggestionOnSelect = (
    value: KnockoutObservable<{}>,
    address: AddressInterface,
    event: any,
    element: any) => {
    value(titleCase(address.street_name))
    this.post_code((address.post_code))
    this.post_area(address.post_area.toUpperCase())
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
