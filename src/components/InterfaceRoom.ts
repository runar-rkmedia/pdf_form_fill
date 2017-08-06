export interface RoomSmartFill {
  name: string;
  outside?: boolean;
  aliases?: string[]
}

export let RoomSuggestionList: RoomSmartFill[] = [
  {
    name: 'Baderom',
    aliases: ['Bad']
  },
  {
    name: 'Toalett',
    aliases: ['WC']
  },
  {
    name: 'Vaskerom',
  },
  {
    name: 'Soverom',
  },
  {
    name: 'Kjøkken',
  },
  {
    name: 'Gang',
    aliases: ['Yttergang']
  },
  {
    name: 'Vindfang',
    aliases: ['VF']
  },
  {
    name: 'Stue',
  },
  {
    name: 'Tunet',
    outside: true,
    aliases: ['Gårdsplass']
  }
]

export interface RoomSuggestionInterface {
  name: string,
  id: number
}
