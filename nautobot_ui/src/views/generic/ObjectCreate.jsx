import { useParams } from "react-router-dom"

import CreateViewTemplate from "@views/BSCreateViewTemplate"
import { nautobot_url } from "src/index"


export default function BSCreateView({ list_url }) {
  const { app_name, model_name } = useParams()

  if (!app_name || !model_name) {
    return <></>
  }
  if (!list_url) {
    list_url = `${nautobot_url}/api/${app_name}/${model_name}/`
  }
  console.log(list_url)
  return (
    <CreateViewTemplate list_url={list_url} />
  )
}
