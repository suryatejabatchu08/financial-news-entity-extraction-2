const ENTITY_COLORS = {
    PERSON: 'bg-blue-500/20 text-blue-300 border-blue-500/50',
    ORG: 'bg-purple-500/20 text-purple-300 border-purple-500/50',
    GPE: 'bg-green-500/20 text-green-300 border-green-500/50',
    MONEY: 'bg-yellow-500/20 text-yellow-300 border-yellow-500/50',
    DATE: 'bg-pink-500/20 text-pink-300 border-pink-500/50',
    PERCENT: 'bg-orange-500/20 text-orange-300 border-orange-500/50',
    PRODUCT: 'bg-cyan-500/20 text-cyan-300 border-cyan-500/50',
    EVENT: 'bg-red-500/20 text-red-300 border-red-500/50',
    LOC: 'bg-teal-500/20 text-teal-300 border-teal-500/50',
    NORP: 'bg-indigo-500/20 text-indigo-300 border-indigo-500/50',
}

function EntityDisplay({ entities, text }) {
    if (!entities || entities.length === 0) {
        return (
            <div className="text-center py-12 text-slate-400">
                <p>No entities detected. Try entering some financial news text.</p>
            </div>
        )
    }

    // Group entities by label
    const groupedEntities = entities.reduce((acc, entity) => {
        if (!acc[entity.label]) {
            acc[entity.label] = []
        }
        acc[entity.label].push(entity)
        return acc
    }, {})

    return (
        <div className="space-y-6">
            {/* Highlighted Text */}
            <div className="bg-slate-800/50 rounded-xl p-6 border border-slate-700/50">
                <h3 className="text-lg font-semibold text-white mb-4">Annotated Text</h3>
                <div className="text-slate-200 leading-relaxed">
                    {renderHighlightedText(text, entities)}
                </div>
            </div>

            {/* Entity Groups */}
            <div className="grid gap-4">
                {Object.entries(groupedEntities).map(([label, labelEntities]) => (
                    <div
                        key={label}
                        className="bg-slate-800/50 rounded-xl p-6 border border-slate-700/50"
                    >
                        <h3 className="text-lg font-semibold text-white mb-3">
                            {label} ({labelEntities.length})
                        </h3>
                        <div className="flex flex-wrap gap-2">
                            {labelEntities.map((entity, idx) => (
                                <span
                                    key={idx}
                                    className={`px-3 py-1.5 rounded-lg border font-medium text-sm ${ENTITY_COLORS[label] || 'bg-slate-500/20 text-slate-300 border-slate-500/50'
                                        }`}
                                >
                                    {entity.text}
                                </span>
                            ))}
                        </div>
                    </div>
                ))}
            </div>
        </div>
    )
}

function renderHighlightedText(text, entities) {
    if (!text || !entities || entities.length === 0) return text

    // Sort entities by start position
    const sortedEntities = [...entities].sort((a, b) => a.start - b.start)

    const parts = []
    let lastIndex = 0

    sortedEntities.forEach((entity, idx) => {
        // Add text before entity
        if (entity.start > lastIndex) {
            parts.push(
                <span key={`text-${idx}`}>{text.slice(lastIndex, entity.start)}</span>
            )
        }

        // Add highlighted entity
        const colorClass = ENTITY_COLORS[entity.label] || 'bg-slate-500/20 text-slate-300 border-slate-500/50'
        parts.push(
            <span
                key={`entity-${idx}`}
                className={`${colorClass} px-1.5 py-0.5 rounded border font-medium`}
                title={entity.label}
            >
                {entity.text}
            </span>
        )

        lastIndex = entity.end
    })

    // Add remaining text
    if (lastIndex < text.length) {
        parts.push(
            <span key="text-end">{text.slice(lastIndex)}</span>
        )
    }

    return parts
}

export default EntityDisplay
