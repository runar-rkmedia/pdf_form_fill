import { ByID, Post } from "./Common"
import { TSAppViewModel } from "./AppViewModel"
import { RoomTypesInfoFlat } from "./ProductModel"
import { CustomerInterface, Customer } from './Customer'
import { HeatingCable, HeatingCables, HeatingCableInterface } from './HeatingCable'

export interface RoomInterface {
  room_name: string;
  id: number;
  area: number | null;
  heated_area: number | null;
  outside: boolean;
  customer_id?: number
  heating_cables?: HeatingCableInterface[]
}

export class Room extends Post {
  url = '/json/v1/room/'
  id: KnockoutObservable<number> = ko.observable()
  name: KnockoutObservable<string> = ko.observable()
  outside: KnockoutObservable<boolean> = ko.observable()
  maxEffect: KnockoutObservable<number> = ko.observable()
  normalEffect: KnockoutObservable<number> = ko.observable()
  area: KnockoutObservable<number> = ko.observable()
  heated_area: KnockoutObservable<number> = ko.observable()
  heating_cables: KnockoutObservable<HeatingCables> = ko.observable()
  room_suggestion: KnockoutObservable<RoomSuggestion>
  validationModel = ko.validatedObservable({
    name: this.name,
    outside: this.outside,
    area: this.area,
    heated_area: this.heated_area
  })
  parent: Rooms
  root: TSAppViewModel
  last_sent_data: KnockoutObservable<RoomInterface> = ko.observable()
  serialize: KnockoutObservable<RoomInterface>

  constructor(root: TSAppViewModel, parent: Rooms, room: RoomInterface | undefined = undefined) {
    super()
    this.parent = parent
    this.root = root
    this.area.extend(
      { required: true, number: true, min: 0.1, max: 1000 });
    this.heated_area.extend(
      { required: true, number: true, min: 0.1, max: 1000 });
    this.name.extend(
      { required: true, minLength: 2, maxLength: 50 });

    this.serialize = ko.computed(() => {
      return {
        room_name: this.name(),
        id: this.id(),
        area: this.area(),
        heated_area: this.heated_area(),
        outside: this.outside(),
        customer_id: this.parent.parent.id()
      }
    })
    this.set(room)
    this.room_suggestion = ko.observable(
      new RoomSuggestion(this.root.Products().flat_room_type_info(),
        this))
  }
  room_effect = ko.computed((): number => {
    let sum_effect = 0
    if (this.heating_cables()) {
      for (let heating_cable of this.heating_cables().list()) {
        if (heating_cable.product()) {
          sum_effect += Number(heating_cable.product()!.effect)
        }
      }
    }
    return sum_effect
  })
  room_title = ko.computed(() => {
    if (this.id() >= 0) {
      let result = this.name()
      if (this.area()) {
        result += ', ' + this.area() + 'm²'
      }
      if (this.heated_area()) {
        result += ' (' + this.heated_area() + ' m²)'
      }
      return result
    }
    return 'Nytt rom/sted'
  }
  )
  bestFitEffect = ko.computed(() => {
    if (this.normalEffect() > 0 && this.heated_area() > 0) {
      return this.normalEffect() * this.heated_area()
    }
    return 0
  })
  modified = ko.computed(() => {
    if (!this.last_sent_data()) {
      return true
    }
    if (
      this.name() != this.last_sent_data().room_name ||
      this.outside() != this.last_sent_data().outside ||
      this.area() != this.last_sent_data().area ||
      this.heated_area() != this.last_sent_data().heated_area
    ) {
      return true
    }
    return false
  })
  // Add some additonal functionality when posting.
  post(h: any, event: Event, data_object?: any, url?: string) {
    return super.post(h, event, data_object, url).done(() => {
      $(event.target).closest('.collapse').collapse('hide')
    }
    )
  }
  save() {
    this.last_sent_data(this.serialize())
  }
  set(room: RoomInterface = {
    room_name: '',
    id: -1,
    area: null,
    heated_area: null,
    outside: false
  }) {
    this.name(room.room_name)
    this.id(room.id)
    this.area(room.area)
    this.heated_area(room.heated_area)
    this.outside(room.outside)
    this.heating_cables(new HeatingCables(this.root, this, room.heating_cables))
    this.save()
  }
}

export class Rooms extends ByID {
  list: KnockoutObservableArray<Room>
  parent: Customer
  root: TSAppViewModel

  constructor(root: TSAppViewModel, parent: Customer, list_of_rooms: Room[] = []) {
    super(list_of_rooms)
    this.parent = parent
    this.root = root
  }
  add = () => {
    let new_room = this.by_id(-1)
    if (!new_room) {
      this.list.push(new Room(this.root, this))
    }
    let accordian = $('#accordion-room')
    let panel = accordian.find('#room-1')
    let room_form = panel.find('#room-form-1')
    let first_input = panel.find('input').first()
    room_form.addClass('in')
    panel.collapse('show')
    // Focus does not work becaus of an issue with using typeahead.Workaround
    // with using a setTimeOut doesnt seemt to work inside animated stuff, so
    // for now, I will leave it not working.
    first_input.focus()
    return new_room
  }
}

export class RoomSuggestion {
  list: KnockoutObservableArray<RoomTypesInfoFlat> = ko.observableArray()
  parent: Room
  constructor(room_type_info_flat: RoomTypesInfoFlat[], room: Room) {
    this.list(room_type_info_flat)
    this.parent = room
  }
  suggestRoom = ko.computed(() => {
    return this.list()
  })
  roomSuggestionOnSelect = (
    value: KnockoutObservable<string>,
    roomSuggestion: RoomTypesInfoFlat,
    event: Event
  ) => {
    this.parent.outside(Boolean(roomSuggestion.outside))
    this.parent.maxEffect(roomSuggestion.maxEffect)
    this.parent.normalEffect(roomSuggestion.normalEffect)
  }
}
