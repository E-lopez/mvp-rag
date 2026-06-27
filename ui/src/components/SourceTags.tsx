interface SourceTagsProps {
  sources: string[]
}

export default function SourceTags({ sources }: SourceTagsProps) {
  if (!sources.length) return null

  return (
    <div className="mt-4 flex flex-wrap items-center gap-2">
      <span className="text-xs font-semibold uppercase tracking-wide text-gray-400">Sources</span>
      {sources.map((source) => (
        <span
          key={source}
          className="rounded-full border border-blue-200 bg-blue-50 px-3 py-1 text-xs font-medium text-blue-700"
        >
          {source}
        </span>
      ))}
    </div>
  )
}
