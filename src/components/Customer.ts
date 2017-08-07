import { TSAppViewModel } from "./AppViewModel"
import { RoomInterface } from "./Rooms"
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
  constructor () {
    this.name.extend(
      {required: false, minLength: 3, maxLength: 100});
    this.address1.extend(
      {required: true, minLength: 2, maxLength: 200});
    this.address2.extend(
      {required: false, maxLength: 200});
    this.post_area.extend(
      {required: true, minLength: 2, maxLength: 100});
    this.post_code.extend(
      {required: true, number: true, min: 0, max: 9999});
  }
}
