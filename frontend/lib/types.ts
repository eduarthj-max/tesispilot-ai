export type Thesis = {
  id: string
  title: string
  topic?: string
  abstract?: string
  status?: string
}

export type Chapter = {
  id: string
  thesis_id: string
  title: string
  content?: string
  order_index?: number
}
