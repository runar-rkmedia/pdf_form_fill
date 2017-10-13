import {
  ByID,
  Post,
  ObsMod,
  HTTPVerbs
} from "./Common"
import { TSAppViewModel } from "./AppViewModel"
import { RoomTypesInfoFlat } from "./ProductModel"
import { CustomerInterface, Customer } from './Customer'
import { HeatingCable, HeatingCableInterface } from './HeatingCable'
import { HeatingCableList } from './HeatingCableList'
import { RoomList } from './RoomList'

require("knockout-template-loader?name=room-suggestion-template!html-loader?-minimize!./room-suggestion.html");

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

interface InsideSpecs {
  LamiFlex: boolean
  low_profile: boolean
  fireproof: boolean
  frost_protection_pipe: boolean
  other: string
  concrete: boolean
}
interface OutsideSpecs {
  asphalt: boolean
  paving_stones: boolean
  vessel: boolean
  frost_protection_pipe: boolean
  frost_protection: boolean
  concrete: boolean
}

interface CheckControlSystem {
  floor_sensor: boolean
  limit_sensor: boolean
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
  normalEffect: number
  curcuit_breaker_size: number
  ground_fault_protection: number
  installation_depth?: number
  check_earthed?: CheckEarthed
  check_max_temp?: CheckMaxTemp
  check_control_system?: CheckControlSystem
  inside_specs?: InsideSpecs
  outside_specs?: OutsideSpecs
  handed_to_owner: boolean
  owner_informed: boolean
}

interface MultiSave {
  rooms: RoomInterface[]
  heating_cables: HeatingCableInterface[]
}

export class Room extends Post {
  url = '/json/v1/room/'
  id: KnockoutObservable<number> = ko.observable()
  name = <ObsMod<string>>this.obs_mod();
  outside = <ObsMod<boolean>>this.obs_mod(undefined, undefined, false);

  outside_concrete = <ObsMod<boolean>>this.obs_mod();
  outside_asphalt = <ObsMod<boolean>>this.obs_mod();
  outside_paving_stones = <ObsMod<boolean>>this.obs_mod();
  outside_vessel = <ObsMod<boolean>>this.obs_mod();
  outside_frost_protection = <ObsMod<boolean>>this.obs_mod();
  outside_frost_protection_pipe = <ObsMod<boolean>>this.obs_mod();

  inside_concrete = <ObsMod<boolean>>this.obs_mod();
  inside_LamiFlex = <ObsMod<boolean>>this.obs_mod();
  inside_low_profile = <ObsMod<boolean>>this.obs_mod();
  inside_fireproof = <ObsMod<boolean>>this.obs_mod();
  inside_frost_protection_pipe = <ObsMod<boolean>>this.obs_mod();
  inside_other = <ObsMod<string>>this.obs_mod();

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
  control_system_limit_sensor = <ObsMod<boolean>>this.obs_mod(undefined, undefined, false);
  control_system_room_sensor = <ObsMod<boolean>>this.obs_mod();
  handed_to_owner = <ObsMod<boolean>>this.obs_mod(undefined, undefined, true);
  owner_informed = <ObsMod<boolean>>this.obs_mod(undefined, undefined, true);
  control_system_designation = <ObsMod<string>>this.obs_mod();
  curcuit_breaker_size = <ObsMod<number>>this.obs_mod(undefined, undefined, 16);
  installation_depth = <ObsMod<number>>this.obs_mod(undefined, undefined, 30);
  ground_fault_protection = <ObsMod<number>>this.obs_mod(undefined, undefined, 30);
  control_system_other = <ObsMod<string>>this.obs_mod();
  heating_cables: KnockoutObservable<HeatingCableList> = ko.observable()
  room_suggestion: KnockoutObservable<RoomSuggestion>
  validationModel = ko.validatedObservable({
    name: this.name,
    outside: this.outside,
    area: this.area,
    heated_area: this.heated_area
  })
  root: TSAppViewModel
  serialize: KnockoutComputed<RoomInterface>
  parent: RoomList

  constructor(root: TSAppViewModel, parent: RoomList, room: RoomInterface | undefined = undefined) {
    super(parent)
    let customer = parent.parent
    this.form_url = `${this.form_url}${customer.id()}/`

    this.root = root
    this.area.extend(
      { required: true, number: true, min: 0.1, max: 1000 });
    this.heated_area.extend(
      { required: true, number: true, min: 0.1, max: 1000 });
    this.name.extend(
      { required: true, minLength: 2, maxLength: 50 });

    this.serialize = ko.computed((): RoomInterface => {
      let data: RoomInterface = {
        room_name: this.name(),
        id: this.id(),
        area: this.area(),
        heated_area: this.heated_area(),
        outside: this.outside(),
        customer_id: this.parent.parent.id(),
        maxEffect: this.maxEffect(),
        normalEffect: this.normalEffect(),
        curcuit_breaker_size: this.curcuit_breaker_size(),
        ground_fault_protection: this.ground_fault_protection(),
        installation_depth: this.installation_depth(),
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
          limit_sensor: this.control_system_limit_sensor(),
          designation: this.control_system_designation(),
          other: this.control_system_other(),
        },
        handed_to_owner: this.handed_to_owner(),
        owner_informed: this.owner_informed(),
      }
      if (this.use_inside_checklist()) {
        data.inside_specs = {
          LamiFlex: this.inside_LamiFlex(),
          low_profile: this.inside_low_profile(),
          fireproof: this.inside_fireproof(),
          frost_protection_pipe: this.inside_frost_protection_pipe(),
          other: this.inside_other(),
          concrete: this.inside_concrete(),
        }
      }
      if (this.use_outside_checklist()) {
        data.outside_specs = {
          asphalt: this.outside_asphalt(),
          paving_stones: this.outside_paving_stones(),
          vessel: this.outside_vessel(),
          frost_protection_pipe: this.outside_frost_protection_pipe(),
          frost_protection: this.outside_frost_protection(),
          concrete: this.outside_concrete(),
        }
      }
      return data
    })
    this.set(room)
    ko.computed(() => {
      if (this.name() && this.room_suggestion) {
        let match = ko.utils.arrayFirst(this.room_suggestion().list(), (item) => {
          return this.name().toLowerCase() === item.name.toLowerCase();
        });
        if (match) {
          this.normalEffect(match.normalEffect)
          this.maxEffect(match.maxEffect)
          this.outside(match.outside)
          this.name(match.name)
        }
      }
    })
    this.room_suggestion = ko.observable(
      new RoomSuggestion(this.root.Products().flat_room_type_info(),
        this))
    this.validationModel.errors.showAllMessages(false)

  }
  use_inside_checklist = ko.computed((): boolean => {
    if (this.heating_cables()) {
      if (!this.outside()) {
        if (this.heating_cables().has_manufacturor('Øglænd')) {
          return true
        }
      }
    }
    return false
  })
  use_outside_checklist = ko.computed((): boolean => {
    if (this.heating_cables()) {
      if (this.outside()) {
        if (this.heating_cables().has_manufacturor('Øglænd')) {
          return true
        }
      }
    }
    return false
  })
  post_all(h: any, event: Event) {
    let data: MultiSave = {
      rooms: [],
      heating_cables: []
    }
    if (this.modified()) {
      data.rooms.push(this.serialize())
    }
    for (let heating_cable of this.heating_cables().list()) {
      if (heating_cable.modified()) {
        data.heating_cables.push(heating_cable.serialize())
      }
    }
    if (data.rooms.length > 0 || data.heating_cables.length > 0) {
      return super.post(h, event, data, '/json/v1/multi_save').done((result: any, successTextStatus: any, jqXHR: any) => {
        let method = jqXHR.originalRequestOptions.type
        for (let heating_cable of this.heating_cables().list()) {
          if (heating_cable.id() == -1) {
            heating_cable.set(result)
          } else {
            heating_cable.save()

          }
        }
      })

    }
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
    maxEffect: 0,
    installation_depth: 30,
    curcuit_breaker_size: 16,
    ground_fault_protection: 30,
    handed_to_owner: true,
    owner_informed: true,
    inside_specs: {
      LamiFlex: false,
      low_profile: false,
      fireproof: false,
      frost_protection_pipe: false,
      other: '',
      concrete: false,
    },
    outside_specs: {
      asphalt: false,
      paving_stones: false,
      vessel: false,
      frost_protection_pipe: false,
      frost_protection: false,
      concrete: false,
    }
  }) {
    this.name(room.room_name)
    this.id(room.id)
    this.area(room.area)
    this.heated_area(room.heated_area)
    this.outside(room.outside)
    this.maxEffect(room.maxEffect || 0)
    this.handed_to_owner(room.handed_to_owner)
    this.owner_informed(room.owner_informed)
    this.installation_depth(Number(room.installation_depth) || 30)
    this.ground_fault_protection(Number(room.ground_fault_protection) || 30)
    this.curcuit_breaker_size(Number(room.curcuit_breaker_size) || 16)
    this.normalEffect(room.normalEffect || 0)
    this.heating_cables(new HeatingCableList(this.root, this, room.heating_cables))
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
      this.control_system_limit_sensor(room.check_control_system.limit_sensor)
      this.control_system_room_sensor(room.check_control_system.room_sensor)
      this.control_system_designation(room.check_control_system.designation)
      this.control_system_other(room.check_control_system.other)
    }
    if (room.inside_specs) {
      this.inside_LamiFlex(room.inside_specs.LamiFlex)
      this.inside_low_profile(room.inside_specs.low_profile)
      this.inside_fireproof(room.inside_specs.fireproof)
      this.inside_frost_protection_pipe(room.inside_specs.frost_protection_pipe)
      this.inside_other(room.inside_specs.other)
      this.inside_concrete(Boolean(room.inside_specs.concrete))
    }
    if (room.outside_specs) {
      this.outside_asphalt(room.outside_specs.asphalt)
      this.outside_paving_stones(room.outside_specs.paving_stones)
      this.outside_vessel(room.outside_specs.vessel)
      this.outside_frost_protection_pipe(room.outside_specs.frost_protection_pipe)
      this.outside_frost_protection(room.outside_specs.frost_protection)
      this.outside_concrete(Boolean(room.outside_specs.concrete))
    }

    this.save()
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
    value(roomSuggestion.name)
    this.parent.outside(Boolean(roomSuggestion.outside))
    this.parent.maxEffect(roomSuggestion.maxEffect)
    this.parent.normalEffect(roomSuggestion.normalEffect)
    this.parent.name.isModified(false)
  }
}
