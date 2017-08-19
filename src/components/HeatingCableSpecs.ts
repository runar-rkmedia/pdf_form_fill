import { Base } from "./Common"
import { HeatingCable } from './HeatingCable'

interface MeasurementsInterface {
  ohm_a: number
  ohm_b: number
  ohm_c: number
  mohm_a: number
  mohm_b: number
  mohm_c: number
}
interface CalculationsInterface {
  cc: number
  w_per_m2: number
}
export interface HeatingCableSpecs {
  measurements?: MeasurementsInterface
  calculations?: CalculationsInterface
  Area: number
  Length: number
  width: number
}

export class Measurements extends Base {
  ohm_a: KnockoutObservable<number> = ko.observable();
  ohm_b: KnockoutObservable<number> = ko.observable();
  ohm_c: KnockoutObservable<number> = ko.observable();
  mohm_a: KnockoutObservable<number> = ko.observable();
  mohm_b: KnockoutObservable<number> = ko.observable();
  mohm_c: KnockoutObservable<number> = ko.observable();
  // modified: KnockoutObservable<boolean>
  last_sent_data: KnockoutObservable<MeasurementsInterface> = ko.observable()

  constructor() {
    super()
    this.init()
  }
  set(measurements?: MeasurementsInterface) {
    if (measurements) {
      this.ohm_a(measurements.ohm_a)
      this.ohm_b(measurements.ohm_b)
      this.ohm_c(measurements.ohm_c)

      this.mohm_a(measurements.mohm_a)
      this.mohm_b(measurements.mohm_b)
      this.mohm_c(measurements.mohm_c)
    }
  }
  serialize = ko.computed(() => {
    return {
      ohm_a: Number(this.ohm_a()),
      ohm_b: Number(this.ohm_b()),
      ohm_c: Number(this.ohm_c()),
      mohm_a: (this.mohm_a() ? 999 : -1),
      mohm_b: (this.mohm_b() ? 999 : -1),
      mohm_c: (this.mohm_c() ? 999 : -1),
    }
  })
}

export class Calculations extends Base {
  cc: KnockoutComputed<number | undefined>
  serialize: KnockoutComputed<CalculationsInterface>
  w_per_m2: KnockoutComputed<number | undefined>
  // modified: KnockoutObservable<boolean>
  last_sent_data: KnockoutObservable<CalculationsInterface> = ko.observable()
  parent: HeatingCable

  constructor(parent: HeatingCable) {
    super()
    this.parent = parent
    this.init()

    this.cc = ko.computed(() => {
      if (this.parent.product()) {
        let effect = this.parent.product()!.effect
        if (effect) {
          return effect
        }
      }
    })
    this.w_per_m2 = ko.computed(() => {
      if (this.parent.product()) {
        console.log(this.parent.product().specs)
        let effect = this.parent.product()!.effect
        let heated_area = this.parent.parent.parent.heated_area()
        if (effect) {
          return effect / heated_area
        }
      }
    })
    this.serialize = ko.computed(() => {
      return {
        cc: Number(this.cc()),
        w_per_m2: Number(this.w_per_m2()),
        mcc: (this.cc() ? 999 : -1),
        mw_per_m2: (this.w_per_m2() ? 999 : -1),
      }
    })
  }
  set(calculations: CalculationsInterface) {
    if (calculations) {
      this.cc(calculations.cc)
      this.w_per_m2(calculations.w_per_m2)

      this.cc(calculations.cc)
      this.w_per_m2(calculations.w_per_m2)
    }
  }
}
