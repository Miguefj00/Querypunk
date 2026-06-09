interface Props {

    chapter: any;

    completed: number;

    total: number;

    onClick: () => void;
}

export default function ChapterCard({
                                        chapter,
                                        completed,
                                        total,
                                        onClick
                                    }: Props) {

    const percentage =
        total > 0
            ? Math.round(
                completed * 100 / total
            )
            : 0;

    return (

        <div
            className="chapter-card"
            onClick={onClick}
        >

            <h2>
                {chapter.title}
            </h2>

            <p>
                {chapter.description}
            </p>

            <div
                className="chapter-progress-header"
            >

            <span>
                {completed} / {total}
            </span>

                <span>
                {percentage}%
            </span>

            </div>

            <div
                className="chapter-progress-bar"
            >

                <div
                    className="chapter-progress-fill"
                    style={{
                        width:
                            `${percentage}%`
                    }}
                />

            </div>

        </div>

    );
}