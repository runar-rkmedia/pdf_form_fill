import 'knockout'


export class Pagination {
  list: KnockoutObservableArray<any> = ko.observableArray([])
  current_page: KnockoutObservable<number> = ko.observable(0)
  per_page = 10
  total_pages: KnockoutComputed<number> = ko.computed(() => {
    return this.list().length > 0 ? Math.floor(this.list().length / this.per_page) : 0
  })

  paginated = ko.computed(() => {
    let first = this.current_page() * this.per_page
    return this.list.slice(first, first + this.per_page)
  })

  has_previous = ko.computed(() => {
    return this.current_page() !== 0
  })

  has_next = ko.computed(() => {
    return this.current_page() !== this.total_pages()
  })

  next = () => {
    if (this.has_next()) {
      this.current_page(this.current_page() + 1)
    }
  }

  previous = () => {
    if (this.has_previous()) {
      this.current_page(this.current_page() - 1)
    }
  }
  goto = (item: any) => {
    let goto = this.list.indexOf(item)
    if (goto != -1) {
      let c = Math.floor(goto / this.per_page)
      this.current_page(c)
    }
  }
  constructor(list: any[], per_page = 10) {
    this.per_page = per_page
    this.list(list)
  }
}

// Sort any list of object by its distance to a setpoint to a certain key.
// For instance, sort all towns with distance closest to 800m:
// kings road: 760m
// queens road: 850m
// princes road: 750m
export let sortDist = (list: any[], setPoint: number, keyA = 'effect', keyB = 'name') => {
  return list.sort((a, b) => {
    let diff = 0;
    if (setPoint) {
      let diffA = Math.abs(setPoint - a[keyA])
      let diffB = Math.abs(setPoint - b[keyA])
      diff = diffA - diffB
    } else {
      diff = (a[keyA]) - (b[keyA]);
    }
    if (diff == 0) {
      if (a[keyB] < b[keyB]) {
        return -1
      }
      return 1
    }
    return diff

  });
}
