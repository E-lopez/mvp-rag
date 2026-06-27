import Markdown from 'react-markdown'
import { useAppState } from '../context/AppStateContext'
import SourceTags from './SourceTags'

export default function ResponseDisplay() {
  const { state } = useAppState()

  if (state.error) {
    return (
      <div className="w-full max-w-2xl rounded-lg border border-red-200 bg-red-50 px-5 py-4 text-sm text-red-700">
        {state.error}
      </div>
    )
  }

  if (!state.answer) return null

  return (
    <div className="w-full max-w-2xl rounded-lg border border-gray-200 bg-white px-6 py-5 shadow-sm">
      <div className="prose prose-sm max-w-none">
        <Markdown>{state.answer}</Markdown>
      </div>
      <SourceTags sources={state.sources} />
    </div>
  )
}
