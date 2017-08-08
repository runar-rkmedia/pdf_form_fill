import { TSAppViewModel } from "./AppViewModel"
import { RoomInterface, Rooms, Room } from "./Rooms"
import {StrIndex, AddressFullInterface, HTTPVerbs}  from "./Common"
import ko = require("knockout");


export interface CustomerInterface {
  id: number;
  name: string;
  address: AddressFullInterface;
  rooms: RoomInterface[];
}

export class Customer {
  name: KnockoutObservable<string> = ko.observable()
  address1: KnockoutObservable<string> = ko.observable()
  address2: KnockoutObservable<string> = ko.observable()
  post_code: KnockoutObservable<number> = ko.observable()
  post_area: KnockoutObservable<string> = ko.observable()
  root: TSAppViewModel
  rooms: KnockoutObservable<Rooms> = ko.observable(new Rooms(this.root, this))
  parent: TSAppViewModel
  id: KnockoutObservable<number> = ko.observable()
  constructor(parent: TSAppViewModel, id: number = -1, root: TSAppViewModel = parent) {
    this.parent = parent
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
  }
  get = (id: number) => {
    $.get("/json/v1/customer/", { id })
      .done((result: CustomerInterface) => {
        this.address1(result.address.address1)
        this.address2(result.address.address2)
        this.post_code(result.address.post_code)
        this.post_area(result.address.post_area)
        this.parent.customer_id(result.id)
        let new_rooms = result.rooms.map((x) => {
          return new Room(this.root, this.rooms(), x)
        })
        this.rooms(new Rooms(this.root, this, new_rooms))
      })
  }
}
