export function ChapterList({ chapters, selectedChapter, onSelect }: { chapters: any[]; selectedChapter: any; onSelect: (chapter: any) => void }) {
  return (
    <div style={{ display: 'grid', gap: 8 }}>
      {chapters.length === 0 ? (
        <div className="text-muted">Sin capítulos aún.</div>
      ) : (
        chapters.map((chapter) => (
          <button
            key={chapter.id}
            className={selectedChapter?.id === chapter.id ? 'secondary' : 'ghost'}
            onClick={() => onSelect(chapter)}
            style={{ textAlign: 'left', width: '100%' }}
          >
            {chapter.order_index}. {chapter.title}
          </button>
        ))
      )}
    </div>
  )
}
