import ChapterCard
    from "./ChapterCard";

import type {
    Chapter,
    SolvedChallenge
} from "../../types/gameplay.types";

interface Props {

    chapters: Chapter[];

    progress: SolvedChallenge[];

    chapterTotals: Record<number, number>;

    onSelect: (
        chapter: Chapter
    ) => void;
}


export default function ChapterList({
                                        chapters,
                                        progress,
                                        chapterTotals,
                                        onSelect
                                    }: Props){

    return (

        <div className="chapter-grid">

            {
                chapters.map(chapter => {

                    const completed =
                        progress.filter(
                            p =>
                                p.chapter_id ===
                                chapter.id
                        ).length;

                    const total =
                        chapterTotals[chapter.id] || 0;

                    return (

                        <ChapterCard
                            key={chapter.id}
                            chapter={chapter}
                            completed={completed}
                            total={total}
                            onClick={() =>
                                onSelect(chapter)
                            }
                        />

                    );
                })
            }

        </div>

    );
}