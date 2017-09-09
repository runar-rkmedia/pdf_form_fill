import {
  ByID,
  Post,
  ObsMod,
} from "./Common"
import { TSAppViewModel } from "./AppViewModel"
import { RoomTypesInfoFlat } from "./ProductModel"
import { CustomerInterface, Customer } from './Customer'
import { HeatingCable, HeatingCables, HeatingCableInterface } from './HeatingCable'

interface CheckEarthed {
  cable_screen: boolean
  chicken_wire: boolean
  other: string
}

interface CheckMaxTemp {
  planning: boolean
  installation: boolean
  other: string
}

interface CheckControlSystem {
  floor_sensor: boolean
  room_sensor: boolean
  designation: string
  other: string
}

export interface RoomInterface {
  room_name: string;
  id: number;
  area: number | null;
  heated_area: number | null;
  outside: boolean;
  customer_id?: number
  heating_cables?: HeatingCableInterface[],
  maxEffect?: number
  normalEffect?: number
  check_earthed?: CheckEarthed
  check_max_temp?: CheckMaxTemp
  check_control_system?: CheckControlSystem
}

export class Room extends Post {
  url = '/json/v1/room/'
  id: KnockoutObservable<number> = ko.observable()
  name = <ObsMod<string>>this.obs_mod();
  outside = <ObsMod<boolean>>this.obs_mod();
  maxEffect = <ObsMod<number>>this.obs_mod();
  normalEffect = <ObsMod<number>>this.obs_mod();
  area = <ObsMod<number>>this.obs_mod();
  heated_area = <ObsMod<number>>this.obs_mod();
  earthed_cable_screen = <ObsMod<boolean>>this.obs_mod();
  earthed_chicken_wire = <ObsMod<boolean>>this.obs_mod();
  earthed_other = <ObsMod<string>>this.obs_mod();
  max_temp_limited_by_planning = <ObsMod<boolean>>this.obs_mod(undefined, undefined, true);
  max_temp_limited_by_installation = <ObsMod<boolean>>this.obs_mod(undefined, undefined, true);
  max_temp_limited_by_other = <ObsMod<string>>this.obs_mod();
  control_system_floor_sensor = <ObsMod<boolean>>this.obs_mod(undefined, undefined, true);
  control_system_room_sensor = <ObsMod<boolean>>this.obs_mod();
  control_system_designation = <ObsMod<string>>this.obs_mod();
  control_system_other = <ObsMod<string>>this.obs_mod();
  heating_cables: KnockoutObservable<HeatingCables> = ko.observable()
  room_suggestion: KnockoutObservable<RoomSuggestion>
  validationModel = ko.validatedObservable({
    name: this.name,
    outside: this.outside,
    area: this.area,
    heated_area: this.heated_area
  })
  root: TSAppViewModel
  serialize: KnockoutComputed<RoomInterface>

  constructor(root: TSAppViewModel, parent: Rooms, room: RoomInterface | undefined = undefined) {
    super(parent)
    this.root = root
    this.area.extend(
      { required: true, number: true, min: 0.1, max: 1000 });
    this.heated_area.extend(
      { required: true, number: true, min: 0.1, max: 1000 });
    this.name.extend(
      { required: true, minLength: 2, maxLength: 50 });

    this.modification_tracking_list([
      this.name,
      this.outside,
      this.maxEffect,
      this.normalEffect,
      this.area,
      this.heated_area,
      this.earthed_cable_screen,
      this.earthed_chicken_wire,
      this.earthed_other,
      this.max_temp_limited_by_planning,
      this.max_temp_limited_by_installation,
      this.max_temp_limited_by_other,
      this.control_system_floor_sensor,
      this.control_system_room_sensor,
      this.control_system_designation,
      this.control_system_other,
      // this.heating_cables,
      // this.room_suggestion,
    ]);

    this.serialize = ko.computed((): RoomInterface => {
      return {
        room_name: this.name(),
        id: this.id(),
        area: this.area(),
        heated_area: this.heated_area(),
        outside: this.outside(),
        customer_id: this.parent.parent.id(),
        maxEffect: this.maxEffect(),
        normalEffect: this.normalEffect(),
        check_earthed: {
          cable_screen: this.earthed_cable_screen(),
          chicken_wire: this.earthed_chicken_wire(),
          other: this.earthed_other(),
        },
        check_max_temp: {
          planning: this.max_temp_limited_by_planning(),
          installation: this.max_temp_limited_by_installation(),
          other: this.max_temp_limited_by_other(),
        },
        check_control_system: {
          room_sensor: this.control_system_room_sensor(),
          floor_sensor: this.control_system_floor_sensor(),
          designation: this.control_system_designation(),
          other: this.control_system_other(),
        },
      }
    })
    this.set(room)
    this.room_suggestion = ko.observable(
      new RoomSuggestion(this.root.Products().flat_room_type_info(),
        this))
    this.validationModel.errors.showAllMessages(false)

  }
  sub_modified = ko.computed(() => {
    if (this.heating_cables()) {
      for (let heating_cable of this.heating_cables().list()) {
        if (heating_cable.modified()) {
          return true
        }
      }
    }
    return false
  })
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

  // Add some additonal functionality when posting.
  post(h: any, event: Event, data_object?: any, url?: string) {
    return super.post(h, event, data_object, url).done(() => {
      $(event.target).closest('.collapse').collapse('hide')
    }
    )
  }
  set(room: RoomInterface = {
    room_name: '',
    id: -1,
    area: null,
    heated_area: null,
    outside: false,
    normalEffect: 0,
    maxEffect: 0
  }) {
    this.name(room.room_name)
    this.id(room.id)
    this.area(room.area)
    this.heated_area(room.heated_area)
    this.outside(room.outside)
    this.maxEffect(room.maxEffect || 0)
    this.normalEffect(room.normalEffect || 0)
    this.heating_cables(new HeatingCables(this.root, this, room.heating_cables))
    if (room.check_earthed) {
      this.earthed_cable_screen(room.check_earthed.cable_screen)
      this.earthed_chicken_wire(room.check_earthed.chicken_wire)
      this.earthed_other(room.check_earthed.other)
    }
    if (room.check_max_temp) {
      this.max_temp_limited_by_planning(room.check_max_temp.planning)
      this.max_temp_limited_by_installation(room.check_max_temp.installation)
      this.max_temp_limited_by_other(room.check_max_temp.other)
    }
    if (room.check_control_system) {
      this.control_system_floor_sensor(room.check_control_system.floor_sensor)
      this.control_system_room_sensor(room.check_control_system.room_sensor)
      this.control_system_designation(room.check_control_system.designation)
      this.control_system_other(room.check_control_system.other)
    }
    this.save()
  }
}

export class Rooms extends ByID {
  // list: KnockoutObservableArray<Room>
  parent: Customer
  root: TSAppViewModel

  constructor(root: TSAppViewModel, parent: Customer, list_of_rooms: RoomInterface[] = []) {
    super([])
    this.parent = parent
    this.root = root
    if (list_of_rooms) {
      let list_of_rooms_obects = list_of_rooms.map((x) => {
        return new Room(this.root, this, x)
      })
      this.list(list_of_rooms_obects)

    }


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
