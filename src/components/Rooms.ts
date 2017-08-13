import { HTTPVerbs, ByID, Post } from "./Common"
import { TSAppViewModel } from "./AppViewModel"
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
export interface RoomSmartFill {
  name: string;
  outside?: boolean;
  aliases?: string[]
  maxEffect: number
  normalEffect: number
}

export let RoomSuggestionList: RoomSmartFill[] = [
  {
    name: 'Stue',
    aliases: ['Kjøkken', 'Soverom', 'Barnerom', 'Kjellerstue'],
    maxEffect: 100,
    normalEffect: 85
  },
  {
    name: 'Baderom',
    aliases: [
      'Badegulv', 'Vaskerom', 'Hall', 'Bad', 'WC', 'Toalett', 'Gang',
      'Vindfang'],
    maxEffect: 160,
    normalEffect: 135
  },
  {
    name: 'Snøsmelting',
    outside: true,
    aliases: ['Gate', 'Fortau', 'Rampe', 'Terrasse', 'Trapp', 'Hjulspor', 'Gårdsplass', 'Tunet'],
    maxEffect: 1000,
    normalEffect: 300
  },
  {
    name: 'Snøsmelting med automatikk',
    outside: true,
    maxEffect: 1000,
    normalEffect: 350
  },
  {
    name: 'Tregulv',
    maxEffect: 80,
    normalEffect: 60
  },
  {
    name: 'Fryseromsgulv',
    maxEffect: 15,
    normalEffect: 12.5
  },
  {
    name: 'Betongherding',
    maxEffect: 1000,
    normalEffect: 110
  },
  {
    name: 'Idrettsanlegg',
    aliases: ['Fotballbane'],
    maxEffect: 1000,
    normalEffect: 60
  },
  {
    name: 'Gartneri',
    maxEffect: 1000,
    normalEffect: 80
  },
  {
    name: 'Magasinvarme',
    maxEffect: 250,
    normalEffect: 215
  }
]

export interface RoomSuggestionInterface {
  name: string,
  id: number
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
  }
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


  suggestRoom = () => {
    let listOfRooms: RoomSuggestionInterface[] = []
    RoomSuggestionList.forEach((room, index) => {
      listOfRooms.push({
        name: room.name,
        id: index
      })
      if (room.aliases) {
        for (let alias of room.aliases) {
          listOfRooms.push({
            name: alias,
            id: index
          })
        }
      }
    })
    return listOfRooms
  };

  roomSuggestionOnSelect = (
    value: KnockoutObservable<string>,
    roomSuggestion: RoomInterface,
    event: Event
  ) => {
    let room_data = RoomSuggestionList[roomSuggestion.id]
    this.outside(Boolean(room_data.outside))
    this.maxEffect(room_data.maxEffect)
    this.normalEffect(room_data.normalEffect)
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
    let first_input = panel.find('input:text').first()
    panel.removeClass('collapse')
    first_input.focus()
    return new_room
  }
}
